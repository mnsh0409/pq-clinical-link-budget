"""
timeline.py -- per-segment timeline of one cold TCP connection on the 5G-hosp profile for C0, C2 and C2 + intermediate:
which part of each data flight left in the first burst and when the rest followed (after the peer's acknowledgments).
A burst ends at a gap of more than GAP_MS between consecutive data segments of the same flight.
Results -> results/testbed_timeline.json.   usage: python3 timeline.py   (TL_CASES=C2w:3 python3 timeline.py adds the
initial-window-20 case, C2 + intermediates with the same keys and certificates, to the existing file)
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "models"))
from common import p
from run import run_case, CLEANUP, TMP

GAP_MS = 4.0
PROF = {"name": "5G-hosp", "ul": p("ul_5gsa_chen2024_avg_bps"), "dl": p("dl_5gsa_chen2024_avg_bps"), "owd_ms": p("rtt_5g_berlet2022_ms") / 2}

def first_conn_flights(log):
    rows = [l.split() for l in open(log) if len(l.split()) >= 7]
    rows = [(float(r[0]), r[1], int(r[6]), int(r[4]), int(r[5])) for r in rows]
    cport = next(r[3] for r in rows if r[1] == "AB" and r[2] >= 0)
    conn = [r for r in rows if (r[1] == "AB" and r[3] == cport) or (r[1] == "BA" and r[4] == cport)]
    t0 = conn[0][0]
    fl = []
    for t, d, pl, _, _ in conn:
        if pl <= 0: continue
        t = (t - t0) * 1e3; d = "C>S" if d == "AB" else "S>C"
        if not fl or fl[-1]["dir"] != d:
            fl.append({"dir": d, "bursts": []})
        b = fl[-1]["bursts"]
        if b and t - b[-1]["t_last_ms"] <= GAP_MS:
            b[-1]["segments"] += 1; b[-1]["payload_B"] += pl; b[-1]["t_last_ms"] = t
        else:
            b.append({"segments": 1, "payload_B": pl, "t_first_ms": t, "t_last_ms": t})
    for f in fl:
        f["payload_B"] = sum(b["payload_B"] for b in f["bursts"]); f["segments"] = sum(b["segments"] for b in f["bursts"])
        f["stalls_ms"] = [f["bursts"][i + 1]["t_first_ms"] - f["bursts"][i]["t_last_ms"] for i in range(len(f["bursts"]) - 1)]
    return fl

def main():
    subprocess.run(["bash", os.path.join(HERE, "netns_up.sh")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dst = os.path.join(HERE, "..", "results", "testbed_timeline.json")
    cases = [("C0", 2), ("C2", 2), ("C2", 3)]
    if os.environ.get("TL_CASES"):          # e.g. TL_CASES=C2w:3 adds cases to the existing file without rerunning the others
        cases = [(c.split(":")[0], int(c.split(":")[1])) for c in os.environ["TL_CASES"].split(",")]
        out = json.load(open(dst))
    else:
        out = {"profile": PROF, "gap_ms": GAP_MS, "cases": {}}
    for cfg, ch in cases:
        tag = f"tl_{cfg}_ch{ch}"
        r = run_case(PROF, cfg, chain=ch, n=1, gap_ms=100, tag=tag)
        out["cases"][f"{cfg}|ch{ch}"] = {"t_first_record_ms": r["runs"][0]["t_first_record_server_ms"], "flights": first_conn_flights(f"{TMP}/emu_{tag}.log")}
        subprocess.run(CLEANUP)
        print(cfg, ch, json.dumps(out["cases"][f"{cfg}|ch{ch}"]), flush=True)
    json.dump(out, open(dst, "w"), indent=1)

if __name__ == "__main__":
    main()
