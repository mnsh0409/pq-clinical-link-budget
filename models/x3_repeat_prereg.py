"""
x3_repeat_prereg.py -- v1.9: filing for the controlled repeat of the 18 ms comparison, written BEFORE those runs
(results/testbed_x3_repeat_prereg.json and the run order results/testbed_x3_repeat_order.json; the sha256 of both is
printed). It answers the v1.8 review's open question: whether the 20-segment window's deadline benefit at 18 ms survives
when every interval is kept, on a host whose scheduling is controlled.
Cells (5G-tele, 18 ms RTT): detect C0, detect C2 + int. (default initial window), detect C2w + int. (initial window 20
segments, same keys and certificates). Ten new seeds; each seed runs the three cells in a random order fixed here.
Predictions use x3_model.py with H = the X12 median connect-to-first-record time (Table III), as for the held-out block.
"""
import hashlib, json, os, sys, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "testbed"))
sys.argv = sys.argv[:1]
import x3_model as M
from x3 import t2_nsa_ms, PROFILES, OUT_EVERY_S
X12 = json.load(open(os.path.join(ROOT, "results", "testbed_x12.json")))
SEEDS = list(range(20261030, 20261040)); N_OUT = 7; ORDER_SEED = 20261040; PNAME = "5G-tele"
CELLS = [("detect", "C0", 2), ("detect", "C2", 3), ("detect", "C2w", 3)]
used = set(range(20261015, 20261025))
assert not used & set(SEEDS)                                     # new seeds: not in the development or held-out blocks
rng_o = np.random.default_rng(ORDER_SEED)
order = [[s, f"{CELLS[i][0]}:{CELLS[i][1]}:{CELLS[i][2]}"] for s in SEEDS for i in rng_o.permutation(len(CELLS))]
T2 = t2_nsa_ms(); PR = PROFILES[PNAME]; rtt, owd = 2 * PR["owd_ms"], PR["owd_ms"]
out = {"written": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "seeds": SEEDS, "profile": PNAME,
       "run_order": order, "run_order_rng_seed": ORDER_SEED,
       "host_control": {"emulator": "pinned to CPU 1 (taskset), SCHED_FIFO priority 50 (chrt)", "endpoints_and_monitor": "pinned to CPU 0",
                        "other_work": "no analysis or build jobs during the block; every other process moved to CPU 0 before it starts",
                        "monitor": "testbed/hostmon.py, every 5 ms: the emulator's on-CPU time and run-queue wait (schedstat), state, CPU; per-CPU jiffies incl. steal",
                        "env": {"X3_EMU_CPU": "1", "X3_EMU_RT": "50", "X3_EP_CPU": "0", "X3_HOSTMON": "1", "X3_ORDER": "interleave", "X3_PROFILES": PNAME}},
       "model": {"PTO_ms": "RTT + 25 + 1 (variation floor) + 0.5 (host turnaround) = RTT + 26.5", "period_ms": M.PERIOD_MS, "deadline_ms": M.DEADLINE_MS,
                 "phase": "g0 uniform on [-OWD, 16 - OWD)", "H_source": "results/testbed_x12.json t_first_record_ms.median"},
       "analysis_plan": [
           "exclusion rule unchanged (testbed/x3_qc.py): an interval is invalid if the emulator delivered any frame more than 15 ms after its schedule",
           "contrasts per interruption, paired by seed and interruption index: C2 + int. minus C0, C2w minus C0, C2w minus C2 + int.; each reported both over the intervals valid in both cells and over all 70 intervals",
           "intervals: two-stage percentile bootstrap (runs, then interruptions within runs; 10,000 draws), as Table IV, and a t-interval over the ten run means",
           "scoring: the filed per-interruption predictions below; mean absolute error over valid intervals; whether each interval contains the prediction for the same intervals",
           "Q1: the window's 18 ms benefit counts as robust if the all-interval C2w minus C2 + int. interval lies below 0; Q2: the window's remaining penalty is reported as the all-interval C2w minus C0 interval (no detectable penalty if it includes 0; equivalence is not tested); Q3: exclusions per cell, each attributed by the rule below",
           "every outcome is reported, including one that shows no robust benefit; the held-out block's results stay in the paper"],
       "stall_classification": "testbed/x3_stallclass.py: per stall episode (frames more than 15 ms late with overlapping windows W), over the monitor samples bracketing W: 'steal' if the steal jiffies of the emulator's CPU cover at least half of it; else 'preempted' if the emulator's run-queue wait does; else 'busy' if its on-CPU time does; else 'blocked' if a sample in W shows state D or T; else 'idle'. Only 'busy' can come from the emulator's own processing; an invalid interval takes the class of the episode with its latest frame",
       "cells": {}}
for pol, cfg, ch in CELLS:
    H = X12[f"{PNAME}|{cfg}|ch{ch}"]["t_first_record_ms"]["median"]
    key = f"{PNAME}|{pol}|{cfg}|ch{ch}"; runs = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed); durs = rng.choice(T2, size=N_OUT)      # as x3.one(): durations first
        _ = [rng.uniform(-1, 1) for _ in range(N_OUT)]                              # then the start jitter
        per = []
        for D in durs:
            e, n, T = M.late_expect(float(D), H, rtt, owd)
            per.append({"outage_ms": float(D), "late_expected": round(e, 4), "failed_attempts_expected": round(n, 4), "detect_expected_ms": round(T, 2)})
        runs.append({"seed": seed, "per_outage": per})
    allp = [x["late_expected"] for r in runs for x in r["per_outage"]]
    out["cells"][key] = {"H_ms": H, "rtt_ms": rtt, "runs": runs, "late_per_interruption_expected": float(np.mean(allp)),
                         "failed_attempts_expected": float(np.mean([x["failed_attempts_expected"] for r in runs for x in r["per_outage"]]))}
C = out["cells"]; k0, ki, kw = (f"{PNAME}|detect|C0|ch2", f"{PNAME}|detect|C2|ch3", f"{PNAME}|detect|C2w|ch3")
C[ki]["diff_from_C0_expected"] = C[ki]["late_per_interruption_expected"] - C[k0]["late_per_interruption_expected"]
C[kw]["diff_from_C0_expected"] = C[kw]["late_per_interruption_expected"] - C[k0]["late_per_interruption_expected"]
C[kw]["diff_from_C2int_expected"] = C[kw]["late_per_interruption_expected"] - C[ki]["late_per_interruption_expected"]
out["claims"] = [
    f"over all 70 interruptions the model expects C2 + int. minus C0 {C[ki]['diff_from_C0_expected']:+.2f}, C2w minus C0 {C[kw]['diff_from_C0_expected']:+.2f} and C2w minus C2 + int. {C[kw]['diff_from_C2int_expected']:+.2f} late records per interruption at 18 ms",
    f"late records per interruption: C0 {C[k0]['late_per_interruption_expected']:.2f}, C2 + int. {C[ki]['late_per_interruption_expected']:.2f}, C2w {C[kw]['late_per_interruption_expected']:.2f}; failed attempts {C[k0]['failed_attempts_expected']:.2f} per interruption in every cell"]
p = os.path.join(ROOT, "results", "testbed_x3_repeat_prereg.json"); po = os.path.join(ROOT, "results", "testbed_x3_repeat_order.json")
json.dump(out, open(p, "w"), indent=1); json.dump(order, open(po, "w"), indent=1)
for f in (p, po): print(os.path.basename(f), "sha256", hashlib.sha256(open(f, "rb").read()).hexdigest())
for k, v in C.items():
    print(f"{k:28s} H {v['H_ms']:6.1f}  late {v['late_per_interruption_expected']:.3f}  fail {v['failed_attempts_expected']:.3f}", {kk: round(vv, 3) for kk, vv in v.items() if kk.startswith('diff')})
print("order", order)
