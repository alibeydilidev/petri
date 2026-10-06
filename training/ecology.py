"""S3 ekolojisi — 5 heterojen ajan, kanal AÇIK, ölüm gerçek.

"Önce ekoloji nefes alsın" (Ali): probes/ sosyal katmanı KAPALI; bu
modül yalnız ekolojiyi koşturur ve DAVRANIŞSAL hayati değerleri loglar
(hayatta kalma, A-hasadı, B-açılışı, sinyal kullanım istatistiği).
Anayasa md.5 uyarınca bu loglardan hiçbir "anlıyor" iddiası türetilmez.

Sinyal seçimi: eylemle BİRLİKTE MPC aday dizisine girer (ortak
planlama); model kendi sinyalinin sonuçlarını efferens girdisi (K-114)
üzerinden öğrenebilir. Sabit-eylem adayları sinyalsizdir (tutumlu plan
her zaman havuzda). Ödül/şekillendirme YOK: sinyalin tek maliyeti
enerji (homeostaz), tek getirisi — varsa — modelin keşfedeceği dünya.

Kullanım: python3 -m training.ecology --turns 20000 --out runs/s3_breath
"""

import argparse
import dataclasses
import json
import pathlib
import time

import numpy as np
import torch

from agent.channel import NO_SIGNAL, N_SYMBOLS, own_signal_onehot, received_vector
from agent.homeostasis import Homeostasis
from agent.mpc import MPCPlanner
from population.lifecycle import successor, transplant_seed3
from population.roster import ROSTER, agent_cfg
from training.loop import OnlineAgent, encode_obs
from world.config import WorldConfig, config_hash
from world.grid import N_ACTIONS, World

WCFG = dataclasses.replace(WorldConfig(), resource_a_count=24)  # economy v3
SEED3 = "runs/s210_weights/seed3.pt"


class SocialPlanner(MPCPlanner):
    """Eylem+sinyal ortak planlaması. Aday: eylem dizisi (K-109/111
    şemasıyla) × sinyal dizisi (uniform 17; sabit-eylem satırları
    sinyalsiz). J değişmedi (K-103)."""

    @torch.no_grad()
    def plan_joint(self, core, h, obs_vec):
        cfg = self.cfg
        C, D = cfg.mpc_candidates, cfg.mpc_horizon
        seqs = self.rng.integers(0, N_ACTIONS, size=(C, D))
        sigs = self.rng.integers(-1, N_SYMBOLS, size=(C, D))
        row = 0
        if cfg.mpc_constant_candidates:
            for a in range(N_ACTIONS):
                seqs[a, :] = a
                sigs[a, :] = NO_SIGNAL
            row = N_ACTIONS
        if cfg.mpc_macro_candidates:
            from world.grid import DOWN, LEFT, RIGHT, UP
            for direction in (UP, DOWN, LEFT, RIGHT):
                for tau in range(1, D + 1):
                    if row >= C:
                        break
                    seqs[row, :tau] = direction
                    row += 1
        scores = self._score_joint(core, h, obs_vec, seqs, sigs)
        for _ in range(cfg.mpc_cem_iters - 1):
            elite_idx = np.argsort(scores)[-cfg.mpc_elites:]
            e_s, e_g = seqs[elite_idx], sigs[elite_idx]
            n_child = C - len(elite_idx)
            pick = self.rng.integers(0, len(elite_idx), size=n_child)
            cs, cg = e_s[pick].copy(), e_g[pick].copy()
            mut = self.rng.random((n_child, D)) < 0.3
            cs = np.where(mut, self.rng.integers(0, N_ACTIONS, cs.shape), cs)
            mutg = self.rng.random((n_child, D)) < 0.3
            cg = np.where(mutg, self.rng.integers(-1, N_SYMBOLS, cg.shape), cg)
            seqs = np.vstack([e_s, cs])
            sigs = np.vstack([e_g, cg])
            scores = self._score_joint(core, h, obs_vec, seqs, sigs)
        best = int(np.argmax(scores))
        return int(seqs[best, 0]), int(sigs[best, 0])

    @torch.no_grad()
    def _score_joint(self, core, h, obs_vec, seqs, sigs):
        C, D = seqs.shape
        kmax = D if self.cfg.mpc_score_horizon is None \
            else min(self.cfg.mpc_score_horizon, D)
        A = N_ACTIONS + N_SYMBOLS + 1
        acts = torch.zeros((C, D, A))
        acts[torch.arange(C)[:, None], torch.arange(D)[None, :],
             torch.as_tensor(seqs)] = 1.0
        sig_idx = torch.as_tensor(np.where(sigs < 0, 0, sigs + 1))
        acts[torch.arange(C)[:, None], torch.arange(D)[None, :],
             N_ACTIONS + sig_idx] = 1.0
        obs = obs_vec.expand(C, 1, -1)
        hh = None if h is None else h.expand(-1, C, -1).contiguous()
        mean_energy = torch.zeros(C)
        for t in range(kmax):
            pred, hh = core(obs, acts[:, t:t + 1, :], hh)
            obs = pred.clamp(0.0, 1.0)
            mean_energy += pred[:, 0, -1]
        return mean_energy.numpy()


class Ledger:
    """Nüfus ölçeğinde KÜMÜLATİF muhasebe (M-23: sayaç da bir cihazdır).

    Sayaçlar Citizen'da yaşar ve Citizen ölümde DEĞİŞTİRİLİR. S3 ilk
    nefes koşumunda vitals doğrudan o anki 5 sakinin yaşam-içi sayacını
    raporluyordu; signal_rate ise bu RESETLENEN payı KÜMÜLATİF paydaya
    (5*turn) bölüyordu. Sonuç yapay monoton düşüştü ve "sinyaller söndü"
    diye okundu (FINDINGS S3 ENSTRÜMAN ŞERHİ — çürütüldü: gerçek oran
    0.55 ve yükseliyordu).

    Bu defter ölen her sakinin sayacını devralır; oranlar AJAN-TURUNA
    bölünür. Kümülatif alanlar tanım gereği azalamaz — testte sabitlendi.
    """

    def __init__(self) -> None:
        self.agent_turns = 0
        self.deaths = 0
        self.harvests_a = 0
        self.b_shares = 0          # B payı alan ajan-olayı (açılış ≠ pay)
        self.signals_sent = 0
        self.symbol_hist = np.zeros(N_SYMBOLS, dtype=np.int64)
        self.lifespans: list[int] = []

    def retire(self, c: "Citizen", turn: int) -> None:
        """Ölen sakinin defterini nüfus toplamına devret."""
        self.deaths += 1
        self.harvests_a += c.harvests_a
        self.b_shares += c.b_shares
        self.signals_sent += c.signals_sent
        self.symbol_hist += c.symbol_hist
        self.lifespans.append(turn - c.birth_turn)

    def totals(self, living: list["Citizen"]) -> dict:
        """Ölenler + hâlâ yaşayanlar = gerçek kümülatif."""
        return {
            "a_harvests": self.harvests_a + sum(c.harvests_a for c in living),
            "b_shares": self.b_shares + sum(c.b_shares for c in living),
            "signals_sent": (self.signals_sent
                             + sum(c.signals_sent for c in living)),
        }


class Citizen:
    """Bir slotun canlı sakini: çekirdek + homeostaz + kimlik."""

    def __init__(self, slot: str, agent: OnlineAgent, gen: int,
                 parent: str | None, birth_turn: int):
        self.slot, self.agent, self.gen = slot, agent, gen
        self.id = f"{slot}.g{gen}"
        self.parent, self.birth_turn = parent, birth_turn
        self.homeo = Homeostasis(agent.cfg)
        self.planner = SocialPlanner(agent.cfg, agent.planner.rng)
        self.harvests_a, self.b_shares, self.signals_sent = 0, 0, 0
        self.symbol_hist = np.zeros(N_SYMBOLS, dtype=np.int64)
        self.last_obs = None

    def act(self, obs_vec):
        cfg = self.agent.cfg
        rng = self.planner.rng
        if rng.random() < cfg.mpc_epsilon:
            if cfg.eps_move_bias > 0 and rng.random() < cfg.eps_move_bias:
                a = int(rng.integers(1, 5))
            else:
                a = int(rng.integers(0, N_ACTIONS))
            s = int(rng.integers(-1, N_SYMBOLS))
            return a, s
        return self.planner.plan_joint(self.agent.core, self.agent.h, obs_vec)


def founding_population(turn: int = 0) -> list[Citizen]:
    cits = []
    for i, (slot, *_rest) in enumerate(ROSTER):
        cfg = agent_cfg(slot)
        if slot == "A2":  # DP-01 fiili: seed-3 miras + mutasyon
            agent = transplant_seed3(SEED3, cfg, torch_seed=1000 + i,
                                     np_seed=2000 + i)
            from population.lifecycle import MUTATION_SIGMA, mutate_
            mutate_(agent, MUTATION_SIGMA, np.random.default_rng(555_000 + i))
            parent = "seed3(S2.10)"
        else:
            agent = OnlineAgent(cfg, torch_seed=1000 + i, np_seed=2000 + i)
            parent = None
        cits.append(Citizen(slot, agent, gen=0, parent=parent,
                            birth_turn=turn))
    return cits


def run_ecology(turns: int, out_dir: str, world_seed: int = 3001,
                log_every: int = 1000) -> None:
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    world = World(WCFG, n_entities=5, seed=world_seed)
    cits = founding_population()
    genealogy = [{"id": c.id, "slot": c.slot, "parent": c.parent,
                  "birth_turn": 0} for c in cits]
    succ_rng = np.random.default_rng(777_001)   # yalnız mutasyon gürültüsü
    ledger = Ledger()
    vitals, prev = [], {"a_harvests": 0, "b_shares": 0, "signals_sent": 0,
                        "agent_turns": 0}
    t0 = time.perf_counter()

    for c in cits:  # ilk gözlemler
        heard = world.heard(cits.index(c), WCFG.signal_range)
        c.last_obs = encode_obs(world.observe(cits.index(c),
                                              c.agent.cfg.obs_radius),
                                c.homeo.energy, c.agent.cfg,
                                received_vector(heard))

    for turn in range(1, turns + 1):
        acts, sigs = [], []
        for c in cits:
            a, s = c.act(c.last_obs)
            acts.append(a)
            sigs.append(s)
        ledger.agent_turns += len(cits)
        deltas = world.step(np.array(acts), np.array(sigs))
        for i, c in enumerate(cits):
            cost_extra = (c.agent.cfg.signal_energy_cost
                          if sigs[i] != NO_SIGNAL else 0.0)
            c.homeo.apply_turn(acts[i], float(deltas[i]) - cost_extra)
            if deltas[i] > 0:
                # B payı 180/k (k=2→90, 3→60); A=45. k>=4 B payı A'ya eşit
                # düşer — bu delta-eşiği yaklaşıklığı yalnız PAYI ayırır;
                # açılış sayısı dünyanın kendi sayacından okunur
                # (world.b_openings_total), geri-çıkarımdan değil.
                if deltas[i] > WCFG.resource_a_energy + 1e-9:
                    c.b_shares += 1
                else:
                    c.harvests_a += 1
            if sigs[i] != NO_SIGNAL:
                c.signals_sent += 1
                c.symbol_hist[sigs[i]] += 1
            heard = world.heard(i, WCFG.signal_range)
            nxt = encode_obs(world.observe(i, c.agent.cfg.obs_radius),
                             max(c.homeo.energy, 0.0), c.agent.cfg,
                             received_vector(heard))
            act_vec = torch.cat([
                torch.eye(N_ACTIONS)[acts[i]],
                torch.from_numpy(own_signal_onehot(sigs[i]))])
            c.agent.learn_step_vec(c.last_obs, act_vec, nxt)
            c.last_obs = nxt
        # Ölüm gerçek + halef (DP-01b fiili)
        for i, c in enumerate(cits):
            if not c.homeo.alive:
                ledger.retire(c, turn)
                deaths = ledger.deaths
                child_agent = successor(
                    c.agent, c.agent.cfg,
                    torch_seed=10_000 + deaths, np_seed=20_000 + deaths,
                    rng=succ_rng)
                child = Citizen(c.slot, child_agent, gen=c.gen + 1,
                                parent=c.id, birth_turn=turn)
                # Yeni beden: doğum yeri DÜNYANIN rng'sinden (anayasa —
                # eski kod succ_rng kullanıyordu, bkz. World.respawn_entity).
                world.respawn_entity(i)
                heard = world.heard(i, WCFG.signal_range)
                child.last_obs = encode_obs(
                    world.observe(i, child.agent.cfg.obs_radius),
                    child.homeo.energy, child.agent.cfg,
                    received_vector(heard))
                cits[i] = child
                genealogy.append({"id": child.id, "slot": child.slot,
                                  "parent": child.parent,
                                  "birth_turn": turn})
        if turn % log_every == 0:
            tot = ledger.totals(cits)
            at = ledger.agent_turns
            d_at = at - prev["agent_turns"]

            def rate(key: str) -> float:
                """Pencere oranı: son log aralığındaki ajan-turu başına.
                Kümülatif ortalama trendi maskeler — asıl seyir budur."""
                return round((tot[key] - prev[key]) / max(d_at, 1), 4)

            v = {"turn": turn,
                 "energies": [round(c.homeo.energy, 1) for c in cits],
                 "gens": [c.gen for c in cits],
                 "deaths": ledger.deaths,
                 "agent_turns": at,
                 # --- kümülatif (ölümden sağ çıkar; azalamaz) ---
                 "a_harvests": tot["a_harvests"],
                 "b_shares": tot["b_shares"],
                 "b_openings": world.b_openings_total,
                 "signals_sent": tot["signals_sent"],
                 # --- oranlar: ajan-turu başına ---
                 "signal_rate": round(tot["signals_sent"] / max(at, 1), 4),
                 "signal_rate_window": rate("signals_sent"),
                 "harvest_rate_window": rate("a_harvests"),
                 "median_lifespan": (float(np.median(ledger.lifespans))
                                     if ledger.lifespans else None),
                 "ms_per_turn": round(1000 * (time.perf_counter() - t0)
                                      / turn, 1)}
            vitals.append(v)
            prev = {"a_harvests": tot["a_harvests"], "b_shares": tot["b_shares"],
                    "signals_sent": tot["signals_sent"], "agent_turns": at}
            print(f"[t={turn:>6}] ölüm {v['deaths']} (medyan ömür "
                  f"{v['median_lifespan']}) | nesil {v['gens']} | "
                  f"A-hasat {v['a_harvests']} | B-açılış {v['b_openings']} | "
                  f"sinyal/ajan-turu {v['signal_rate']} "
                  f"(pencere {v['signal_rate_window']}) | "
                  f"{v['ms_per_turn']} ms/tur", flush=True)

    tot = ledger.totals(cits)
    cum_hist = ledger.symbol_hist + sum(c.symbol_hist for c in cits)
    out = {"turns": turns, "world_seed": world_seed,
           "world": dataclasses.asdict(WCFG),
           "world_config_hash": config_hash(WCFG),
           "genealogy": genealogy, "deaths": ledger.deaths,
           "vitals": vitals,
           # Kümülatif nüfus defteri (M-23). final_symbol_hist yalnız o
           # anki sakinleri gösterir — sürekliliği bozmamak için duruyor,
           # ama analiz symbol_hist_cumulative'den okunur.
           "ledger": {"agent_turns": ledger.agent_turns, **tot,
                      "b_openings": world.b_openings_total,
                      "signal_rate": tot["signals_sent"]
                      / max(ledger.agent_turns, 1),
                      "lifespans": ledger.lifespans},
           "symbol_hist_cumulative": cum_hist.tolist(),
           "final_symbol_hist": {c.id: c.symbol_hist.tolist() for c in cits}}
    with open(pathlib.Path(out_dir) / "breath.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nyazıldı: {out_dir}/breath.json | toplam ölüm {ledger.deaths} | "
          f"soy kütüğü {len(genealogy)} kayıt | A-hasat {tot['a_harvests']} | "
          f"B-açılış {world.b_openings_total} | sinyal/ajan-turu "
          f"{tot['signals_sent'] / max(ledger.agent_turns, 1):.3f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=int, default=20_000)
    ap.add_argument("--out", default="runs/s3_breath")
    a = ap.parse_args()
    run_ecology(a.turns, a.out)


if __name__ == "__main__":
    main()
