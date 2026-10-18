"""
x3_stallclass.py -- attribution of the host stalls of the controlled X3 repeat (v1.9), with the rule filed before the
runs in results/testbed_x3_repeat_prereg.json ("stall_classification").

A stall episode is a set of frames that the emulator delivered more than STALL_MS after their schedule (x3_qc.py's
rule), with overlapping windows W = [t_in + one-way delay, t_sent]. Over the hostmon.py samples that bracket W
(Delta t between the last sample at or before its start and the first at or after its end):
  steal   = steal jiffies of the emulator's CPU x 10 ms        (the hypervisor ran something else on that vCPU)
  wait    = the emulator's run-queue wait                       (runnable, but another task or interrupt work ran)
  run     = the emulator's on-CPU time                          (the emulator itself was computing)
Class, in this order: "steal" if steal >= Delta t / 2; "preempted" if wait >= Delta t / 2; "busy" if run >= Delta t / 2;
"blocked" if any sample inside W shows state D (uninterruptible wait) or T (stopped); else "idle" (the emulator slept
although a frame was due). Only "busy" can come from the emulator's own processing, and so from the condition;
"steal", "preempted" and "blocked" are interference from outside the emulator.
An invalid interval (x3_qc.py) takes the class of the episode that holds its latest frame.

usage: X3_RESULTS=testbed_x3_repeat.json python3 x3_stallclass.py     -> results/testbed_x3_repeat_stallclass.json
       python3 x3_stallclass.py EMU_LOG MON_LOG OWD_MS                 (episodes of one run, for tests)
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STALL_MS = 15.0
JIFFY_S = 0.01
STATE_COL, CPU_COL = 3, 4


def load_mon(path):
    t, run, wait, state, cpu, steal = [], [], [], [], [], []
    for line in open(path):
        f = line.split()
        if len(f) < 5 + 16: continue
        t.append(float(f[0])); run.append(int(f[1])); wait.append(int(f[2])); state.append(f[STATE_COL]); c = int(f[CPU_COL]); cpu.append(c)
        steal.append([int(f[5 + 8 * k + 7]) for k in range(2)])       # steal jiffies of cpu0 and cpu1
    return {"t": np.array(t), "run": np.array(run, dtype=np.int64), "wait": np.array(wait, dtype=np.int64), "state": state,
            "cpu": np.array(cpu), "steal": np.array(steal, dtype=np.int64)}


def late_frames(emu_log, owd_s):
    rows = [l.split() for l in open(emu_log)]
    rows = [r for r in rows if len(r) >= 7]
    t = np.array([float(r[0]) for r in rows]); tout = np.array([float(r[3]) for r in rows])
    lag = (tout - t - owd_s) * 1e3
    m = (tout > 0) & (lag > STALL_MS)
    return t[m] + owd_s, tout[m], lag[m]


def episodes(emu_log, mon_log, owd_s):
    due, sent, lag = late_frames(emu_log, owd_s)
    eps = []
    for a, b, l in sorted(zip(due, sent, lag)):
        if eps and a <= eps[-1]["t_sent"]:
            e = eps[-1]; e["t_sent"] = max(e["t_sent"], b); e["frames"] += 1
            if l > e["lag_ms"]: e["lag_ms"] = float(l); e["t_latest_frame_in"] = float(a - owd_s)
        else:
            eps.append({"t_due": float(a), "t_sent": float(b), "lag_ms": float(l), "frames": 1, "t_latest_frame_in": float(a - owd_s)})
    M = load_mon(mon_log) if eps else None
    for e in eps:
        i = int(np.searchsorted(M["t"], e["t_due"], side="right") - 1); j = int(np.searchsorted(M["t"], e["t_sent"], side="left"))
        if i < 0 or j >= len(M["t"]):
            e["class"] = "unmonitored"; continue
        dt = M["t"][j] - M["t"][i]
        cpu = int(np.bincount(M["cpu"][i:j + 1]).argmax())
        steal = (M["steal"][j, cpu] - M["steal"][i, cpu]) * JIFFY_S
        wait = (M["wait"][j] - M["wait"][i]) / 1e9; run = (M["run"][j] - M["run"][i]) / 1e9
        states = M["state"][i + 1:j] or M["state"][i:j + 1]
        e.update({"window_s": float(dt), "cpu": cpu, "steal_frac": float(steal / dt), "wait_frac": float(wait / dt), "run_frac": float(run / dt),
                  "states": {s: states.count(s) for s in sorted(set(states))}, "samples": j - i + 1})
        if steal >= dt / 2: e["class"] = "steal"
        elif wait >= dt / 2: e["class"] = "preempted"
        elif run >= dt / 2: e["class"] = "busy"
        elif any(s in ("D", "T", "t") for s in states): e["class"] = "blocked"
        else: e["class"] = "idle"
    return eps


def main():
    from x3 import t2_nsa_ms, PROFILES
    from run import TMP
    import x3_qc
    inp = os.environ.get("X3_RESULTS", "testbed_x3_repeat.json")
    res = json.load(open(os.path.join(HERE, "..", "results", inp)))
    qc = json.load(open(os.path.join(HERE, "..", "results", inp.replace(".json", "_qc.json"))))
    T2 = t2_nsa_ms()
    out = {"rule": __doc__.split("\n\n")[1], "stall_ms": STALL_MS, "cells": {}}
    for key, c in res["cells"].items():
        prof, pol, cfg, ch = key.split("|"); owd = PROFILES[prof]["owd_ms"] / 1e3
        for r in c["runs"]:
            seed = r["seed"]; tag = f"{prof}_{pol}_{cfg}_{ch[2:]}_{seed}"
            eps = episodes(os.path.join(TMP, f"x3_emu_{tag}.log"), os.path.join(TMP, f"x3_mon_{tag}.log"), owd)
            # interval of each episode: the windows of x3_qc (schedule origin fitted from the drops, as there)
            win = x3_qc.windows(os.path.join(TMP, f"x3_emu_{tag}.log"), seed, T2)
            inv = qc["cells"][key][str(seed)]["invalid"]
            per = []
            for k in range(len(inv)):
                mine = [e for e in eps if win(e["t_latest_frame_in"]) == k]
                top = max(mine, key=lambda e: e["lag_ms"]) if mine else None
                per.append({"invalid": inv[k], "episodes": len(mine), "class": top["class"] if top else None,
                            "lag_ms": top["lag_ms"] if top else None})
            out["cells"].setdefault(key, {})[str(seed)] = {"intervals": per, "episodes": eps}
    tally = {}
    for key, v in out["cells"].items():
        for q in v.values():
            for x in q["intervals"]:
                if x["invalid"]: tally.setdefault(key, {}).setdefault(x["class"], 0); tally[key][x["class"]] += 1
    out["invalid_by_class"] = tally
    json.dump(out, open(os.path.join(HERE, "..", "results", inp.replace(".json", "_stallclass.json")), "w"), indent=1)
    print(json.dumps(tally, indent=1))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        for e in episodes(sys.argv[1], sys.argv[2], float(sys.argv[3]) / 1e3):
            print(json.dumps(e))
    else:
        main()
