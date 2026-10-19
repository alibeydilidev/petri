"""Program A1 — EnsembleAgent: OnlineAgent'ın K-üyeli topluluk sürümü.

Aynı veri, aynı pencere, aynı PER; her üye kendi hidden'ı ve kendi
kaybıyla eğitilir (toplam kayıp = üyelerin toplamı). Dışarıya `core`
(EnsembleCore) ve `h` (liste) sunar; planlayıcı `core.members` görünce
üye-başına rollout + uyuşmazlık cezası uygular.
"""

import copy

import numpy as np
import torch
import torch.nn.functional as F

from agent.config import AgentConfig
from agent.ensemble import EnsembleCore, clone_h, detach_h
from agent.mpc import MPCPlanner
from training.loop import OnlineAgent
from world.grid import N_ACTIONS


class EnsembleAgent(OnlineAgent):
    def __init__(self, cfg: AgentConfig, torch_seed: int, np_seed: int):
        self.cfg = cfg
        torch.manual_seed(torch_seed)
        self.core = EnsembleCore(cfg, cfg.ensemble_k, torch_seed)
        self.opt = torch.optim.Adam(self.core.parameters(), lr=cfg.learning_rate)
        self.planner = MPCPlanner(cfg, np.random.default_rng(np_seed))
        self.grid_w = 2 * cfg.obs_radius + 1
        self.per = None
        if cfg.per_enabled:
            from training.per import PERBuffer
            self.per = PERBuffer(cfg.per_buffer_size, cfg.per_alpha,
                                 np.random.default_rng(np_seed + 500_000))
            self.per.stratify_prob = cfg.per_stratify_prob
            self.per.spatial_weight = cfg.per_spatial_weight
        self.stats = {"transitions": 0, "move_visible": 0, "move_shift": 0}
        self.reset_episode_state()

    def eval_clone(self, eval_seed: int):
        clone = EnsembleAgent.__new__(EnsembleAgent)
        clone.cfg = self.cfg
        clone.core = copy.deepcopy(self.core)
        clone.opt = None
        clone.planner = MPCPlanner(self.cfg, np.random.default_rng(eval_seed))
        clone.grid_w = self.grid_w
        clone.per = None
        clone.stats = dict(self.stats)
        clone.reset_episode_state()
        return clone

    def observe_step_vec(self, obs_vec, act_vec):
        with torch.no_grad():
            _, self.h = self.core(obs_vec.view(1, 1, -1), act_vec.view(1, 1, -1), self.h)

    def learn_step_vec(self, obs_vec, act_vec, next_obs_vec):
        self.window.append((obs_vec, act_vec, next_obs_vec))
        with torch.no_grad():
            _, self.h = self.core(obs_vec.view(1, 1, -1), act_vec.view(1, 1, -1), self.h)
        if len(self.window) < self.cfg.tbptt_window:
            return None
        obs = torch.stack([w[0] for w in self.window]).unsqueeze(0)
        acts = torch.stack([w[1] for w in self.window]).unsqueeze(0)
        targets = torch.stack([w[2] for w in self.window]).unsqueeze(0)
        outs = self.core.member_outputs(obs, acts, self.h_start)
        loss = 0.0
        for pred, _ in outs:
            grid_loss = F.mse_loss(pred[..., :-1], targets[..., :-1])
            energy_loss = F.mse_loss(pred[..., -1], targets[..., -1])
            loss = loss + grid_loss + self.cfg.energy_loss_weight * energy_loss
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()
        h_n = [hn for _, hn in outs]

        act_ids = acts[0, :, :N_ACTIONS].argmax(dim=-1)
        move_mask = (act_ids >= 1) & (act_ids <= 4)
        w2 = self.grid_w * self.grid_w
        vis_mask = obs[0, :, :w2].sum(dim=-1) > 0
        gchange_steps = (targets[0, :, :-1] - obs[0, :, :-1]).abs().sum(dim=-1)
        self.stats["transitions"] += int(acts.shape[1])
        self.stats["move_visible"] += int((move_mask & vis_mask).sum())
        self.stats["move_shift"] += int((move_mask & (gchange_steps > 0.5)).sum())

        if self.per is not None:
            acts_present = np.zeros(6, dtype=bool)
            acts_present[acts[..., :N_ACTIONS].argmax(dim=-1).unique().numpy()] = True
            h0 = clone_h(self.h_start)
            self.per.push((obs.detach(), acts.detach(), targets.detach(), h0),
                          priority=float(loss.item()) / self.core.k,
                          actions_present=acts_present,
                          grid_change=float(gchange_steps.mean()))
            if len(self.per) >= self.cfg.per_batch:
                self._replay_step()
        self.h = detach_h(h_n)
        self.h_start = self.h
        self.window.clear()
        return float(loss.item()) / self.core.k

    def _replay_step(self):
        B = self.cfg.per_batch
        idx, batch = self.per.sample(B)
        obs = torch.cat([b[0] for b in batch], dim=0)
        acts = torch.cat([b[1] for b in batch], dim=0)
        targets = torch.cat([b[2] for b in batch], dim=0)
        H = self.cfg.memory_dim
        per_item_total = torch.zeros(B)
        loss = 0.0
        for k, m in enumerate(self.core.members):
            h0 = torch.zeros(1, B, H)
            for i, b in enumerate(batch):
                if b[3] is not None:
                    h0[:, i, :] = b[3][k][:, 0, :]
            pred, _ = m(obs, acts, h0)
            grid_se = (pred[..., :-1] - targets[..., :-1]) ** 2
            energy_se = (pred[..., -1] - targets[..., -1]) ** 2
            per_item = grid_se.mean(dim=(1, 2)) + self.cfg.energy_loss_weight * energy_se.mean(dim=1)
            per_item_total = per_item_total + per_item.detach()
            loss = loss + per_item.mean()
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()
        self.per.update(idx, (per_item_total / self.core.k).numpy())
