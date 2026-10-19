"""S3 ekolojisi — 5 ajan, kanal AÇIK, ölüm gerçek.

"Önce ekoloji nefes alsın" (Ali): probes/ sosyal katmanı KAPALI; bu
modül yalnız ekolojiyi koşturur ve DAVRANIŞSAL hayati değerleri loglar
(hayatta kalma, A-hasadı, B-açılışı, sinyal kullanım istatistiği, S3-E
ile olay isabeti ve sinyal-ipucu olumsallığı). Anayasa md.5 uyarınca
bu loglardan hiçbir "anlıyor" iddiası türetilmez.

Sinyal seçimi: eylemle BİRLİKTE MPC aday dizisine girer (ortak
planlama); model kendi sinyalinin sonuçlarını efferens girdisi (K-114)
üzerinden öğrenebilir. Sabit-eylem adayları sinyalsizdir (tutumlu plan
her zaman havuzda). Ödül/şekillendirme YOK: sinyalin tek maliyeti
enerji (homeostaz), tek getirisi — varsa — modelin keşfedeceği dünya.

S3-E (PL-30, 2026-10-18 — Ali kararı PL-22 c+b):
  --founding clone   : kurucu kadronun 5 slotu da seed-3 transplantı
                       (A2 mimarisi, mutasyonsuz; halefler σ=0.01).
  --nest T f         : yuva dönemi (AgentConfig.nest_turns/nest_factor).
  --events           : S3-C asimetrik olay görevi (event_every=30,
                       lead 8, süre 1, ceza 25, K=4 — oracle kalibrasyonu).
  --channel mute     : kontrol kolu; kanal fiziksel açık (obs_dim aynı)
                       ama sinyal gönderilmez/duyulmaz (MutePlanner).
Varsayılanlar S3 ilk-nefes kadrosunu (roster + A2 transplant) korur.
NOT: sinyal maliyeti artık Homeostasis.apply_turn(signal_cost=) yoluyla
düşülür (yuva kapsasın diye); f=1'de kayan-nokta sırası değiştiğinden
eski breath.json'larla bit-eş DEĞİLDİR (beyan, PL-30).

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
from agent.config import AgentConfig as AgentConfigFromDict_
from agent.homeostasis import Homeostasis


def AgentConfigFromDict(d: dict):
    return AgentConfigFromDict_(**d)
from agent.mpc import MPCPlanner
from population.lifecycle import successor, transplant_seed3
from population.roster import ROSTER, agent_cfg
from training.loop import OnlineAgent, encode_obs
from world.config import WorldConfig, config_hash
from world.grid import N_ACTIONS, World

WCFG = dataclasses.replace(WorldConfig(), resource_a_count=24)  # economy v3
# S3-C olay kalibrasyonu (runs/s3c_event_oracle.json ile aynı değerler)
EVENT_KW = dict(event_every=30, event_lead=8, event_duration=1,
                event_penalty=25.0, event_polarities=4)
SEED3 = "runs/s210_weights/seed3.pt"
NEST_TAIL = 60   # PL-29: "yuva-sonu uçurumu" penceresi (tur)


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
        frac = getattr(cfg, "mpc_signal_candidate_frac", 1.0)
        if frac < 1.0:   # S3-O: satırların (1-frac) kısmı sinyalsiz
            quiet = self.rng.random(C) >= frac
            sigs[quiet, :] = NO_SIGNAL
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
            if frac < 1.0:
                quiet = self.rng.random(n_child) >= frac
                cg[quiet, :] = NO_SIGNAL
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
        members = getattr(core, "members", None)
        if members is None:   # tek çekirdek (S0…S3 yolu, bit-eş)
            return self._rollout(core, h, obs_vec, acts, C, kmax).numpy()
        # Program A1: üye başına rollout; J = ortalama − β·std (uyuşmazlık
        # cezası). İçerik vermez: az görülmüş girdide kararsızlık puana
        # yansır. β=0 → saf topluluk ortalaması.
        E = torch.stack([self._rollout(m, None if h is None else h[k],
                                       obs_vec, acts, C, kmax)
                         for k, m in enumerate(members)])          # (K, C)
        beta = float(getattr(self.cfg, "mpc_ensemble_beta", 0.0))
        score = E.mean(0) - beta * E.std(0, unbiased=False)
        return score.numpy()

    @torch.no_grad()
    def _rollout(self, core, h, obs_vec, acts, C, kmax):
        obs = obs_vec.expand(C, 1, -1)
        hh = None if h is None else h.expand(-1, C, -1).contiguous()
        mean_energy = torch.zeros(C)
        for t in range(kmax):
            pred, hh = core(obs, acts[:, t:t + 1, :], hh)
            obs = pred.clamp(0.0, 1.0)
            mean_energy += pred[:, 0, -1]
        return mean_energy


class MutePlanner(SocialPlanner):
    """Kanal-açık çekirdekle EYLEM-ONLY planlama (S3-D/S3-E kontrol
    kolu): aday geometrisi SocialPlanner ile aynı (sabit + makro + CEM),
    sinyal her yerde YOK. Böylece kanal farkı izole edilir (M-06)."""

    @torch.no_grad()
    def plan_joint(self, core, h, obs_vec):
        cfg = self.cfg
        C, D = cfg.mpc_candidates, cfg.mpc_horizon
        seqs = self.rng.integers(0, N_ACTIONS, size=(C, D))
        sigs = np.full((C, D), NO_SIGNAL, dtype=np.int64)
        row = 0
        if cfg.mpc_constant_candidates:
            for a in range(N_ACTIONS):
                seqs[a, :] = a
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
            e_s = seqs[elite_idx]
            n_child = C - len(elite_idx)
            cs = e_s[self.rng.integers(0, len(elite_idx), size=n_child)].copy()
            mut = self.rng.random((n_child, D)) < 0.3
            cs = np.where(mut, self.rng.integers(0, N_ACTIONS, cs.shape), cs)
            seqs = np.vstack([e_s, cs])
            sigs = np.full((C, D), NO_SIGNAL, dtype=np.int64)
            scores = self._score_joint(core, h, obs_vec, seqs, sigs)
        best = int(np.argmax(scores))
        return int(seqs[best, 0]), NO_SIGNAL


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
    S3-E ek alanları (olay isabeti, sinyal-ipucu tablosu, PL-29 ölüm
    sınıfları) aynı disiplinle kümülatiftir.
    """

    # Citizen'dan devralınan skaler sayaçlar
    SCALARS = ("harvests_a", "b_shares", "signals_sent",
               "event_turns", "event_hits", "pending_turns",
               "pending_signals", "heard_in_window_turns",
               "event_turns_heard", "event_hits_heard",
               "event_own_consistent", "event_stay", "event_protected")

    def __init__(self) -> None:
        self.agent_turns = 0
        self.deaths = 0
        for k in self.SCALARS:
            setattr(self, k, 0)
        self.symbol_hist = np.zeros(N_SYMBOLS, dtype=np.int64)
        # Sinyal-ipucu olumsallığı: [ipucu (bit_idx*2+bit_val) 0..3][sembol]
        # yalnız uyarı penceresinde gönderilen sinyaller.
        self.cue_symbol = np.zeros((4, N_SYMBOLS), dtype=np.int64)
        self.lifespans: list[int] = []
        # PL-29: ölüm sınıfları
        self.deaths_in_nest = 0
        self.deaths_nest_tail = 0

    def retire(self, c: "Citizen", turn: int) -> None:
        """Ölen sakinin defterini nüfus toplamına devret."""
        self.deaths += 1
        for k in self.SCALARS:
            setattr(self, k, getattr(self, k) + getattr(c, k))
        self.symbol_hist += c.symbol_hist
        self.cue_symbol += c.cue_symbol
        age = turn - c.birth_turn
        self.lifespans.append(age)
        T = c.agent.cfg.nest_turns
        if T > 0:
            if age <= T:
                self.deaths_in_nest += 1
            elif age <= T + NEST_TAIL:
                self.deaths_nest_tail += 1

    def totals(self, living: list["Citizen"]) -> dict:
        """Ölenler + hâlâ yaşayanlar = gerçek kümülatif."""
        return {k: getattr(self, k) + sum(getattr(c, k) for c in living)
                for k in self.SCALARS}


class Citizen:
    """Bir slotun canlı sakini: çekirdek + homeostaz + kimlik."""

    def __init__(self, slot: str, agent: OnlineAgent, gen: int,
                 parent: str | None, birth_turn: int, mute: bool = False,
                 channel: str | None = None):
        """channel: "open" (konuş+duy), "mute" (ikisi de yok), "hear"
        (yalnız duy — S3-L), "speak" (yalnız konuş — S3-L). mute=True
        eski çağrılarla uyum için "mute" demektir."""
        self.slot, self.agent, self.gen = slot, agent, gen
        self.id = f"{slot}.g{gen}"
        self.parent, self.birth_turn = parent, birth_turn
        mode = channel or ("mute" if mute else "open")
        self.channel_mode = mode
        self.can_send = mode in ("open", "speak")
        self.can_hear = mode in ("open", "hear")
        self.mute = not self.can_send
        self.homeo = Homeostasis(agent.cfg)
        P = SocialPlanner if self.can_send else MutePlanner
        self.planner = P(agent.cfg, agent.planner.rng)
        for k in Ledger.SCALARS:
            setattr(self, k, 0)
        self.symbol_hist = np.zeros(N_SYMBOLS, dtype=np.int64)
        self.cue_symbol = np.zeros((4, N_SYMBOLS), dtype=np.int64)
        self.heard_in_window = False   # bu uyarı penceresinde bir şey duydu mu
        self.last_obs = None

    def act(self, obs_vec):
        cfg = self.agent.cfg
        rng = self.planner.rng
        if rng.random() < cfg.mpc_epsilon:
            if cfg.eps_move_bias > 0 and rng.random() < cfg.eps_move_bias:
                a = int(rng.integers(1, 5))
            else:
                a = int(rng.integers(0, N_ACTIONS))
            if not self.can_send:
                s = NO_SIGNAL
            elif cfg.eps_signal_quiet_prob > 0.0 and \
                    rng.random() < cfg.eps_signal_quiet_prob:
                s = NO_SIGNAL                      # S3-P: dengeli susma
            else:
                s = int(rng.integers(-1, N_SYMBOLS))
            return a, s
        return self.planner.plan_joint(self.agent.core, self.agent.h, obs_vec)


def founding_population(turn: int = 0, founding: str = "roster",
                        nest: tuple[int, float] = (0, 1.0),
                        mute: bool = False,
                        channel: str | None = None,
                        signal_candidate_frac: float | None = None,
                        eps_signal_quiet: float | None = None,
                        ensemble: tuple[int, float] | None = None
                        ) -> list[Citizen]:
    cits = []
    extra = {}
    if signal_candidate_frac is not None:
        extra["mpc_signal_candidate_frac"] = float(signal_candidate_frac)
    if eps_signal_quiet is not None:
        extra["eps_signal_quiet_prob"] = float(eps_signal_quiet)
    if ensemble is not None:
        extra["ensemble_k"] = int(ensemble[0])
        extra["mpc_ensemble_beta"] = float(ensemble[1])
    if founding.startswith("weights:"):
        # S3-Q (Program B): kurucu kadro, önceki koşumun final_weights.pt
        # dosyasındaki 5 çekirdek (kademeli kanal: önce kanal-kapalı
        # öğren, sonra aynı ağırlıklarla kanalı aç). Config'in gözlem
        # boyutları aynı (kanal fiziksel olarak hep açık); yuva/arama
        # parametreleri bu koşumun ayarlarıyla EZİLİR (deneyci kararı).
        ck = torch.load(founding.split(":", 1)[1], weights_only=False)
        cits = []
        for i, (slot, *_rest) in enumerate(ROSTER):
            entry = ck[slot]
            cfg = dataclasses.replace(AgentConfigFromDict(entry["cfg"]),
                                      nest_turns=nest[0], nest_factor=nest[1],
                                      **extra)
            agent = OnlineAgent(cfg, torch_seed=1000 + i, np_seed=2000 + i)
            agent.core.load_state_dict(entry["state_dict"])
            cits.append(Citizen(slot, agent, gen=0,
                                parent=f"{entry['id']}@{founding}",
                                birth_turn=turn, mute=mute, channel=channel))
        return cits
    for i, (slot, *_rest) in enumerate(ROSTER):
        if founding == "clone":
            # PL-22 (c): tüm slotlar seed-3 transplantı, A2 mimarisi,
            # kurucu mutasyon YOK (çeşitlilik halefiyetle, σ=0.01).
            cfg = dataclasses.replace(agent_cfg("A2"), nest_turns=nest[0],
                                      nest_factor=nest[1], **extra)
            if cfg.ensemble_k > 1:   # Program A1
                from population.lifecycle import transplant_seed3_ensemble
                agent = transplant_seed3_ensemble(SEED3, cfg, torch_seed=1000 + i,
                                                  np_seed=2000 + i)
            else:
                agent = transplant_seed3(SEED3, cfg, torch_seed=1000 + i,
                                         np_seed=2000 + i)
            parent = "seed3(S2.10)"
        else:
            cfg = dataclasses.replace(agent_cfg(slot), nest_turns=nest[0],
                                      nest_factor=nest[1], **extra)
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
                            birth_turn=turn, mute=mute, channel=channel))
    return cits


def _observe(world: World, i: int, c: Citizen, energy: float):
    heard = world.heard(i, world.cfg.signal_range) if c.can_hear else []
    if heard and world.events.pending(world.turn):
        c.heard_in_window = True
    return encode_obs(world.observe(i, c.agent.cfg.obs_radius), energy,
                      c.agent.cfg, received_vector(heard))


def run_ecology(turns: int, out_dir: str, world_seed: int = 3001,
                log_every: int = 1000, founding: str = "roster",
                nest: tuple[int, float] = (0, 1.0), events: bool = False,
                channel: str = "open",
                mutation_sigma: float | None = None,
                event_penalty: float | None = None,
                save_weights: bool = True, event_every: int | None = None,
                selection: str = "none",
                event_lead: int | None = None,
                event_share: float | None = None,
                signal_candidate_frac: float | None = None,
                eps_signal_quiet: float | None = None,
                ensemble: tuple[int, float] | None = None,
                event_min_safe: int | None = None,
                inherit_per: bool = False) -> None:
    """mutation_sigma: halef mutasyonu σ (None → lifecycle.MUTATION_SIGMA
    =0.01). S3-F drift merdiveni için parametrik; 0.0 = saf miras."""
    from population.lifecycle import MUTATION_SIGMA
    sigma = MUTATION_SIGMA if mutation_sigma is None else float(mutation_sigma)
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    wcfg = dataclasses.replace(WCFG, **EVENT_KW) if events else WCFG
    if events and event_penalty is not None:   # S3-G doz kalibrasyonu
        wcfg = dataclasses.replace(wcfg, event_penalty=float(event_penalty))
    if events and event_every is not None:     # S3-H sıklık (M-14 deneyim)
        wcfg = dataclasses.replace(wcfg, event_every=int(event_every))
    if events and event_lead is not None:      # S3-I uyarı penceresi (0 bit)
        wcfg = dataclasses.replace(wcfg, event_lead=int(event_lead))
    if events and event_share is not None:     # S3-N paylaşılan kayıp (PL-33)
        wcfg = dataclasses.replace(wcfg, event_share=float(event_share))
    if events and event_min_safe is not None:  # Program C sığınak
        wcfg = dataclasses.replace(wcfg, event_min_safe=int(event_min_safe))
    if selection not in ("none", "max_age"):
        raise ValueError(selection)
    if channel not in ("open", "mute", "hear", "speak"):
        raise ValueError(channel)
    mute = channel == "mute"
    world = World(wcfg, n_entities=5, seed=world_seed)
    cits = founding_population(founding=founding, nest=nest, mute=mute,
                               channel=channel,
                               signal_candidate_frac=signal_candidate_frac,
                               eps_signal_quiet=eps_signal_quiet,
                               ensemble=ensemble)
    genealogy = [{"id": c.id, "slot": c.slot, "parent": c.parent,
                  "birth_turn": 0} for c in cits]
    succ_rng = np.random.default_rng(777_001)   # yalnız mutasyon gürültüsü
    ledger = Ledger()
    vitals, prev = [], {k: 0 for k in Ledger.SCALARS}
    prev["agent_turns"] = 0
    t0 = time.perf_counter()

    for i, c in enumerate(cits):  # ilk gözlemler
        c.last_obs = _observe(world, i, c, c.homeo.energy)

    for turn in range(1, turns + 1):
        ev = world.events
        pending_now = ev.pending(world.turn)            # öncü gözlemde
        will_be_active = ev.active(world.turn + 1)      # eylem bu turda sınanır
        safe = ev.safe_action() if will_be_active else None
        min_safe = int(getattr(wcfg, "event_min_safe", 0))
        acts, sigs = [], []
        for c in cits:
            a, s = c.act(c.last_obs)
            acts.append(a)
            sigs.append(s)
        ledger.agent_turns += len(cits)
        n_safe = sum(1 for a in acts if a == safe) if will_be_active else 0
        deltas = world.step(np.array(acts), np.array(sigs))
        for i, c in enumerate(cits):
            sc = c.agent.cfg.signal_energy_cost if sigs[i] != NO_SIGNAL else 0.0
            c.homeo.apply_turn(acts[i], float(deltas[i]), signal_cost=sc)
            if deltas[i] > 0:
                # B payı 180/k (k=2→90, 3→60); A=45. k>=4 B payı A'ya eşit
                # düşer — bu delta-eşiği yaklaşıklığı yalnız PAYI ayırır;
                # açılış sayısı dünyanın kendi sayacından okunur
                # (world.b_openings_total), geri-çıkarımdan değil.
                if deltas[i] > wcfg.resource_a_energy + 1e-9:
                    c.b_shares += 1
                else:
                    c.harvests_a += 1
            if sigs[i] != NO_SIGNAL:
                c.signals_sent += 1
                c.symbol_hist[sigs[i]] += 1
            # --- S3-E gözlemci sayaçları (ajana gitmez) ---
            if pending_now:
                c.pending_turns += 1
                if sigs[i] != NO_SIGNAL:
                    c.pending_signals += 1
                    cue = ev.cue_for(i)
                    if cue is not None:
                        c.cue_symbol[2 * cue[0] + cue[1], sigs[i]] += 1
            if will_be_active:
                c.event_turns += 1
                hit = acts[i] == safe
                if hit:
                    c.event_hits += 1
                # Teşhis: eylem kendi ipucunun aday kümesinde mi (şans 0.5 —
                # "kendi bitini okuyor mu"); STAY payı (M-25 kaçış yolu i).
                if acts[i] in ev.candidates(i):
                    c.event_own_consistent += 1
                if acts[i] == 0:
                    c.event_stay += 1
                # Program C: korunma = doğru eylem VE sığınak açıldı (≥N)
                if hit and (min_safe == 0 or n_safe >= min_safe):
                    c.event_protected += 1
                if c.heard_in_window:
                    c.event_turns_heard += 1
                    if hit:
                        c.event_hits_heard += 1
                c.heard_in_window = False      # pencere kapandı
            heard_before = c.heard_in_window
            nxt = _observe(world, i, c, max(c.homeo.energy, 0.0))
            if c.heard_in_window and not heard_before:
                c.heard_in_window_turns += 1
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
                # S3-H seçilim (PL-22 a): halef, ölenin değil YAŞAYANLAR
                # arasında en uzun süredir hayatta olanın ağırlıklarından
                # türer (en uzun yaşayan soy çoğalır). Ajana bit gitmez;
                # nüfus kuralıdır (M-09). "none": DP-01b (ölenin tortusu).
                parent_c = c
                if selection == "max_age":
                    living = [x for x in cits if x.homeo.alive]
                    if living:
                        parent_c = max(living, key=lambda x: (turn - x.birth_turn,
                                                             -cits.index(x)))
                child_agent = successor(
                    parent_c.agent, c.agent.cfg,
                    torch_seed=10_000 + deaths, np_seed=20_000 + deaths,
                    rng=succ_rng, sigma=sigma, inherit_per=inherit_per)
                child = Citizen(c.slot, child_agent, gen=c.gen + 1,
                                parent=parent_c.id, birth_turn=turn, mute=mute,
                                channel=channel)
                # Yeni beden: doğum yeri DÜNYANIN rng'sinden (anayasa —
                # eski kod succ_rng kullanıyordu, bkz. World.respawn_entity).
                world.respawn_entity(i)
                child.last_obs = _observe(world, i, child, child.homeo.energy)
                cits[i] = child
                genealogy.append({"id": child.id, "slot": child.slot,
                                  "parent": child.parent,
                                  "birth_turn": turn})
        if turn % log_every == 0:
            tot = ledger.totals(cits)
            at = ledger.agent_turns
            d_at = at - prev["agent_turns"]

            def rate(key: str, denom_key: str | None = None) -> float | None:
                """Pencere oranı: son log aralığındaki ajan-turu (ya da
                verilen payda) başına. Kümülatif ortalama trendi maskeler."""
                num = tot[key] - prev[key]
                den = d_at if denom_key is None else tot[denom_key] - prev[denom_key]
                return round(num / den, 4) if den else None

            v = {"turn": turn,
                 "energies": [round(c.homeo.energy, 1) for c in cits],
                 "gens": [c.gen for c in cits],
                 "deaths": ledger.deaths,
                 "agent_turns": at,
                 # --- kümülatif (ölümden sağ çıkar; azalamaz) ---
                 "a_harvests": tot["harvests_a"],
                 "b_shares": tot["b_shares"],
                 "b_openings": world.b_openings_total,
                 "signals_sent": tot["signals_sent"],
                 "event_turns": tot["event_turns"],
                 "event_hits": tot["event_hits"],
                 "deaths_in_nest": ledger.deaths_in_nest,
                 "deaths_nest_tail": ledger.deaths_nest_tail,
                 # --- oranlar ---
                 "signal_rate": round(tot["signals_sent"] / max(at, 1), 4),
                 "signal_rate_window": rate("signals_sent"),
                 "harvest_rate_window": rate("harvests_a"),
                 "event_hit_rate_window": rate("event_hits", "event_turns"),
                 "own_cue_rate_window": rate("event_own_consistent",
                                             "event_turns"),
                 "event_stay_share_window": rate("event_stay", "event_turns"),
                 "event_protected_rate_window": rate("event_protected",
                                                     "event_turns"),
                 "pending_signal_rate_window": rate("pending_signals",
                                                    "pending_turns"),
                 "median_lifespan": (float(np.median(ledger.lifespans))
                                     if ledger.lifespans else None),
                 "ms_per_turn": round(1000 * (time.perf_counter() - t0)
                                      / turn, 1)}
            vitals.append(v)
            prev = {**tot, "agent_turns": at}
            print(f"[t={turn:>6}] ölüm {v['deaths']} (medyan ömür "
                  f"{v['median_lifespan']}) | nesil {v['gens']} | "
                  f"A-hasat {v['a_harvests']} | olay isabet(pencere) "
                  f"{v['event_hit_rate_window']} | sinyal/ajan-turu "
                  f"{v['signal_rate']} (pencere {v['signal_rate_window']}) | "
                  f"{v['ms_per_turn']} ms/tur", flush=True)

    tot = ledger.totals(cits)
    cum_hist = ledger.symbol_hist + sum(c.symbol_hist for c in cits)
    cue_sym = ledger.cue_symbol + sum(c.cue_symbol for c in cits)
    out = {"turns": turns, "world_seed": world_seed,
           "arm": {"founding": founding, "nest": list(nest),
                   "events": events, "channel": channel,
                   "mutation_sigma": sigma, "selection": selection,
                   "event_every": wcfg.event_every,
                   "event_penalty": wcfg.event_penalty,
                   "event_lead": wcfg.event_lead,
                   "event_share": wcfg.event_share,
                   "event_min_safe": wcfg.event_min_safe,
                   "inherit_per": inherit_per,
                   "signal_candidate_frac": cits[0].agent.cfg.mpc_signal_candidate_frac,
                   "eps_signal_quiet": cits[0].agent.cfg.eps_signal_quiet_prob,
                   "ensemble_k": cits[0].agent.cfg.ensemble_k,
                   "ensemble_beta": cits[0].agent.cfg.mpc_ensemble_beta},
           "world": dataclasses.asdict(wcfg),
           "world_config_hash": config_hash(wcfg),
           "genealogy": genealogy, "deaths": ledger.deaths,
           "vitals": vitals,
           # Kümülatif nüfus defteri (M-23). final_symbol_hist yalnız o
           # anki sakinleri gösterir — sürekliliği bozmamak için duruyor,
           # ama analiz symbol_hist_cumulative'den okunur.
           "ledger": {"agent_turns": ledger.agent_turns, **tot,
                      "a_harvests": tot["harvests_a"],
                      "b_openings": world.b_openings_total,
                      "signal_rate": tot["signals_sent"]
                      / max(ledger.agent_turns, 1),
                      "event_hit_rate": (tot["event_hits"] / tot["event_turns"]
                                         if tot["event_turns"] else None),
                      "deaths_in_nest": ledger.deaths_in_nest,
                      "deaths_nest_tail": ledger.deaths_nest_tail,
                      "lifespans": ledger.lifespans},
           "symbol_hist_cumulative": cum_hist.tolist(),
           "cue_symbol_cumulative": cue_sym.tolist(),
           "final_symbol_hist": {c.id: c.symbol_hist.tolist() for c in cits}}
    with open(pathlib.Path(out_dir) / "breath.json", "w") as f:
        json.dump(out, f, indent=2)
    if save_weights:   # son sakinlerin çekirdekleri (sonraki problar için)
        def _entry(c):
            e = {"id": c.id, "gen": c.gen, "cfg": dataclasses.asdict(c.agent.cfg)}
            members = getattr(c.agent.core, "members", None)
            if members is None:
                e["state_dict"] = c.agent.core.state_dict()
            else:   # A1: üye 0 tek-çekirdek problar için, tamamı ayrıca
                e["state_dict"] = members[0].state_dict()
                e["ensemble_state_dict"] = c.agent.core.state_dict()
            return e
        torch.save({c.slot: _entry(c) for c in cits},
                   pathlib.Path(out_dir) / "final_weights.pt")
    print(f"\nyazıldı: {out_dir}/breath.json | toplam ölüm {ledger.deaths} | "
          f"soy kütüğü {len(genealogy)} kayıt | A-hasat {tot['harvests_a']} | "
          f"B-açılış {world.b_openings_total} | olay isabet "
          f"{out['ledger']['event_hit_rate']} | sinyal/ajan-turu "
          f"{tot['signals_sent'] / max(ledger.agent_turns, 1):.3f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=int, default=20_000)
    ap.add_argument("--out", default="runs/s3_breath")
    ap.add_argument("--world-seed", type=int, default=3001)
    ap.add_argument("--log-every", type=int, default=1000)
    ap.add_argument("--founding", default="roster",
                    help="roster | clone | weights:<final_weights.pt>")
    ap.add_argument("--nest", type=float, nargs=2, default=(0, 1.0),
                    metavar=("T", "F"))
    ap.add_argument("--events", action="store_true")
    ap.add_argument("--channel", choices=["open", "mute", "hear", "speak"],
                    default="open")
    ap.add_argument("--sigma", type=float, default=None,
                    help="halef mutasyonu σ (varsayılan 0.01)")
    ap.add_argument("--event-penalty", type=float, default=None,
                    help="olay cezası (varsayılan EVENT_KW 25)")
    ap.add_argument("--event-every", type=int, default=None,
                    help="olay periyodu (varsayılan 30)")
    ap.add_argument("--selection", choices=["none", "max_age"], default="none")
    ap.add_argument("--event-lead", type=int, default=None,
                    help="öncü ile olay arası tur (varsayılan 8)")
    ap.add_argument("--event-share", type=float, default=None,
                    help="paylaşılan olay kaybı payı (varsayılan 0)")
    ap.add_argument("--signal-frac", type=float, default=None,
                    help="S3-O: sinyal taşıyabilen aday satırı payı (varsayılan 1)")
    ap.add_argument("--eps-quiet", type=float, default=None,
                    help="S3-P: ε dalında sessiz çekme olasılığı (varsayılan 0)")
    ap.add_argument("--ensemble", type=float, nargs=2, default=None,
                    metavar=("K", "BETA"), help="A1: topluluk K ve β")
    ap.add_argument("--min-safe", type=int, default=None,
                    help="Program C: sığınak için eşzamanlı doğru ajan sayısı")
    ap.add_argument("--inherit-per", action="store_true",
                    help="A2′: halef PER tamponu + optimizer durumunu devralır")
    a = ap.parse_args()
    run_ecology(a.turns, a.out, world_seed=a.world_seed, log_every=a.log_every,
                founding=a.founding, nest=(int(a.nest[0]), float(a.nest[1])),
                events=a.events, channel=a.channel, mutation_sigma=a.sigma,
                event_penalty=a.event_penalty, event_every=a.event_every,
                selection=a.selection, event_lead=a.event_lead,
                event_share=a.event_share,
                signal_candidate_frac=a.signal_frac,
                eps_signal_quiet=a.eps_quiet,
                ensemble=None if a.ensemble is None
                else (int(a.ensemble[0]), float(a.ensemble[1])),
                event_min_safe=a.min_safe, inherit_per=a.inherit_per)


if __name__ == "__main__":
    main()
