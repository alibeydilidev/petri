"""S1 ana döngü: tek ajan, kanal KAPALI, online self-supervised öğrenme.

Ödül yok, politika ağı yok: ajan her tur MPC ile eylem seçer, dünyadan
gerçek gözlemi alır, tahmin hatasıyla (TBPTT) öğrenir. Ölüm epizodu
bitirir. S1'de ağırlıklar epizotlar arası TAŞINIR (PL-06: "yetiştirme
kabı" modu — DP-01'in "ölüm gerçek" kuralı S3+ ekoloji deneyinin
kuralıdır; S1 makine dairesi testidir).

Determinizm: torch.manual_seed + tek thread + ajanın kendi numpy
Generator'ı. Aynı seed üçlüsü → bit-eş ağırlıklar (test edilir).
"""

import numpy as np
import torch
import torch.nn.functional as F

from agent.config import AgentConfig
from agent.homeostasis import Homeostasis
from agent.mpc import MPCPlanner
from agent.predictive_core import PredictiveCore
from world.config import WorldConfig
from world.grid import N_ACTIONS, STAY, World

torch.set_num_threads(1)  # bit-eş tekrarlanabilirlik > hız (S1 ölçeğinde yeter)


def encode_obs(grid_obs: np.ndarray, energy: float, cfg: AgentConfig,
               signals_vec: np.ndarray | None = None) -> torch.Tensor:
    """(4,w,w) grid [+ 16 alınan-sinyal] + enerji → (obs_dim,) float32.
    Enerji SON boyut (mpc.ENERGY_DIM).

    interoception=False (PL-15 kontrolü): enerji boyutu sıfırlanır —
    hedef de bu kodlayıcıdan geçtiği için enerji tahmin hedefinden de
    silinmiş olur; boyutlar sabit kalır."""
    parts = [torch.from_numpy(grid_obs.reshape(-1))]
    if cfg.channel_open:
        sv = (np.zeros(16, dtype=np.float32) if signals_vec is None
              else signals_vec)
        parts.append(torch.as_tensor(sv, dtype=torch.float32))
    e_val = energy / cfg.max_energy if cfg.interoception else 0.0
    parts.append(torch.tensor([e_val], dtype=torch.float32))
    return torch.cat(parts)


class OnlineAgent:
    """Tahmin çekirdeği + homeostaz + MPC'yi bir bedende toplar."""

    def __init__(self, cfg: AgentConfig, torch_seed: int, np_seed: int):
        self.cfg = cfg
        torch.manual_seed(torch_seed)
        self.core = PredictiveCore(cfg)
        self.opt = torch.optim.Adam(self.core.parameters(), lr=cfg.learning_rate)
        self.planner = MPCPlanner(cfg, np.random.default_rng(np_seed))
        self.grid_w = 2 * cfg.obs_radius + 1
        self.per = None
        if cfg.per_enabled:  # K-110
            from training.per import PERBuffer
            self.per = PERBuffer(cfg.per_buffer_size, cfg.per_alpha,
                                 np.random.default_rng(np_seed + 500_000))
            self.per.stratify_prob = cfg.per_stratify_prob
            self.per.spatial_weight = cfg.per_spatial_weight  # K-110rev
        # M-14 sayaçları: öz-hareket geçişlerinin taban oranı (S2.9 iş 1)
        self.stats = {"transitions": 0, "move_visible": 0, "move_shift": 0}
        self.reset_episode_state()

    def reset_episode_state(self) -> None:
        """Epizot sınırı: hidden ve TBPTT penceresi sıfırlanır (ağırlıklar değil)."""
        self.h = None            # (1,1,H) detached
        self.h_start = None      # pencere başı hidden
        self.window: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = []

    def eval_clone(self, eval_seed: int) -> "OnlineAgent":
        """Öğrenmesiz değerlendirme kopyası. Orijinalin ağırlıklarına,
        optimizer'ına ve rng'sine DOKUNMAZ; torch global seed'i de
        değiştirmez (zero-touch: tests/test_s2_gen.py bit-eş kanıtı)."""
        import copy
        clone = OnlineAgent.__new__(OnlineAgent)
        clone.cfg = self.cfg
        clone.core = copy.deepcopy(self.core)
        clone.opt = None
        clone.planner = MPCPlanner(self.cfg, np.random.default_rng(eval_seed))
        clone.grid_w = self.grid_w
        clone.reset_episode_state()
        return clone

    def observe_step(self, obs_vec: torch.Tensor, action: int) -> None:
        """Hidden'ı ilerletir, ÖĞRENMEZ (checkpoint değerlendirmesi için)."""
        act_oh = torch.zeros(N_ACTIONS)
        act_oh[action] = 1.0
        self.observe_step_vec(obs_vec, act_oh)

    def observe_step_vec(self, obs_vec: torch.Tensor,
                         act_vec: torch.Tensor) -> None:
        with torch.no_grad():
            _, self.h = self.core(obs_vec.view(1, 1, -1),
                                  act_vec.view(1, 1, -1), self.h)

    def act(self, obs_vec: torch.Tensor) -> int:
        # ε-greedy (K-108): MPC argmax'ının kendi verisini yanlılaştırıp
        # hiç görülmeyen eylemleri öğrenilemez kılmasını kırar. ε ajanın
        # parçasıdır; eval'de de açık kalır (makyaj yok).
        if self.planner.rng.random() < self.cfg.mpc_epsilon:
            # K-110rev ε hareket yanlılığı: bias=0 → eski tek-çekiliş yolu
            # birebir korunur (bit-eş).
            if self.cfg.eps_move_bias > 0.0 and \
                    self.planner.rng.random() < self.cfg.eps_move_bias:
                return int(self.planner.rng.integers(1, 5))  # UP..RIGHT
            return int(self.planner.rng.integers(0, N_ACTIONS))
        return self.planner.plan(self.core, self.h, obs_vec)

    def learn_step(self, obs_vec: torch.Tensor, action: int,
                   next_obs_vec: torch.Tensor) -> float | None:
        act_oh = torch.zeros(N_ACTIONS)
        act_oh[action] = 1.0
        return self.learn_step_vec(obs_vec, act_oh, next_obs_vec)

    def learn_step_vec(self, obs_vec: torch.Tensor, act_vec: torch.Tensor,
                       next_obs_vec: torch.Tensor) -> float | None:
        """Bir turun deneyimini işler; pencere dolarsa gradyan adımı atar.
        act_vec: efferens vektörü (kapalı: 6; kanal açık: 6+17 — S3).

        Dönüş: gradyan adımı atıldıysa loss, yoksa None.
        """
        act_oh = act_vec
        self.window.append((obs_vec, act_oh, next_obs_vec))

        # Hidden'ı ilerlet (grad'sız; eğitim ileri geçişi pencere sonunda).
        with torch.no_grad():
            _, self.h = self.core(obs_vec.view(1, 1, -1),
                                  act_oh.view(1, 1, -1), self.h)

        if len(self.window) < self.cfg.tbptt_window:
            return None

        obs = torch.stack([w[0] for w in self.window]).unsqueeze(0)
        acts = torch.stack([w[1] for w in self.window]).unsqueeze(0)
        targets = torch.stack([w[2] for w in self.window]).unsqueeze(0)
        pred, h_n = self.core(obs, acts, self.h_start)
        grid_loss = F.mse_loss(pred[..., :-1], targets[..., :-1])
        energy_loss = F.mse_loss(pred[..., -1], targets[..., -1])
        loss = grid_loss + self.cfg.energy_loss_weight * energy_loss  # K-106
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

        # M-14 sayaçları: hareket eylemi altında (a) kaynak görünür,
        # (b) grid gerçekten değişti (kayma deneyimi).
        act_ids = acts[0, :, :N_ACTIONS].argmax(dim=-1)
        move_mask = (act_ids >= 1) & (act_ids <= 4)
        w2 = self.grid_w * self.grid_w
        vis_mask = obs[0, :, :w2].sum(dim=-1) > 0  # yalnız A-kanalı
        gchange_steps = (targets[0, :, :-1] - obs[0, :, :-1]).abs().sum(dim=-1)
        self.stats["transitions"] += int(acts.shape[1])
        self.stats["move_visible"] += int((move_mask & vis_mask).sum())
        self.stats["move_shift"] += int((move_mask
                                         & (gchange_steps > 0.5)).sum())

        if self.per is not None:  # K-110: pencereyi tampona + tekrar adımı
            acts_present = np.zeros(6, dtype=bool)
            acts_present[acts[..., :N_ACTIONS].argmax(dim=-1)
                         .unique().numpy()] = True
            h0 = None if self.h_start is None else self.h_start.detach().clone()
            grid_change = float(gchange_steps.mean())  # K-110rev ağırlığı
            self.per.push((obs.detach(), acts.detach(), targets.detach(), h0),
                          priority=float(loss.item()),
                          actions_present=acts_present,
                          grid_change=grid_change)
            if len(self.per) >= self.cfg.per_batch:
                self._replay_step()

        self.h = h_n.detach()  # güncelleme öncesi ağırlıklarla hesaplanmış — standart TBPTT
        self.h_start = self.h
        self.window.clear()
        return float(loss.item())

    def _replay_step(self) -> None:
        """PER tekrar adımı: kayıp-orantılı örneklenen pencerelerde bir
        gradyan adımı; öncelikler taze kayıpla güncellenir."""
        B = self.cfg.per_batch
        idx, batch = self.per.sample(B)
        obs = torch.cat([b[0] for b in batch], dim=0)      # (B, W, obs)
        acts = torch.cat([b[1] for b in batch], dim=0)
        targets = torch.cat([b[2] for b in batch], dim=0)
        H = self.cfg.memory_dim
        h0 = torch.zeros(1, B, H)
        for i, b in enumerate(batch):
            if b[3] is not None:
                h0[:, i, :] = b[3][:, 0, :]
        pred, _ = self.core(obs, acts, h0)
        grid_se = (pred[..., :-1] - targets[..., :-1]) ** 2
        energy_se = (pred[..., -1] - targets[..., -1]) ** 2
        per_item = (grid_se.mean(dim=(1, 2))
                    + self.cfg.energy_loss_weight * energy_se.mean(dim=1))
        loss = per_item.mean()
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()
        self.per.update(idx, per_item.detach().numpy())


def run_episode(agent_or_policy, world_seed: int, cfg: AgentConfig,
                max_turns: int = 1500, world_cfg: WorldConfig | None = None,
                snapshot=None, random_rng: np.random.Generator | None = None,
                learn: bool = True, spawn_seed: int | None = None,
                nest_rng: np.random.Generator | None = None) -> dict:
    """Tek epizot koşar. `agent_or_policy`: OnlineAgent, "random" ya da
    "stay" (saf-tasarruf taban çizgisi: her tur STAY, ε=0 — S2.5).

    spawn_seed (PL-11): verilirse ajanın başlangıç hücresi dünya
    yerleşiminden BAĞIMSIZ, seed'li olarak yeniden örneklenir (dünya
    rng'sine dokunmaz; determinizm korunur).

    Dönüş: {"lifetime", "harvested", "harvest_count", "capped"}
    """
    wcfg = world_cfg or WorldConfig()
    world = World(wcfg, n_entities=1, seed=world_seed)
    if spawn_seed is not None:
        world.entity_pos[0] = np.random.default_rng(spawn_seed).integers(
            0, wcfg.grid_size, size=2)
    if nest_rng is not None:  # S2.7 yuva müfredatı: kaynak-yakını doğum
        k = int(nest_rng.integers(0, wcfg.resource_a_count))
        off = nest_rng.integers(-2, 3, size=2)  # Chebyshev <= 2
        world.entity_pos[0] = (world.res_a[k] + off) % wcfg.grid_size
    homeo = Homeostasis(cfg)
    is_random = agent_or_policy == "random"
    is_stay = agent_or_policy == "stay"
    is_oracle = hasattr(agent_or_policy, "act_grid")  # S2.6 fizibilite oracle'ı
    scripted = is_random or is_stay or is_oracle
    if is_oracle:
        agent_or_policy.reset()
    if not scripted:
        agent_or_policy.reset_episode_state()
    if snapshot is not None:
        snapshot.note_start(world)

    harvested, harvest_count = 0.0, 0
    obs_vec = None
    if not scripted:
        obs_vec = encode_obs(world.observe(0, cfg.obs_radius), homeo.energy, cfg)

    turn = 0
    while turn < max_turns:
        if is_random:
            action = int(random_rng.integers(0, N_ACTIONS))
        elif is_stay:
            action = STAY
        elif is_oracle:
            action = agent_or_policy.act_grid(world.observe(0, cfg.obs_radius))
        else:
            action = agent_or_policy.act(obs_vec)

        deltas = world.step(np.array([action]))
        homeo.apply_turn(action, float(deltas[0]))
        if deltas[0] > 0:
            harvested += float(deltas[0])
            harvest_count += 1
        turn += 1

        if not scripted:
            next_obs = encode_obs(world.observe(0, cfg.obs_radius),
                                  max(homeo.energy, 0.0), cfg)
            if learn:
                agent_or_policy.learn_step(obs_vec, action, next_obs)
            else:
                agent_or_policy.observe_step(obs_vec, action)
            if snapshot is not None:
                snapshot.capture(world, agent_or_policy, homeo, action)
            obs_vec = next_obs

        if not homeo.alive:
            break

    return {"lifetime": turn, "harvested": harvested,
            "harvest_count": harvest_count,
            "capped": turn >= max_turns and homeo.alive}
