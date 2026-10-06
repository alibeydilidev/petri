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

    @property
    def alive(self) -> bool:
        return self.energy > 0.0

    def action_cost(self, action: int) -> float:
        if action == STAY:
            return 0.0
        if action == INTERACT:
            return self.cfg.interact_energy_cost
        return self.cfg.move_energy_cost

    def apply_turn(self, action: int, world_delta: float) -> float:
        """Bir turun enerji muhasebesini uygular; yeni enerjiyi döndürür."""
        self.energy += world_delta
        self.energy -= self.cfg.base_metabolism + self.action_cost(action)
        self.energy = min(self.energy, self.cfg.max_energy)
        return self.energy
