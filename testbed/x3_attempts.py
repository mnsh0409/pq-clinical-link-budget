"""
x3_attempts.py -- post hoc check (v1.9, after the controlled repeat; NOT part of any filed analysis) of the model's timing
assumptions in the lost-session windows of all three X3 blocks (development, held-out, repeat), asked by the review of
v1.9: are the model's misses at 18 ms a detection delay?

From the client's loss declarations (per_outage detect_ms) and the emulator logs (the SYN of each connection attempt):
  - loss declaration after the onset, against the model's mean declaration time t_d = tau + 8 ms - RTT/2 (tau = RTT + 26.5 ms);
  - period of the failed attempts (SYN to SYN), against tau;
  - first SYN after the declaration.
Then the model with the measured timing: the extra period delta and the first-attempt delay delta0 are estimated on the
DEVELOPMENT block only and applied unchanged to the held-out and repeat blocks (cell means and paired contrasts over the
windows the exclusion rule keeps). Windows flagged by x3_qc.py are skipped.
Output: results/testbed_x3_attempt_timing.json        usage: python3 x3_attempts.py   (needs the emulator logs in $TESTBED_TMP)
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "models"))
sys.argv = sys.argv[:1]
import x3_qc as Q
import x3_model as M
from run import TMP
from x3 import t2_nsa_ms
RES = os.path.join(ROOT, "results")
T2 = t2_nsa_ms()
BLOCKS = {"development": ("testbed_x3.json", "testbed_x3_qc.json"), "heldout": ("testbed_x3_heldout.json", "testbed_x3_heldout_qc.json"),
          "repeat": ("testbed_x3_repeat.json", "testbed_x3_repeat_qc.json")}
PROF = {"5G-hosp": (10.0, 5.0), "5G-tele": (18.0, 9.0)}
S = json.load(open(os.path.join(RES, "testbed_summary.json")))
H_of = lambda prof, cfg, ch: S["rows"][f"{cfg}|ch{ch}"]["tcp_ms"][prof]


def timing(b):
    xf, qf = BLOCKS[b]; X = json.load(open(os.path.join(RES, xf))); QC = json.load(open(os.path.join(RES, qf))); out = {}
    for key, c in X["cells"].items():
        prof, pol, cfg, ch = key.split("|")
        if pol != "detect": continue
        rtt, owd = PROF[prof]; tau = M.pto_ms(rtt)
        det, gaps, first = [], [], []
        for r in c["runs"]:
            logf = os.path.join(TMP, f"x3_emu_{prof}_{pol}_{cfg}_{ch[2:]}_{r['seed']}.log")
            rows, t, tout = Q.read_log(logf)
            _, a, _ = Q.fit_schedule(t, tout, r["seed"], T2)
            inv = QC["cells"][key][str(r["seed"])]["invalid"]
            syn = [float(x[0]) for x in rows if x[1] == "AB" and int(x[2]) == 74]
            for i, o in enumerate(r["per_outage"]):
                if inv[i] or o["detect_ms"] is None: continue
                det.append(o["detect_ms"]); d = a[i] + o["detect_ms"] / 1e3
                s = [ti for ti in syn if d - 0.002 <= ti < a[i] + 2.0][:o["failed_attempts"] + 1]
                if s:
                    first.append((s[0] - d) * 1e3); gaps += list(np.diff(s) * 1e3)
        out[key] = {"tau_ms": tau, "td_model_mean_ms": tau + M.PERIOD_MS / 2 - owd, "declaration_ms_mean": float(np.mean(det)), "n_declarations": len(det),
                    "attempt_period_ms_mean": float(np.mean(gaps)) if gaps else None, "n_attempt_periods": len(gaps),
                    "first_syn_after_declaration_ms_median": float(np.median(first))}
    return out


def late_for_phase(D, H, rtt, g0, d, d0):
    pto = M.pto_ms(rtt); td = g0 + pto; s = td + d0
    n = 0 if s >= D else math.ceil((D - s) / (pto + d))
    L = s + n * (pto + d) + H - M.DEADLINE_MS - (g0 if g0 >= 0 else g0 + M.PERIOD_MS)
    return 0 if L < 0 else math.floor(L / M.PERIOD_MS) + 1


def expect(D, H, rtt, owd, d, d0):
    G = np.arange(-owd, M.PERIOD_MS - owd, 0.25)
    return float(np.mean([late_for_phase(D, H, rtt, g, d, d0) for g in G]))


TM = {b: timing(b) for b in BLOCKS}
dev = TM["development"].values()
DELTA = sum((v["attempt_period_ms_mean"] - v["tau_ms"]) * v["n_attempt_periods"] for v in dev) / sum(v["n_attempt_periods"] for v in dev)
DELTA0 = float(np.median([v["first_syn_after_declaration_ms_median"] for v in dev]))
assert all(abs(expect(D, 48.6, 18.0, 9.0, 0.0, 0.0) - M.late_expect(D, 48.6, 18.0, 9.0)[0]) < 1e-12 for D in (20.0, 47.0, 66.0, 111.0))   # delta = delta0 = 0 is the model
out = {"note": __doc__.strip().split("\n\n")[0], "delta_ms_from_development": DELTA, "delta0_ms_from_development": DELTA0, "timing": TM, "model_with_timing": {}}
for b, (xf, qf) in BLOCKS.items():
    X = json.load(open(os.path.join(RES, xf))); QC = json.load(open(os.path.join(RES, qf))); cells = {}
    for key, c in X["cells"].items():
        prof, pol, cfg, ch = key.split("|")
        if pol != "detect": continue
        rtt, owd = PROF[prof]; H = H_of(prof, cfg, int(ch[2:]))
        per = [x for r in c["runs"] for x in r["per_outage"]]
        ok = np.array([not v for r in c["runs"] for v in QC["cells"][key][str(r["seed"])]["invalid"]])
        obs = np.array([x["late"] for x in per], float)
        m0 = np.array([M.late_expect(x["outage_ms"], H, rtt, owd)[0] for x in per]); m1 = np.array([expect(x["outage_ms"], H, rtt, owd, DELTA, DELTA0) for x in per])
        cells[key] = (obs, m0, m1, ok)
    res = {"cells": {k: {"late_obs": float(v[0][v[3]].mean()), "late_model": float(v[1][v[3]].mean()), "late_model_with_timing": float(v[2][v[3]].mean())} for k, v in cells.items()},
           "contrasts": {}}
    for prof in PROF:
        k0, k2, kw = f"{prof}|detect|C0|ch2", f"{prof}|detect|C2|ch3", f"{prof}|detect|C2w|ch3"
        for name, (ka, kb) in {"C2int_minus_C0": (k2, k0), "C2w_minus_C0": (kw, k0), "C2w_minus_C2int": (kw, k2)}.items():
            if ka in cells and kb in cells:
                (oa, ma, na, oka), (ob, mb, nb, okb) = cells[ka], cells[kb]; m = oka & okb
                res["contrasts"][f"{prof}|{name}"] = {"obs": float((oa - ob)[m].mean()), "model": float((ma - mb)[m].mean()), "model_with_timing": float((na - nb)[m].mean()), "n": int(m.sum())}
    allo = np.concatenate([v[0][v[3]] for v in cells.values()])
    res["mae"] = {"model": float(np.mean(np.abs(allo - np.concatenate([v[1][v[3]] for v in cells.values()])))),
                  "model_with_timing": float(np.mean(np.abs(allo - np.concatenate([v[2][v[3]] for v in cells.values()]))))}
    out["model_with_timing"][b] = res
json.dump(out, open(os.path.join(RES, "testbed_x3_attempt_timing.json"), "w"), indent=1)
print(f"delta {DELTA:.2f} ms, delta0 {DELTA0:.2f} ms (development)")
for b in BLOCKS:
    for k, v in TM[b].items():
        if "5G-tele" in k: print(b, k, {kk: round(vv, 2) if isinstance(vv, float) else vv for kk, vv in v.items()})
    print(b, "MAE", out["model_with_timing"][b]["mae"], {k: {kk: round(vv, 2) for kk, vv in v.items() if kk != "n"} for k, v in out["model_with_timing"][b]["contrasts"].items() if "5G-tele" in k})
