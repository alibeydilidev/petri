"""Organ 1 — Tahmin çekirdeği: küçük, nedensel, recurrent world-model.

Girdi: yerel gözlem + kendi son eylemi. (Alınan sinyaller S3'te eklenecek —
kanal S1'de KAPALI, girdi genişletmesi PL-08.)
Çıktı: sonraki gözlemin tahmini (enerji boyutu dahil).
Öğrenme sinyali: yalnız tahmin hatası (self-supervised). Ödül yok.

GRU tek yönlü → nedensellik oku ileri, gelecek sızıntısı yapısal olarak
imkânsız (test: tests/test_agent.py::test_causality).
Parametre bütçesi: < 500K (test eder).
"""

import hashlib

import torch
import torch.nn as nn

from agent.config import AgentConfig
from world.grid import N_ACTIONS


def obs_dim(cfg: AgentConfig) -> int:
    """Gözlem: 4 kanal x (2r+1)^2 grid [+ 16 alınan-sinyal] + 1 enerji.
    Enerji HEP son boyut (mpc.ENERGY_DIM)."""
    w = 2 * cfg.obs_radius + 1
    return 4 * w * w + (16 if cfg.channel_open else 0) + 1


def act_dim(cfg: AgentConfig) -> int:
    """Efferens girdisi: eylem one-hot(6) [+ kendi-sinyal one-hot(17)]."""
    return N_ACTIONS + (17 if cfg.channel_open else 0)


class PredictiveCore(nn.Module):
    def __init__(self, cfg: AgentConfig):
        super().__init__()
        self.cfg = cfg
        self.obs_dim = obs_dim(cfg)
        self.in_dim = self.obs_dim + act_dim(cfg)  # gözlem + efferens
        self.w = 2 * cfg.obs_radius + 1
        self.gru = nn.GRU(self.in_dim, cfg.memory_dim, batch_first=True)
        if cfg.decoder_type == "conv":
            # K-113: yerellik + ağırlık paylaşımı. Eylem girdisi YOK —
            # kayma bilgisi hidden'dan gelmek zorunda (kazanılacak şey).
            self.dec_proj = nn.Linear(cfg.memory_dim, 8 * self.w * self.w)
            self.dec_conv = nn.Sequential(
                nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(),
                nn.Conv2d(16, 4, 3, padding=1))
            # Grid-dışı boyutlar (kapalı: 1=enerji; açık: 16 sinyal+enerji).
            # Ad, seed3.pt uyumu için "dec_energy" kaldı.
            self.dec_energy = nn.Linear(cfg.memory_dim,
                                        self.obs_dim - 4 * self.w * self.w)
        else:
            self.decoder = nn.Linear(cfg.memory_dim, self.obs_dim)

    def forward(self, obs: torch.Tensor, act_onehot: torch.Tensor,
                h: torch.Tensor | None = None):
        """obs: (B, T, obs_dim), act_onehot: (B, T, 6) — t anındaki eylem.

        Dönüş: (B, T, obs_dim) sonraki-gözlem tahmini, son hidden (1, B, H).
        """
        x = torch.cat([obs, act_onehot], dim=-1)
        out, h_n = self.gru(x, h)
        if self.cfg.decoder_type == "conv":
            B, T, H = out.shape
            z = self.dec_proj(out).view(B * T, 8, self.w, self.w)
            grid = self.dec_conv(z).view(B, T, 4 * self.w * self.w)
            rest = self.dec_energy(out)  # kapalı: enerji; açık: sinyal+enerji
            return torch.cat([grid, rest], dim=-1), h_n
        return self.decoder(out), h_n

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def weight_hash(self) -> str:
        """Ağırlıkların SHA-256'sı — prob sızıntısı denetimi (Beş Kapı / KAPI 2)
        ve bit-eş eğitim tekrarı (KAPI 5) için."""
        m = hashlib.sha256()
        for name, p in sorted(self.state_dict().items()):
            m.update(name.encode())
            m.update(p.detach().cpu().contiguous().numpy().tobytes())
        return m.hexdigest()
