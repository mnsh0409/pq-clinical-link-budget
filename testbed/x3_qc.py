"""
x3_qc.py -- host-stall check of the X3 runs (x3.py), from the emulator logs that x3.py leaves in $TESTBED_TMP.

The emulated link has a constant one-way delay, so a frame that the emulator delivers more than STALL_MS after its
schedule (one-way delay plus queue) means the host did not run the emulator in time, an event outside the link model.
Such a stall marks the attribution window that contains it (x3.py: from 0.5 s before an interruption to 0.5 s before
the next) invalid. The rule looks only at the emulator's timing, never at whether records were late, and it is applied
to every cell; models/testbed_tables.py then compares cells over the windows valid in both.
Also reported, not used by the rule: "false", a new connection opened while the current one was alive in the emulator
(a session-loss declaration without an interruption; most coincide with a stall), and "client_start_after_origin_ms",
when the client's first connection request reached the emulator relative to the fitted schedule origin: the client's
record clock starts then, so the phase of the 16-ms record grid at an interruption onset differs between cells.
Each run's interruption schedule is replayed from its seed exactly as x3.py draws it (durations, then start jitter);
its time origin is fitted to the frames the emulator dropped in interruptions.

Output: results/testbed_x3_qc.json   usage: python3 x3_qc.py
"""
import glob, json, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x3 import t2_nsa_ms, PROFILES, OUT_EVERY_S
from run import TMP

STALL_MS = 15.0
N_OUT = 7

def check(logf, seed, owd_s, T2):
    rng = np.random.default_rng(seed)
    durs = rng.choice(T2, size=N_OUT)                                  # same draws, same order as x3.one()
    jit = np.array([rng.uniform(-1, 1) for _ in range(N_OUT)])
    rows = [l.split() for l in open(logf)]
    rows = [r for r in rows if len(r) >= 7]
    t = np.array([float(r[0]) for r in rows]); tout = np.array([float(r[3]) for r in rows])
    drops = t[tout < 0]
    best = (-1, None)
    for tb in np.arange(t[0] - 1.0, t[0] + 4.0, 0.001):                 # origin of the schedule (the log may open with a
                                                                        # stray frame up to ~2 s early): most drops inside it
        a = tb + OUT_EVERY_S * np.arange(1, N_OUT + 1) + jit; b = a + durs / 1e3
        k = int(sum(((drops >= a[i]) & (drops <= b[i] + 0.002)).sum() for i in range(N_OUT)))
        if k > best[0]: best = (k, tb)
    a = best[1] + OUT_EVERY_S * np.arange(1, N_OUT + 1) + jit
    lo = a - 0.5; hi = np.r_[a[1:] - 0.5, np.inf]
    win = lambda x: int(np.searchsorted(lo, x, side="right") - 1)       # -1: before the first window
    stall = [False] * N_OUT; false = [False] * N_OUT; syn_lost = [0] * N_OUT     # connection requests dropped in an interruption
    for x in t[(tout > 0) & ((tout - t - owd_s) * 1e3 > STALL_MS)]:
        i = win(x)
        if i >= 0: stall[i] = True
    seen, dead, cur = set(), set(), None
    for r in rows:
        ti, d, ln, to, sp, dp, pl = float(r[0]), r[1], int(r[2]), float(r[3]), int(r[4]), int(r[5]), int(r[6])
        cp = sp if d == "AB" else dp
        if to == -2: dead.add(cp)
        if d == "AB" and ln == 74 and to == -1:
            i = win(ti)
            if i >= 0: syn_lost[i] += 1
        if d == "AB" and ln == 74 and cp not in seen:                     # SYN of a new connection
            seen.add(cp)
            if cur is not None and cur not in dead:
                i = win(ti)
                if i >= 0: false[i] = True
        if d == "AB" and pl > 0: cur = cp                                 # the connection that carries records now
    t0 = min((float(r[0]) for r in rows if r[1] == "AB" and int(r[2]) == 74 and float(r[0]) >= best[1] - 0.5), default=float("nan"))
    return {"stall": stall, "false": false, "invalid": list(stall), "syn_dropped_in_interruption": syn_lost,
            "drops_in_schedule": best[0], "drops": int(len(drops)), "client_start_after_origin_ms": (t0 - best[1]) * 1e3}

def main():
    T2 = t2_nsa_ms()
    res = json.load(open(os.path.join(HERE, "..", "results", "testbed_x3.json")))
    out = {"stall_ms": STALL_MS, "cells": {}}
    for key, c in res["cells"].items():
        prof, pol, cfg, ch = key.split("|")
        owd = PROFILES[prof]["owd_ms"] / 1e3
        for r in c["runs"]:
            f = os.path.join(TMP, f"x3_emu_{prof}_{pol}_{cfg}_{ch[2:]}_{r['seed']}.log")
            q = check(f, r["seed"], owd, T2)
            out["cells"].setdefault(key, {})[str(r["seed"])] = q
    json.dump(out, open(os.path.join(HERE, "..", "results", "testbed_x3_qc.json"), "w"), indent=1)
    n = sum(len(q["invalid"]) for v in out["cells"].values() for q in v.values())
    bad = sum(sum(q["invalid"]) for v in out["cells"].values() for q in v.values())
    st = sum(sum(q["stall"]) for v in out["cells"].values() for q in v.values())
    fa = sum(sum(q["false"]) for v in out["cells"].values() for q in v.values())
    both = sum(sum(s and f for s, f in zip(q["stall"], q["false"])) for v in out["cells"].values() for q in v.values())
    print(f"{bad} of {n} windows invalid (emulator stall); false detections in {fa} windows, {both} of them with a stall")
    st0 = [q["client_start_after_origin_ms"] for v in out["cells"].values() for q in v.values()]
    print(f"client start after the schedule origin: {min(st0):.1f} to {max(st0):.1f} ms")
    for k, v in out["cells"].items():
        print(k, {s: sum(q["invalid"]) for s, q in v.items()}, "schedule fit:", [f"{q['drops_in_schedule']}/{q['drops']}" for q in v.values()])

if __name__ == "__main__":
    main()
