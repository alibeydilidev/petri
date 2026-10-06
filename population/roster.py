"""Heterojen kadro (doküman 4.3). Etiketler ajanlara VERİLMEZ —
yalnız analiz sözlüğümüz."""

ROSTER = [
    # (slot, obs_radius, memory_dim, learning_rate, analiz etiketi)
    ("A0", 6, 64, 1e-3, "uzak görür, çabuk unutur, hızlı öğrenir"),
    ("A1", 3, 256, 1e-4, "kör ama fil hafızalı, yavaş öğrenir"),
    ("A2", 4, 128, 5e-4, "dengeli"),
    ("A3", 5, 96, 8e-4, "gözcü-ağırlıklı"),
    ("A4", 3, 192, 3e-4, "hafıza-ağırlıklı"),
]

# S3 ortak ayarları: S2.10 yığını + kanal açık. Metabolizma v2-dönem
# basıncı (0.6). lr roster'dan gelir.
COMMON = dict(base_metabolism=0.6, mpc_horizon=10,
              mpc_constant_candidates=True, mpc_cem_iters=2,
              mpc_candidates=64, mpc_macro_candidates=True,
              per_enabled=True, per_spatial_weight=4.0, eps_move_bias=0.5,
              decoder_type="conv", channel_open=True)
# Beyan: S2.10'a görece TEK hafifletme cem_iters 4→2 (5-ajan tur
# maliyeti; KERNEL_BUDGET S3 notu). Diğer her şey S2.9/S2.10 yığını.


def agent_cfg(slot: str):
    from agent.config import AgentConfig
    for s, r, m, lr, _ in ROSTER:
        if s == slot:
            return AgentConfig(obs_radius=r, memory_dim=m, learning_rate=lr,
                               **COMMON)
    raise KeyError(slot)
