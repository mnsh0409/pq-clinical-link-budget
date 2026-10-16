"""
x3.py -- telemetry through handover outages (X3). Results -> results/testbed_x3.json.

Stream: 1,000-B message every 16 ms (= 0.5 Mb/s, the TR 22.826 cardiac-telemetry target), deadline 100 ms.
Link: 5G-hosp profile (ledger rates, 10 ms RTT). Outages: one every OUT_EVERY_S seconds, duration drawn
(seeded) from the measured NSA primary-cell execution-stage interruptions T2 of the SIGCOMM'22 artifact
(the same events as Fig. 2a). Cells: policy x configuration.
usage: python3 x3.py [RUNS] [DURATION_S]
"""
import json, os, signal, statistics, subprocess, sys, time
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "models"))
from common import p
from run import CONFIGS, PKI, TMP, CLEANUP

RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
PERIOD_MS = 16.0
DEADLINE_MS = p("telemetry_latency_ms")
OUT_EVERY_S = 10.0
PROFILES = {"5G-hosp": {"name": "5G-hosp", "ul": p("ul_5gsa_chen2024_avg_bps"), "dl": p("dl_5gsa_chen2024_avg_bps"), "owd_ms": p("rtt_5g_berlet2022_ms") / 2},
            "5G-tele": {"name": "5G-tele", "ul": p("ul_5g_ye2026_bps"), "dl": p("dl_5g_ye2026_bps"), "owd_ms": p("rtt_5g_moustris2023_ms") / 2}}
PROFILE = PROFILES["5G-hosp"]
CELLS = [("keep", "C2", 2), ("reconnect", "C0", 2), ("reconnect", "C1", 2), ("reconnect", "C2", 2), ("reconnect", "C2", 3), ("resume", "C2", 2)]

D1 = os.path.join(ROOT, "data", "sigcomm22-5g-mobility")
def t2_nsa_ms():
    cands = [os.path.join(dp, f) for dp, _, fs in os.walk(D1) for f in fs if f == "HO-Duration_Combined.csv"]
    ho = pd.read_csv(cands[0])
    ho = ho[(ho["Tech"] == "NSA") & (ho["Type"].isin(["PCell", "MCG"]))]
    t2 = ((ho["HO"] + ho["RCH"]) * 1000.0).dropna()
    return t2[t2 > 0].values

def one(policy, cfg, chain, seed, T2, PROFILE):
    groups, fam, mutual = CONFIGS[cfg]
    P = os.path.join(PKI, fam)
    rng = np.random.default_rng(seed)
    n_out = int(DUR // OUT_EVERY_S) - 1
    t_base = time.monotonic() + 2.0          # stream starts ~2 s from now
    outf = f"{TMP}/x3_out_{os.getpid()}.txt"
    durs = rng.choice(T2, size=n_out)
    with open(outf, "w") as f:
        for i, d in enumerate(durs):
            a = t_base + OUT_EVERY_S * (i + 1) + rng.uniform(-1, 1)
            f.write(f"{a:.6f} {a + d / 1e3:.6f}\n")
    emu = subprocess.Popen(["ip", "netns", "exec", "rt", "python3", f"{HERE}/linkemu.py", "r0", "r1", "--ab-rate", str(PROFILE["ul"]), "--ba-rate", str(PROFILE["dl"]),
                            "--ab-delay-ms", str(PROFILE["owd_ms"]), "--ba-delay-ms", str(PROFILE["owd_ms"]), "--outages", outf, "--outages-abs"], stderr=open(f"{TMP}/x3_emu_{policy}_{cfg}_{chain}_{seed}.err", "w"))
    time.sleep(0.5)
    scert = f"{P}/srv.byroot.crt"; schain = f"{P}/srv.chain3.pem" if chain == 3 else "-"
    srv = subprocess.Popen(["ip", "netns", "exec", "srv", f"{HERE}/tele", "s", "4433", scert, f"{P}/srv.key", schain, f"{P}/root.crt", groups, str(mutual)],
                           stdout=open(f"{TMP}/x3_srv_{seed}.out", "w"), stderr=subprocess.PIPE, text=True)   # a file, not a pipe: 5,000 lines overflow a pipe and block the server
    srv.stderr.readline()
    if mutual:
        cc, ck = f"{P}/cli.byroot.crt", f"{P}/cli.key"; cch = f"{P}/cli.chain3.pem" if chain == 3 else "-"
    else:
        cc = ck = cch = "-"
    while time.monotonic() < t_base: time.sleep(0.01)
    cli = subprocess.run(["ip", "netns", "exec", "cli", f"{HERE}/tele", "c", "10.9.0.2", "4433", f"{P}/root.crt", groups, cc, ck, cch,
                          str(DUR), str(PERIOD_MS), policy, outf], capture_output=True, text=True, timeout=DUR + 120)
    if cli.returncode != 0: print("CLIENT", policy, cfg, chain, seed, cli.returncode, cli.stderr[-300:], flush=True)
    try: srv.wait(timeout=20)
    except subprocess.TimeoutExpired: srv.kill()
    sout = open(f"{TMP}/x3_srv_{seed}.out").read()
    emu.send_signal(signal.SIGINT)
    try: emu.wait(timeout=5)
    except subprocess.TimeoutExpired: emu.kill()
    subprocess.run(CLEANUP)
    R = [l.split() for l in sout.splitlines() if l.startswith("R ")]
    delay = np.array([(float(r[3]) - float(r[2])) * 1e3 for r in R])
    recv = np.array(sorted(float(r[3]) for r in R))
    K = [l.split() for l in cli.stdout.splitlines() if l.startswith("K ")]
    hs = [(float(k[3]) - float(k[2])) * 1e3 for k in K[1:]]   # re-establishments after outages (connection 0 is the cold start)
    reused = [int(k[4]) for k in K[1:]]
    win = [tuple(map(float, l.split())) for l in open(outf)]
    if len(delay) < 2:
        return {"seed": seed, "failed": True, "client_rc": cli.returncode, "client_err": cli.stderr[-300:], "outage_ms": [], "n_recv": 0, "n_miss": 0,
                "longest_gap_ms": float("nan"), "reestablish_ms": [], "delay_ms": {"p99": float("nan")}}
    expected = int(DUR * 1e3 / PERIOD_MS)
    return {"seed": seed, "outage_ms": [round((b - a) * 1e3, 1) for a, b in win], "n_expected": expected, "n_recv": int(len(delay)),
            "delay_ms": {"p50": float(np.median(delay)), "p99": float(np.percentile(delay, 99)), "max": float(delay.max())},
            "miss_share": float((delay > DEADLINE_MS).mean()), "n_miss": int((delay > DEADLINE_MS).sum()),
            "longest_gap_ms": float(np.diff(recv).max() * 1e3), "reestablish_ms": hs, "resumed": reused,
            "client_rc": cli.returncode, "client_err": cli.stderr[-300:]}

def main():
    subprocess.run(["bash", os.path.join(HERE, "netns_up.sh")], check=True, stdout=subprocess.DEVNULL)
    T2 = t2_nsa_ms()
    outp = os.path.join(ROOT, "results", "testbed_x3.json")
    res = {"setup": {"profiles": PROFILES, "period_ms": PERIOD_MS, "msg_B": 1000, "deadline_ms": DEADLINE_MS, "duration_s": DUR, "runs": RUNS,
                     "outage_every_s": OUT_EVERY_S, "outage_source": "NSA primary-cell T2 (HO+RCH), SIGCOMM'22 artifact, measured events",
                     "T2_pool_n": int(len(T2)), "T2_pool_median_ms": float(np.median(T2))}, "cells": {}}
    only = os.environ.get("X3_ONLY")            # e.g. X3_ONLY=resume reruns only those cells and merges them in
    if only and os.path.exists(outp):
        res["cells"] = json.load(open(outp))["cells"]
    for pname, PROFILE in PROFILES.items():
     for policy, cfg, ch in CELLS:
        if only and policy != only: continue
        key = f"{pname}|{policy}|{cfg}|ch{ch}"
        runs = [one(policy, cfg, ch, 20261015 + r, T2, PROFILE) for r in range(RUNS)]   # same seeds => same outages in every cell
        res["cells"][key] = {"runs": runs,
            "miss_share": sum(r["n_miss"] for r in runs) / max(1, sum(r["n_recv"] for r in runs)),
            "misses_per_outage": sum(r["n_miss"] for r in runs) / max(1, sum(len(r["outage_ms"]) for r in runs)),
            "longest_gap_ms_max": max(r["longest_gap_ms"] for r in runs),
            "reestablish_ms_median": (statistics.median([h for r in runs for h in r["reestablish_ms"]]) if any(r["reestablish_ms"] for r in runs) else None),
            "failed_runs": sum(1 for r in runs if r.get("failed") or r.get("client_rc", 0) != 0),
            "p99_ms": max(r["delay_ms"]["p99"] for r in runs)}
        c = res["cells"][key]
        print(key, {k: c[k] for k in ("miss_share", "misses_per_outage", "longest_gap_ms_max", "reestablish_ms_median", "p99_ms")},
              "lost:", [r["n_expected"] - r["n_recv"] for r in runs], "rc:", [r["client_rc"] for r in runs], flush=True)
        json.dump(res, open(outp, "w"), indent=1)

if __name__ == "__main__":
    main()
