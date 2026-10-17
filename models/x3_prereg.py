"""
x3_prereg.py -- pre-registration of the model's predictions for the held-out X3 block (seeds 20261020..24), written
BEFORE those runs (results/testbed_x3_heldout_prereg.json; its sha256 is printed and recorded in testbed/README.md).
Cells: detect C0, detect C2 + int. (default initial window), detect C2w + int. (initial window 20 segments on both
endpoints, same keys and certificates as C2), on the 5G-hosp (10 ms) and 5G-tele (18 ms) profiles.
Predictions use x3_model.py with H = the X12 median connect-to-first-record time of the configuration (Table III) and
the interruptions that x3.py will draw from each seed (replayed here exactly as x3.py draws them).
"""
import hashlib, json, os, sys, datetime
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "testbed"))
import x3_model as M
from x3 import t2_nsa_ms, PROFILES, OUT_EVERY_S
X12 = json.load(open(os.path.join(ROOT, "results", "testbed_x12.json")))
SEEDS = list(range(20261020, 20261025)); N_OUT = 7
CELLS = [("detect", "C0", 2), ("detect", "C2", 3), ("detect", "C2w", 3)]
T2 = t2_nsa_ms()
out = {"written": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "seeds": SEEDS,
       "model": {"PTO_ms": "RTT + 25 + 1 (variation floor) + 0.5 (host turnaround) = RTT + 26.5", "period_ms": M.PERIOD_MS, "deadline_ms": M.DEADLINE_MS,
                 "phase": "g0 uniform on [-OWD, 16 - OWD)", "H_source": "results/testbed_x12.json t_first_record_ms.median"},
       "claims": [],   # filled below from the computed expectations
       "cells": {}}
for pname, PR in PROFILES.items():
    rtt, owd = 2 * PR["owd_ms"], PR["owd_ms"]
    for pol, cfg, ch in CELLS:
        H = X12[f"{pname}|{cfg}|ch{ch}"]["t_first_record_ms"]["median"]
        key = f"{pname}|{pol}|{cfg}|ch{ch}"; runs = []
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
for pname in PROFILES:
    c0 = out["cells"][f"{pname}|detect|C0|ch2"]["late_per_interruption_expected"]
    for pol, cfg, ch in CELLS[1:]:
        k = f"{pname}|{pol}|{cfg}|ch{ch}"; out["cells"][k]["diff_from_C0_expected"] = out["cells"][k]["late_per_interruption_expected"] - c0
    out["cells"][f"{pname}|detect|C2w|ch3"]["diff_from_C2int_expected"] = out["cells"][f"{pname}|detect|C2w|ch3"]["late_per_interruption_expected"] - out["cells"][f"{pname}|detect|C2|ch3"]["late_per_interruption_expected"]
C = out["cells"]
out["claims"] = [
    f"paired difference from C0 of C2w + int. (initial window 20, same ML-DSA-65 chain): {C['5G-hosp|detect|C2w|ch3']['diff_from_C0_expected']:+.2f} (10 ms) and {C['5G-tele|detect|C2w|ch3']['diff_from_C0_expected']:+.2f} (18 ms) late records per interruption; its 95 % interval should include 0 and exclude the default-window difference",
    f"paired difference from C0 of C2 + int. (default window): {C['5G-hosp|detect|C2|ch3']['diff_from_C0_expected']:+.2f} (10 ms) and {C['5G-tele|detect|C2|ch3']['diff_from_C0_expected']:+.2f} (18 ms)",
    f"late records per interruption: C0 {C['5G-hosp|detect|C0|ch2']['late_per_interruption_expected']:.2f} / {C['5G-tele|detect|C0|ch2']['late_per_interruption_expected']:.2f}, C2 + int. {C['5G-hosp|detect|C2|ch3']['late_per_interruption_expected']:.2f} / {C['5G-tele|detect|C2|ch3']['late_per_interruption_expected']:.2f}, C2w + int. {C['5G-hosp|detect|C2w|ch3']['late_per_interruption_expected']:.2f} / {C['5G-tele|detect|C2w|ch3']['late_per_interruption_expected']:.2f} (10 / 18 ms)",
    f"failed attempts per interruption {C['5G-hosp|detect|C0|ch2']['failed_attempts_expected']:.2f} (10 ms) and {C['5G-tele|detect|C0|ch2']['failed_attempts_expected']:.2f} (18 ms), the same in every cell of a profile (the detector, not the configuration, sets them)",
    "intervals that need no retry: C2 + int. late at 18 ms (about 1.4 per interruption), every other cell about 0; intervals that need a retry: every cell late (about 1 at 10 ms, 2 to 3 at 18 ms; C2 + int. 2 and 4 to 5): the initial window removes the certificate-chain penalty, not the retry cost",
    "scoring: mean absolute error of the per-interval expectation against the observed count over the intervals testbed/x3_qc.py leaves valid (rule fixed before these runs: a frame delivered more than 15 ms late), cell means, and whether each paired 95 % interval (two-stage bootstrap, as Table IV) contains the prediction"]
p = os.path.join(ROOT, "results", "testbed_x3_heldout_prereg.json")
json.dump(out, open(p, "w"), indent=1)
print("sha256", hashlib.sha256(open(p, "rb").read()).hexdigest())
for k, v in out["cells"].items():
    print(f"{k:28s} H {v['H_ms']:6.1f}  late {v['late_per_interruption_expected']:.3f}  fail {v['failed_attempts_expected']:.3f}", {kk: round(vv, 3) for kk, vv in v.items() if kk.startswith('diff')})
