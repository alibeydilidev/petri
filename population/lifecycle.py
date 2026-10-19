"""Doğum/ölüm + miras (DP-01 FİİLİ KARAR — S3 açılış talimatı):

Kurucu nüfus: A2 slotu seed-3 ağırlıklarını TRANSPLANT + mutasyonla
devralır (kanal-açık mimariye sıfır-nötr genişletme: yeni sinyal
sütunları 0 başlatılır — sinyalsiz girdide eski modelle bit-yakın
özdeşlik, test kanıtlı). Diğer slotlar mimari uyumsuzluğu nedeniyle
taze başlar (kısmi miras; soy kütüğüne dürüstçe işlenir).

Ölüm gerçek: ölen ajanın ağırlıkları biter; halef, ÖLENİN ağırlıklarının
mutasyonunu devralır (DP-01 seçenek-b, "çekirdek+miras" — fiili karar,
FINDINGS soy kütüğünde). Homeostaz/hidden/pencere sıfırdan.
"""

import copy

import numpy as np
import torch

from agent.config import AgentConfig
from training.loop import OnlineAgent

MUTATION_SIGMA = 0.01  # mutasyon gürültüsü (ağırlık başına gauss std)


def mutate_(agent: OnlineAgent, sigma: float,
            rng: np.random.Generator) -> None:
    """Yerinde mutasyon: tüm parametrelere N(0, sigma) eklenir.
    Determinizm: numpy rng'den örneklenir (torch global rng'ye dokunmaz)."""
    with torch.no_grad():
        for p in agent.core.parameters():
            noise = torch.from_numpy(
                rng.normal(0.0, sigma, size=tuple(p.shape)).astype("float32"))
            p.add_(noise)


def transplant_seed3(ckpt_path: str, cfg: AgentConfig, torch_seed: int,
                     np_seed: int) -> OnlineAgent:
    """Kanal-kapalı A2 (seed-3) ağırlıklarını kanal-açık A2 çekirdeğine
    nötr genişletmeyle taşır. Yeni girdi sütunları (alınan-sinyal 16 +
    sinyal-efferensi 17) ve yeni çıktı satırları (sinyal tahmini 16)
    SIFIR başlatılır → sinyalsiz ortamda davranış eski modele özdeş."""
    ckpt = torch.load(ckpt_path, weights_only=False)
    old = ckpt["state_dict"]
    agent = OnlineAgent(cfg, torch_seed=torch_seed, np_seed=np_seed)
    w = 2 * cfg.obs_radius + 1
    g = 4 * w * w                      # grid boyu (324)
    with torch.no_grad():
        sd = agent.core.state_dict()
        # GRU giriş matrisi sütun haritası:
        # eski x: [grid(g), enerji(1), eylem(6)]
        # yeni x: [grid(g), sinyal(16), enerji(1), eylem(6), sig-eff(17)]
        W_old, W_new = old["gru.weight_ih_l0"], sd["gru.weight_ih_l0"]
        W_new.zero_()
        W_new[:, :g] = W_old[:, :g]
        W_new[:, g + 16] = W_old[:, g]
        W_new[:, g + 17:g + 23] = W_old[:, g + 1:g + 7]
        sd["gru.weight_ih_l0"] = W_new
        for k in ("gru.weight_hh_l0", "gru.bias_ih_l0", "gru.bias_hh_l0",
                  "dec_proj.weight", "dec_proj.bias",
                  "dec_conv.0.weight", "dec_conv.0.bias",
                  "dec_conv.2.weight", "dec_conv.2.bias"):
            sd[k] = old[k]
        # dec_energy: eski (H,1) → yeni (H,17); enerji SON satır.
        sd["dec_energy.weight"].zero_()
        sd["dec_energy.weight"][-1] = old["dec_energy.weight"][0]
        sd["dec_energy.bias"].zero_()
        sd["dec_energy.bias"][-1] = old["dec_energy.bias"][0]
        agent.core.load_state_dict(sd)
    return agent


def transplant_seed3_ensemble(ckpt_path: str, cfg: AgentConfig,
                              torch_seed: int, np_seed: int):
    """A1: K üyeli topluluk; her üye seed-3 nötr transplantı. Üye 0 nötr
    (sinyal sütunları sıfır); üye k>0'ın EĞİTİLMEMİŞ sinyal sütunları
    N(0, ensemble_new_col_sigma) ile başlatılır → uyuşmazlık tam olarak
    hiç denenmemiş sinyal boyutunda doğar (M-29). Determinizm: numpy rng."""
    from training.ensemble_agent import EnsembleAgent
    agent = EnsembleAgent(cfg, torch_seed=torch_seed, np_seed=np_seed)
    rng = np.random.default_rng(np_seed + 909)
    w = 2 * cfg.obs_radius + 1
    g = 4 * w * w
    for k, member in enumerate(agent.core.members):
        tmp = transplant_seed3(ckpt_path, cfg, torch_seed=torch_seed, np_seed=np_seed)
        member.load_state_dict(tmp.core.state_dict())
        if k == 0:
            continue
        with torch.no_grad():
            sd = member.state_dict()
            sig = cfg.ensemble_new_col_sigma
            W = sd["gru.weight_ih_l0"]
            cols = list(range(g, g + 16)) + list(range(g + 23, g + 23 + 17))
            W[:, cols] = torch.from_numpy(
                rng.normal(0.0, sig, size=(W.shape[0], len(cols))).astype("float32"))
            De = sd["dec_energy.weight"]
            De[:-1] = torch.from_numpy(
                rng.normal(0.0, sig, size=tuple(De[:-1].shape)).astype("float32"))
            member.load_state_dict(sd)
    return agent


def successor(dead: OnlineAgent, cfg: AgentConfig, torch_seed: int,
              np_seed: int, rng: np.random.Generator,
              sigma: float = MUTATION_SIGMA,
              inherit_per: bool = False) -> OnlineAgent:
    """Halef: ölenin ağırlıkları + mutasyon (DP-01b fiili). Optimizer,
    PER tamponu, hidden SIFIRDAN (yaşantı miras alınmaz, yapı alınır).

    inherit_per=True (A2′, 2026-10-20): PER tamponu ve optimizer durumu da
    devralınır — ekolojide ömür ~40 tur olduğundan tampon her ölümde
    sıfırlanıyor ve karşı-olgusal tekrar (M-05 panzehiri) hiç
    çalışmıyordu. İçerik 0 bit; deneyci kararı (M-09). Hidden yine sıfır."""
    child = type(dead)(cfg, torch_seed=torch_seed, np_seed=np_seed)
    with torch.no_grad():
        child.core.load_state_dict(copy.deepcopy(dead.core.state_dict()))
    if inherit_per:
        if dead.per is not None:
            child.per = dead.per            # aynı tampon nesnesi, soy hattında sürer
        if dead.opt is not None and child.opt is not None:
            child.opt.load_state_dict(dead.opt.state_dict())
    mutate_(child, sigma, rng)
    return child
