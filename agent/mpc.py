"""MPC eylem seçici: öğrenilmiş world-model üzerinde açık-döngü rollout.

Politika ağı YOK, ödül YOK. Aday eylem dizileri örneklenir, model ile
hayal edilir (tahmin edilen gözlem geri beslenir), homeostatik hedef
J = ufuk sonunda tahmin edilen kendi enerjisi (KERNEL_BUDGET K-103)
ile puanlanır; en iyi dizinin İLK eylemi uygulanır.

Keşif ayrıca teşvik edilmez (merak terimi YOK — K-104): erken dönemde
model kötüyken argmax rastgele adaylar üzerinde ~rastgele davranır;
keşif buradan gelir.

Determinizm: adaylar ajanın kendi numpy Generator'ından örneklenir;
torch yalnız ileri geçişte kullanılır (no_grad).
"""

import numpy as np
import torch

from agent.config import AgentConfig
from agent.predictive_core import PredictiveCore
from world.grid import N_ACTIONS

# Gözlem vektöründe enerji skalarının indeksi: son eleman (bkz. loop._encode_obs).
ENERGY_DIM = -1


class MPCPlanner:
    def __init__(self, cfg: AgentConfig, rng: np.random.Generator):
        self.cfg = cfg
        self.rng = rng

    @torch.no_grad()
    def _score(self, core: PredictiveCore, h, obs_vec: torch.Tensor,
               seqs: np.ndarray) -> np.ndarray:
        """Aday dizileri J = ufuk-ortalaması tahmini enerji ile puanlar
        (K-103). Rollout geri beslemesi [0,1]'e kırpılır."""
        C, D = seqs.shape
        # K-112: skorlama ufku kırpma — rollout güvenilirliği (H_eff)
        # ötesindeki hayal adımları J'ye katılmaz (roll da edilmez).
        kmax = D if self.cfg.mpc_score_horizon is None \
            else min(self.cfg.mpc_score_horizon, D)
        acts = torch.zeros((C, D, N_ACTIONS))
        acts[torch.arange(C)[:, None], torch.arange(D)[None, :],
             torch.as_tensor(seqs)] = 1.0
        obs = obs_vec.expand(C, 1, -1)                      # (C, 1, obs_dim)
        hh = None if h is None else h.expand(-1, C, -1).contiguous()
        mean_energy = torch.zeros(C)
        for t in range(kmax):
            pred, hh = core(obs, acts[:, t:t + 1, :], hh)   # (C, 1, obs_dim)
            obs = pred.clamp(0.0, 1.0)
            mean_energy += pred[:, 0, ENERGY_DIM]
        return mean_energy.numpy()

    @torch.no_grad()
    def plan(self, core: PredictiveCore, h: torch.Tensor | None,
             obs_vec: torch.Tensor) -> int:
        """Bir sonraki eylemi seçer.

        h: mevcut hidden (1, 1, H) veya None; obs_vec: (obs_dim,) float32.
        Not: h'yi İLERLETMEZ — gerçek gözlem geldiğinde eğitim yolu ilerletir.

        K-109 (S2.5 adım 4, teşhis: ilk-eylem seyreltmesi): açıksa 6
        sabit-eylem dizisi adaylara katılır ve elit-iyileştirme (CEM-lite)
        turları uygulanır. İçerik vermez: tüm eylemlere simetrik.
        """
        cfg = self.cfg
        C, D = cfg.mpc_candidates, cfg.mpc_horizon
        seqs = self.rng.integers(0, N_ACTIONS, size=(C, D))
        row = 0
        if cfg.mpc_constant_candidates:
            for a in range(N_ACTIONS):  # ilk 6 satır: sabit-eylem planları
                seqs[a, :] = a
            row = N_ACTIONS
        if cfg.mpc_macro_candidates:
            # K-111: yön×süre makro önekleri (kuyruk rastgele kalır —
            # içerik vermez, 4 yöne simetrik; "sonra ne" CEM'e bırakılır).
            from world.grid import DOWN, LEFT, RIGHT, UP
            for direction in (UP, DOWN, LEFT, RIGHT):
                for tau in range(1, D + 1):
                    if row >= C:
                        break
                    seqs[row, :tau] = direction
                    row += 1
        scores = self._score(core, h, obs_vec, seqs)
        for _ in range(cfg.mpc_cem_iters - 1):
            elite_idx = np.argsort(scores)[-cfg.mpc_elites:]
            elites = seqs[elite_idx]
            n_child = C - len(elites)
            children = elites[self.rng.integers(0, len(elites), size=n_child)]
            mut = self.rng.random((n_child, D)) < 0.3
            children = np.where(
                mut, self.rng.integers(0, N_ACTIONS, size=(n_child, D)),
                children)
            seqs = np.vstack([elites, children])
            scores = self._score(core, h, obs_vec, seqs)
        best = int(np.argmax(scores))
        return int(seqs[best, 0])
