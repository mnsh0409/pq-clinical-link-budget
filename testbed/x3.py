"""
x3.py -- telemetry through handover outages (X3). Results -> results/testbed_x3.json.

Stream: 1,000-B message every 16 ms (= 0.5 Mb/s, the TR 22.826 cardiac-telemetry target), deadline 100 ms.
Links: 5G-hosp (10 ms RTT) and 5G-tele (18 ms RTT) profiles (ledger rates). Outages: one every OUT_EVERY_S seconds
(+-1 s), duration drawn (seeded) from the measured NSA primary-cell execution-stage interruptions T2 of the SIGCOMM'22
artifact (the same events as Fig. 2a); the same seeds give the same outages in every cell (paired design).
Cells: policy x configuration. keep = the session survives the outage (TCP recovers); detect = the session is lost
at the outage start (the emulator kills the old connection) and the client finds out only from missing application
acknowledgments (tele.c), reconnects and resends; detect-resume = detect with PSK resumption.
Records: generated every PERIOD_MS at the client (generation time = schedule), queued while no session exists, late if
first received more than DEADLINE_MS after generation, lost if never received.
usage: python3 x3.py [RUNS] [DURATION_S]
"""
import json, os, signal, statistics, subprocess, sys, time
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "models"))
from common import p
from run import CONFIGS, PKI, TMP, CLEANUP, env_for

RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 5
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
PERIOD_MS = 16.0
DEADLINE_MS = p("telemetry_latency_ms")
OUT_EVERY_S = 10.0
PROFILES = {"5G-hosp": {"name": "5G-hosp", "ul": p("ul_5gsa_chen2024_avg_bps"), "dl": p("dl_5gsa_chen2024_avg_bps"), "owd_ms": p("rtt_5g_berlet2022_ms") / 2},
            "5G-tele": {"name": "5G-tele", "ul": p("ul_5g_ye2026_bps"), "dl": p("dl_5g_ye2026_bps"), "owd_ms": p("rtt_5g_moustris2023_ms") / 2}}
PROFILE = PROFILES["5G-hosp"]
CELLS = [("keep", "C2", 2), ("detect", "C0", 2), ("detect", "C1", 2), ("detect", "C2", 2), ("detect", "C2", 3), ("detect", "C3m", 3),
         ("detect-resume", "C2", 3)]
if os.environ.get("X3_CELLS"):                 # e.g. X3_CELLS="detect:C2:2,keep:C2:2"
    CELLS = [(c.split(":")[0], c.split(":")[1], int(c.split(":")[2])) for c in os.environ["X3_CELLS"].split(",")]

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
    kill = ["--kill-flows"] if policy.startswith("detect") else []
    elog = f"{TMP}/x3_emu_{PROFILE['name']}_{policy}_{cfg}_{chain}_{seed}.log"
    emu = subprocess.Popen(["ip", "netns", "exec", "rt", "python3", f"{HERE}/linkemu.py", "r0", "r1", "--ab-rate", str(PROFILE["ul"]), "--ba-rate", str(PROFILE["dl"]),
                            "--ab-delay-ms", str(PROFILE["owd_ms"]), "--ba-delay-ms", str(PROFILE["owd_ms"]), "--outages", outf, "--outages-abs", "--log", elog] + kill,
                           stderr=open(f"{TMP}/x3_emu_{policy}_{cfg}_{chain}_{seed}.err", "w"))
    env = env_for(fam)
    time.sleep(0.5)
    scert = f"{P}/srv.byroot.crt"; schain = f"{P}/srv.chain3.pem" if chain == 3 else "-"
    srv = subprocess.Popen(["ip", "netns", "exec", "srv", f"{HERE}/tele", "s", "4433", scert, f"{P}/srv.key", schain, f"{P}/root.crt", groups, str(mutual)],
                           stdout=open(f"{TMP}/x3_srv_{seed}.out", "w"), stderr=subprocess.PIPE, text=True, env=env)   # a file, not a pipe: 5,000 lines overflow a pipe and block the server
    srv.stderr.readline()
    if mutual:
        cc, ck = f"{P}/cli.byroot.crt", f"{P}/cli.key"; cch = f"{P}/cli.chain3.pem" if chain == 3 else "-"
    else:
        cc = ck = cch = "-"
    while time.monotonic() < t_base: time.sleep(0.01)
    cli = subprocess.run(["ip", "netns", "exec", "cli", f"{HERE}/tele", "c", "10.9.0.2", "4433", f"{P}/root.crt", groups, cc, ck, cch,
                          str(DUR), str(PERIOD_MS), policy, outf], capture_output=True, text=True, timeout=DUR + 120, env=env)
    if cli.returncode != 0: print("CLIENT", policy, cfg, chain, seed, cli.returncode, cli.stderr[-300:], flush=True)
    try: srv.wait(timeout=20)
    except subprocess.TimeoutExpired: srv.kill()
    sout = open(f"{TMP}/x3_srv_{seed}.out").read()
    emu.send_signal(signal.SIGINT)
    try: emu.wait(timeout=5)
    except subprocess.TimeoutExpired: emu.kill()
    subprocess.run(CLEANUP)
    R = [l.split() for l in sout.splitlines() if l.startswith("R ")]
    win = [tuple(map(float, l.split())) for l in open(outf)]
    expected = int(np.ceil(DUR * 1e3 / PERIOD_MS - 1e-9))   # the client generates at t0, t0 + period, ... while < t0 + DUR
    if len(R) < 2:
        return {"seed": seed, "failed": True, "client_rc": cli.returncode, "client_err": cli.stderr[-300:], "outage_ms": [], "n_expected": expected,
                "n_recv": 0, "n_miss": 0, "longest_gap_ms": float("nan"), "delay_ms": {"p99": float("nan")}, "per_outage": []}
    first, dup = {}, 0
    for r in R:                                   # first receipt per sequence number (resent messages may arrive twice)
        sq = int(r[1])
        if sq in first: dup += 1; continue
        first[sq] = (float(r[2]), float(r[3]), int(r[4]))
    keys = sorted(first)
    tg = np.array([first[k][0] for k in keys]); tr = np.array([first[k][1] for k in keys])
    delay = (tr - tg) * 1e3
    late = delay > DEADLINE_MS
    trs = np.sort(tr)
    K = [l.split() for l in cli.stdout.splitlines() if l.startswith("K ")]
    D = [float(l.split()[1]) for l in cli.stdout.splitlines() if l.startswith("D ")]
    F = [float(l.split()[1]) for l in cli.stdout.splitlines() if l.startswith("F ")]
    per = []
    for i, (oa, ob) in enumerate(win):           # attribute by generation time: from 0.5 s before this outage to 0.5 s before the next
        lo = oa - 0.5; hi = win[i + 1][0] - 0.5 if i + 1 < len(win) else float("inf")
        m = (tg >= lo) & (tg < hi)
        after = trs[trs > ob]
        rec = (after[0] - ob) * 1e3 if len(after) else float("nan")
        seg = trs[(trs >= oa - 0.5) & (trs < oa + 2.0)]
        gap = float(np.diff(seg).max() * 1e3) if len(seg) > 1 else float("nan")
        det = [(d - oa) * 1e3 for d in D if oa <= d < oa + 2.0]
        hs = [((float(k[3]) - float(k[2])) * 1e3, int(k[4])) for k in K[1:] if oa <= float(k[2]) < hi + 0.5]
        per.append({"outage_ms": round((ob - oa) * 1e3, 1), "late": int(late[m].sum()), "n_gen": int(m.sum()),
                    "resume_delivery_ms": rec, "gap_ms": gap, "detect_ms": det[0] if det else None,
                    "handshake_ms": hs[0][0] if hs else None, "resumed": hs[0][1] if hs else None,
                    "failed_attempts": sum(1 for f in F if oa <= f < hi)})
    late_outside = int(late.sum()) - sum(x["late"] for x in per)
    return {"seed": seed, "outage_ms": [x["outage_ms"] for x in per], "n_expected": expected, "n_recv": len(first), "n_dup": dup,
            "n_lost": expected - len(first), "delay_ms": {"p50": float(np.median(delay)), "p99": float(np.percentile(delay, 99)), "max": float(delay.max())},
            "n_miss": int(late.sum()), "late_outside_outages": late_outside, "miss_share": float(late.mean()),
            "longest_gap_ms": float(np.diff(trs).max() * 1e3), "per_outage": per, "n_detect": len(D), "n_failed_attempts": len(F),
            "client_rc": cli.returncode, "client_err": cli.stderr[-300:]}

def main():
    subprocess.run(["bash", os.path.join(HERE, "netns_up.sh")], check=True, stdout=subprocess.DEVNULL)
    T2 = t2_nsa_ms()
    outp = os.path.join(ROOT, "results", "testbed_x3.json")
    res = {"setup": {"profiles": PROFILES, "period_ms": PERIOD_MS, "msg_B": 1000, "deadline_ms": DEADLINE_MS, "duration_s": DUR, "runs": RUNS,
                     "outage_every_s": OUT_EVERY_S, "outage_source": "NSA primary-cell T2 (HO+RCH), SIGCOMM'22 artifact, measured events",
                     "T2_pool_n": int(len(T2)), "T2_pool_median_ms": float(np.median(T2)),
                     "detect_rule": "session declared lost when the oldest unacknowledged message has waited one probe timeout, srtt + max(4 rttvar, 1 ms) + 25 ms (RFC 9002 form, application-acknowledgment RTT samples, Karn); connect and handshake bounded by the same timeout, then retried; unacknowledged messages resent",
                     "session_loss": "emulator --kill-flows: connections seen before an outage start are dropped from then on",
                     "attribution": "late messages assigned to the outage whose window [start - 0.5 s, next start - 0.5 s) contains their generation time"}, "cells": {}}
    only = os.environ.get("X3_ONLY")            # e.g. X3_ONLY=detect reruns only those cells and merges them in
    outp = os.environ.get("X3_OUT", outp)
    if (only or os.environ.get("X3_MERGE")) and os.path.exists(outp):
        res["cells"] = json.load(open(outp))["cells"]
    for pname, PROFILE in PROFILES.items():
     if os.environ.get("X3_PROFILES") and pname not in os.environ["X3_PROFILES"].split(","): continue
     for policy, cfg, ch in CELLS:
        if only and policy != only: continue
        key = f"{pname}|{policy}|{cfg}|ch{ch}"
        runs = [one(policy, cfg, ch, 20261015 + r, T2, PROFILE) for r in range(RUNS)]   # same seeds => same outage durations in every cell
        per = [x for r in runs for x in r.get("per_outage", [])]
        med = lambda v: statistics.median(v) if v else None
        res["cells"][key] = {"policy": policy, "cfg": cfg, "chain": ch, "runs": runs,
            "late_per_outage": [x["late"] for x in per],
            "misses_per_outage": sum(x["late"] for x in per) / max(1, len(per)),
            "late_outside_outages": sum(r.get("late_outside_outages", 0) for r in runs),
            "lost": sum(r.get("n_lost", 0) for r in runs), "dup": sum(r.get("n_dup", 0) for r in runs),
            "gap_ms_max": max((x["gap_ms"] for x in per if x["gap_ms"] == x["gap_ms"]), default=None),
            "resume_delivery_ms_median": med([x["resume_delivery_ms"] for x in per if x["resume_delivery_ms"] == x["resume_delivery_ms"]]),
            "detect_ms_median": med([x["detect_ms"] for x in per if x["detect_ms"] is not None]),
            "handshake_ms_median": med([x["handshake_ms"] for x in per if x["handshake_ms"] is not None]),
            "resumed_share": (sum(1 for x in per if x["resumed"]) / max(1, sum(1 for x in per if x["resumed"] is not None))) if policy.endswith("resume") else None,
            "failed_attempts": sum(r.get("n_failed_attempts", 0) for r in runs),
            "failed_runs": sum(1 for r in runs if r.get("failed") or r.get("client_rc", 0) != 0),
            "p99_ms": max(r["delay_ms"]["p99"] for r in runs)}
        c = res["cells"][key]
        print(key, {k: c[k] for k in ("misses_per_outage", "lost", "dup", "gap_ms_max", "resume_delivery_ms_median", "detect_ms_median", "handshake_ms_median", "failed_attempts", "failed_runs")}, flush=True)
        json.dump(res, open(outp, "w"), indent=1)

if __name__ == "__main__":
    main()
