"""
x3_stalldiag.py -- post hoc diagnostic of the stall episodes of the controlled repeat (v1.9; NOT the rule filed before
the runs, which is testbed/x3_stallclass.py). The filed rule found no episode in which the emulator was busy; most
were "idle" (neither running nor waiting for a CPU nor blocked). This script asks whether the monitor itself, which runs
on the other vCPU (hostmon.py, a sample every 5 ms), missed samples during each episode: if both vCPUs stall together,
the cause is outside the guest (the virtual machine as a whole was not running), which the steal counter, kept in
10 ms jiffies, records only in part. It also reports the emulator's state letters and steal in an extended window.
Output: results/testbed_x3_repeat_stalldiag.json        usage: python3 x3_stalldiag.py
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import x3_stallclass as C
from run import TMP
GAP_MS = 15.0
SC = json.load(open(os.path.join(HERE, "..", "results", "testbed_x3_repeat_stallclass.json")))
rows, gaps_all, gaps_big, gaps_big_in_ep, n_samples = [], [], 0, 0, 0
for key, v in SC["cells"].items():
    prof, pol, cfg, ch = key.split("|")
    for seed, q in v.items():
        M = C.load_mon(os.path.join(TMP, f"x3_mon_{prof}_{pol}_{cfg}_{ch[2:]}_{seed}.log"))
        t = M["t"]; g = np.diff(t) * 1e3; gaps_all.extend(g.tolist()); n_samples += len(t)
        eps = q["episodes"]
        for b in np.where(g > GAP_MS)[0]:
            gaps_big += 1
            if any(e["t_due"] - 0.02 <= t[b + 1] and t[b] <= e["t_sent"] + 0.02 for e in eps): gaps_big_in_ep += 1
        for e in eps:
            i = int(np.searchsorted(t, e["t_due"], side="right") - 1); j = int(np.searchsorted(t, e["t_sent"], side="left"))
            j2 = min(int(np.searchsorted(t, e["t_sent"] + 0.1, side="left")), len(t) - 1)
            seg = M["state"][i:j + 1]
            rows.append({"cell": key, "seed": int(seed), "lag_ms": e["lag_ms"], "class": e["class"],
                         "monitor_max_gap_ms": float(g[i:j].max()) if j > i else None, "R_share": seg.count("R") / max(1, len(seg)),
                         "steal_ms_extended": [int((M["steal"][j2, c] - M["steal"][max(i - 2, 0), c]) * 10) for c in (0, 1)]})
gaps_all = np.array(gaps_all); mg = np.array([r["monitor_max_gap_ms"] or 0 for r in rows])
out = {"note": __doc__.strip().split("\n\n")[0], "gap_threshold_ms": GAP_MS, "monitor_samples": n_samples, "monitor_gap_median_ms": float(np.median(gaps_all)),
       "monitor_gaps_over_threshold": gaps_big, "monitor_gaps_over_threshold_in_episodes": gaps_big_in_ep,
       "episodes": len(rows), "episodes_with_monitor_gap": int((mg > GAP_MS).sum()), "episodes_with_steal": int(sum(1 for r in rows if max(r["steal_ms_extended"]) > 0)),
       "rows": rows}
json.dump(out, open(os.path.join(HERE, "..", "results", "testbed_x3_repeat_stalldiag.json"), "w"), indent=1)
print({k: v for k, v in out.items() if k not in ("rows", "note")})
