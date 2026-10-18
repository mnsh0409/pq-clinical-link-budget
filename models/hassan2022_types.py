"""
hassan2022_types.py -- event categories in the released handover log of Hassan et al. (SIGCOMM 2022) that Sec. V uses
(figure9-ho_exec_duration/HO-Duration_Combined.csv; the dataset is fetched locally, see data/README.md, and never
redistributed). Supports the Limitations sentence "the data identify no dual active protocol stack or conditional
handover": the log's Type column has no such category (counts per Type, Tech and Operator are recorded).
Output: results/hassan2022_event_types.json        usage: python3 hassan2022_types.py
"""
import collections, csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
F = os.path.join(ROOT, "data", "sigcomm22-5g-mobility", "data", "figure9-ho_exec_duration", "HO-Duration_Combined.csv")
with open(F, newline="") as h:
    rows = list(csv.DictReader(h))
out = {"file": "data/sigcomm22-5g-mobility/data/figure9-ho_exec_duration/HO-Duration_Combined.csv", "rows": len(rows)}
for col in ("Type", "Tech", "Operator"):
    out[col] = dict(sorted(collections.Counter(r[col] for r in rows).items()))
out["daps_or_conditional_category"] = any(("daps" in t.lower()) or ("dual" in t.lower()) or ("cond" in t.lower()) or ("cho" == t.lower()) for t in out["Type"])
json.dump(out, open(os.path.join(ROOT, "results", "hassan2022_event_types.json"), "w"), indent=1)
print(json.dumps(out))
