"""Program A1 — model topluluğu (PL-12 c): K bağımsız başlatılmış tahmin
çekirdeği, aynı veriyle eğitilir; planlayıcı J = ortalama − β·uyuşmazlık.

Niçin: argmax planlayıcı, hiç/az denenmiş eylem boyutunu (sinyal) modelin
eğitimsiz sütunlarından gelen SAHTE primle seçiyor (S3-O/P/Q problları,
M-05, M-29). Topluluk uyuşmazlığı "bilmediğin yerde iddialı olma"
demenin içeriksiz yoludur: hangi sembolün/eylemin iyi olduğunu
söylemez, yalnız az görülmüş girdide kararsızlığı puana yansıtır.
KERNEL_BUDGET: K ve β birer hiperparametre (~2-3 bit; S3 kapanış A1).

Hidden durumu üye başına ayrı taşınır (liste). forward() ortalama tahmini
döndürür — tek-çekirdekli kodla uyum için; planlayıcı `members` ile üye
başına rollout yapar.
"""

import torch
import torch.nn as nn

from agent.config import AgentConfig
from agent.predictive_core import PredictiveCore


class EnsembleCore(nn.Module):
    def __init__(self, cfg: AgentConfig, k: int, torch_seed: int):
        super().__init__()
        self.cfg = cfg
        members = []
        for i in range(k):
            torch.manual_seed(torch_seed + 7919 * i)   # üye başına farklı init
            members.append(PredictiveCore(cfg))
        self.members = nn.ModuleList(members)
        self.obs_dim = self.members[0].obs_dim
        self.w = self.members[0].w

    @property
    def k(self) -> int:
        return len(self.members)

    def forward(self, obs, act_onehot, h=None):
        """h: None ya da K uzunluklu liste. Dönüş: (ortalama tahmin, hidden listesi)."""
        preds, hs = [], []
        for i, m in enumerate(self.members):
            p, hn = m(obs, act_onehot, None if h is None else h[i])
            preds.append(p)
            hs.append(hn)
        return torch.stack(preds).mean(0), hs

    def member_outputs(self, obs, act_onehot, h=None):
        """Üye başına (tahmin, hidden) — planlayıcı/öğrenme için."""
        return [m(obs, act_onehot, None if h is None else h[i])
                for i, m in enumerate(self.members)]

    def n_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


def detach_h(h):
    if h is None:
        return None
    return [x.detach() for x in h]


def clone_h(h):
    if h is None:
        return None
    return [x.detach().clone() for x in h]
