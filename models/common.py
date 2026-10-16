"""common.py -- ledger access for the model scripts.

Every number a model uses must come through `p(key)` (value) and be cited with
`cid(key)` (ledger id) so that the results JSON carries provenance.  Anything a
model computes is a DERIVED quantity and is recorded with the list of ledger ids
it combines plus any assumption text.
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(HERE, "..", "sources", "ledger.json")
RESULTS_DIR = os.path.join(HERE, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

with open(LEDGER_PATH) as _f:
    LEDGER = json.load(_f)
PARAMS = LEDGER["params"]

def p(key):
    return PARAMS[key]["value"]

def cid(key):
    return PARAMS[key]["id"]

def status(key):
    return PARAMS[key]["status"]

def derived(value, unit, from_keys, assumption=None, note=None):
    d = {"value": value, "unit": unit, "derived_from": [f"{k}[{cid(k)}]" for k in from_keys]}
    if assumption: d["assumption"] = assumption
    if note: d["note"] = note
    return d

def fmt_time(s):
    if s < 1e-3: return f"{s*1e6:.0f} us"
    if s < 1:    return f"{s*1e3:.1f} ms"
    if s < 60:   return f"{s:.2f} s"
    if s < 3600: return f"{s/60:.1f} min"
    if s < 86400:return f"{s/3600:.1f} h"
    return f"{s/86400:.1f} d"

def fmt_bytes(b):
    if b < 1e3: return f"{b:.0f} B"
    if b < 1e6: return f"{b/1e3:.1f} kB"
    if b < 1e9: return f"{b/1e6:.2f} MB"
    return f"{b/1e9:.2f} GB"

def save(name, obj):
    path = os.path.join(RESULTS_DIR, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)
    print(f"wrote {os.path.normpath(path)}")
