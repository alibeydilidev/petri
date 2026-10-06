"""S2.6 iş 1 — Fizibilite oracle'ı: scripted referans politika.

Ajan DEĞİLDİR; dünya kalibrasyonu ölçüm aletidir (KERNEL_BUDGET'a bit
yazmaz — ajana hiçbir şey vermez). Ajanla AYNI arayüzü kullanır: aynı
obs_radius'lu egosantrik gözlem, aynı eylem maliyetleri (run_episode
içindeki Homeostasis). Dünya durumuna Tanrı-gözü erişimi YOK.

Politika: görünür A-kaynağına aç-gözlü yürü (büyük eksen önce, kararlı
eşitlik bozumu), kaynağın üstündeyse INTERACT; hiçbiri görünmüyorsa
lawnmower taraması (64 adım doğu → 2r+1 adım güney → tekrar). Görünür
tehlike hücresine adım atmaktan tek-alternatifli kaçınma.
"""

import numpy as np

from world.grid import DOWN, INTERACT, LEFT, RIGHT, UP

_DELTA = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


class OraclePolicy:
    def __init__(self, obs_radius: int, grid_size: int = 64, scan: bool = True):
        """scan=False → görünür-A oracle'ı (S2.7 iş 1): kaynak görünürse
        yaklaş/hasat et, görünmüyorsa STAY (tarama yok). Saf fırsatçılığın
        tavanını ölçer."""
        self.r = obs_radius
        self.grid = grid_size
        self.scan = scan
        self.reset()

    def reset(self) -> None:
        self._east = 0
        self._down_left = 0

    def act_grid(self, obs: np.ndarray) -> int:
        r = self.r
        res = np.argwhere(obs[0] > 0.5)
        if len(res):
            d = np.abs(res - r).max(axis=1)          # Chebyshev
            order = np.lexsort((res[:, 1], res[:, 0], d))  # kararlı sıralama
            ty, tx = int(res[order[0]][0]), int(res[order[0]][1])
            if ty == r and tx == r:
                return INTERACT
            dy, dx = ty - r, tx - r
            if abs(dy) >= abs(dx) and dy != 0:
                step = UP if dy < 0 else DOWN
                alts = ([LEFT if dx < 0 else RIGHT] if dx != 0
                        else [LEFT, RIGHT])          # eksen-üstü: dik sap
            else:
                step = LEFT if dx < 0 else RIGHT
                alts = ([UP if dy < 0 else DOWN] if dy != 0
                        else [UP, DOWN])
            return self._avoid_hazard(obs, step, alts)
        # Kaynak görünmüyor.
        if not self.scan:
            from world.grid import STAY
            return STAY
        # Tarama modu (lawnmower).
        if self._down_left > 0:
            self._down_left -= 1
            return self._avoid_hazard(obs, DOWN, [RIGHT])
        self._east += 1
        if self._east >= self.grid:
            self._east = 0
            self._down_left = 2 * self.r  # bu turdaki DOWN + kalanlar = şerit
            return self._avoid_hazard(obs, DOWN, [RIGHT])
        return self._avoid_hazard(obs, RIGHT, [DOWN])

    def _avoid_hazard(self, obs: np.ndarray, step: int, alts: list[int]) -> int:
        y, x = self.r + _DELTA[step][0], self.r + _DELTA[step][1]
        if obs[2, y, x] <= 0.5:
            return step
        for alt in alts:
            y2, x2 = self.r + _DELTA[alt][0], self.r + _DELTA[alt][1]
            if obs[2, y2, x2] <= 0.5:
                return alt
        return step
