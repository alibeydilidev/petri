"""Organ 2 — Homeostaz: tek skaler, enerji. Sıfırlanırsa ajan ölür.

Tur muhasebesi: sabit metabolizma + eylem maliyeti + (S3'te sinyal
maliyeti) + dünyadan gelen delta (hasat kazancı / tehlike emmesi).
"""

from agent.config import AgentConfig
from world.grid import INTERACT, STAY


class Homeostasis:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        self.energy = cfg.max_energy
        self.age = 0  # S3-D yuva dönemi için yaş (tur); T=0'da etkisiz

    @property
    def in_nest(self) -> bool:
        """Yuva dönemi (PL-22 b): yaş < nest_turns."""
        return self.age < self.cfg.nest_turns

    def cost_factor(self) -> float:
        return self.cfg.nest_factor if self.in_nest else 1.0

    @property
    def alive(self) -> bool:
        return self.energy > 0.0

    def action_cost(self, action: int) -> float:
        if action == STAY:
            return 0.0
        if action == INTERACT:
            return self.cfg.interact_energy_cost
        return self.cfg.move_energy_cost

    def apply_turn(self, action: int, world_delta: float,
                   signal_cost: float = 0.0) -> float:
        """Bir turun enerji muhasebesini uygular; yeni enerjiyi döndürür.

        signal_cost: bu tur gönderilen sinyalin bedeli (S3). Eskiden
        çağıranlar bunu world_delta'dan düşüyordu; yuva indirimi sinyali
        de kapsasın diye ayrı parametre. 0.0 → eski davranış bit-eş.
        Dünyadan gelen delta (hasat/tehlike) indirime GİRMEZ: yuva
        ajanın kendi maliyetlerini ucuzlatır, dünyayı değiştirmez.
        """
        f = self.cost_factor()
        self.energy += world_delta
        self.energy -= f * (self.cfg.base_metabolism
                            + self.action_cost(action) + signal_cost)
        self.energy = min(self.energy, self.cfg.max_energy)
        self.age += 1
        return self.energy
