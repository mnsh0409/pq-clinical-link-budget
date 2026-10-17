"""
testbed_tables.py -- Tables IV and V of the ICC paper and results/testbed_summary.json, from the testbed results
(results/testbed_x12.json: TCP, X1/X2; testbed_x4.json: QUIC, X4; testbed_timeline.json: per-segment timeline of one
C2 and one C2 + intermediate connection; testbed_x3.json: telemetry through handover interruptions, X3).
Handshake bytes are taken from the 5G-hosp runs (no retransmissions): all TCP payload of the first connection
except the client's 1,022-B application record and the server's 24-B close_notify.
"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(HERE, "..", "paper", "tables")
X12 = json.load(open(os.path.join(RES, "testbed_x12.json")))
X4 = json.load(open(os.path.join(RES, "testbed_x4.json")))
X3 = json.load(open(os.path.join(RES, "testbed_x3.json")))
TL = json.load(open(os.path.join(RES, "testbed_timeline.json"))) if os.path.exists(os.path.join(RES, "testbed_timeline.json")) else None
APP, CLOSE = 1022, 24
ETH_IP_UDP = 14 + 20 + 8          # frame bytes in the X4 log minus these = UDP payload per datagram

ROWS = [("C0", 2, "C0"), ("C1", 2, "C1"), ("C2", 2, "C2"), ("C2u", 2, "C2$'$"),
        ("C2", 3, "C2 + int."), ("C3", 2, "C3"), ("C3", 3, "C3 + int."), ("C3m", 2, "C3m"), ("C3m", 3, "C3m + int.")]

def hs_bytes(cfg, ch):
    f = X12[f"5G-hosp|{cfg}|ch{ch}"]["flights_first_conn"]
    cs = sum(x[1] for x in f if x[0] == "C>S") - APP
    sc = sum(x[1] for x in f if x[0] == "S>C") - CLOSE
    server_flight = f[1][1]
    return cs + sc, server_flight, cs, sc

S = {"rows": {}}
for cfg, ch, lab in ROWS:
    tot, sf, cs, sc = hs_bytes(cfg, ch)
    k = f"{cfg}|ch{ch}"
    S["rows"][k] = {"label": lab, "hs_bytes": tot, "server_flight_B": sf, "client_B": cs, "server_B": sc,
        "tcp_ms": {p: X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["median"] for p in ("5G-hosp", "5G-tele", "LTE-M", "NB-IoT")},
        "tcp_p10_p90_ms": {p: [X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["p10"], X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["p90"]] for p in ("5G-hosp", "5G-tele")},
        "quic_ms": {p: X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["median"] for p in ("5G-hosp", "5G-tele")},
        "quic_p10_p90_ms": {p: [X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["p10"], X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["p90"]] for p in ("5G-hosp", "5G-tele")},
        "quic_retry_ms": {p: X4[f"{p}|{cfg}|ch{ch}|retry"]["t_first_record_ms"]["median"] for p in ("5G-hosp", "5G-tele")},
        "n_tcp_5g": X12[f"5G-hosp|{cfg}|ch{ch}"]["n"], "n_quic": X4[f"5G-hosp|{cfg}|ch{ch}|noretry"]["n"]}
# spread of the 5G cells of Table IV (p90 - p10 of the time to the first record)
spr = [v["tcp_p10_p90_ms"]["5G-hosp"][1] - v["tcp_p10_p90_ms"]["5G-hosp"][0] for v in S["rows"].values()] + \
      [v["quic_p10_p90_ms"]["5G-hosp"][1] - v["quic_p10_p90_ms"]["5G-hosp"][0] for v in S["rows"].values()]
S["spread_5g_hosp_p10_p90_max_ms"] = max(spr)
S["spread_5g_hosp_p10_p90_tcp_max_ms"] = max(spr[:len(S["rows"])]); S["spread_5g_hosp_p10_p90_quic_max_ms"] = max(spr[len(S["rows"]):])

# QUIC, C2 without Retry: first bursts of the first connection, in UDP payload bytes
fq = X4["5G-hosp|C2|ch2|noretry"]["flights_first_conn"]
udp = lambda f: f[1] - ETH_IP_UDP * f[2]
S["quic_C2_first_bursts"] = {"client_initial_udp_B": udp(fq[0]), "client_initial_datagrams": fq[0][2],
                             "server_first_udp_B": udp(fq[1]), "server_first_datagrams": fq[1][2], "server_first_t_ms": fq[1][3],
                             "client_next_udp_B": udp(fq[2]), "client_next_t_ms": fq[2][3],
                             "server_rest_udp_B": udp(fq[3]), "server_rest_datagrams": fq[3][2], "server_rest_t_ms": fq[3][3],
                             "ratio_server_first_to_client_initial": udp(fq[1]) / udp(fq[0])}

# model check: k RTTs (2.5 for TCP setup + handshake + first record, +1 per flight exceeding the 10-segment initial window)
# plus TCP/IP-framed bytes per direction over that direction's rate (66 B of headers per segment)
X12P = {k.split("|")[0]: v["profile"] for k, v in X12.items()}
err = {}
for cfg, ch, lab in ROWS:
    f = X12[f"5G-hosp|{cfg}|ch{ch}"]["flights_first_conn"]
    k_rtt = 2.5 + (f[1][2] > 10) + (f[2][2] > 10)
    cs = sum(x[1] + 66 * x[2] for x in f[:3] if x[0] == "C>S"); sc = sum(x[1] + 66 * x[2] for x in f[:3] if x[0] == "S>C")
    for p in ("5G-hosp", "5G-tele", "LTE-M", "NB-IoT"):
        pr = X12P[p]; up = cs * 8 / pr["ul"] * 1e3; down = sc * 8 / pr["dl"] * 1e3; rtt = k_rtt * 2 * pr["owd_ms"]
        model = rtt + up + down
        m = X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["median"]
        err[f"{p}|{cfg}|ch{ch}"] = {"model_ms": model, "meas_ms": m, "diff_ms": m - model, "rel": (m - model) / model, "k_rtt": k_rtt,
                                   "up_framed_B": cs, "down_framed_B": sc, "up_ms": up, "down_ms": down, "rtt_ms": rtt}
S["model_check"] = err
pq_slow = [v for k, v in err.items() if k.split("|")[0] in ("LTE-M", "NB-IoT") and k.split("|")[1] not in ("C0", "C1")]
S["model_check_summary"] = {"pq_constrained_max_abs_rel": max(abs(v["rel"]) for v in pq_slow),
                            "5g_diff_ms_range": [min(v["diff_ms"] for k, v in err.items() if k.startswith("5G")), max(v["diff_ms"] for k, v in err.items() if k.startswith("5G"))]}

# TCP timeline (testbed/timeline.py): bursts of each data flight of one connection
if TL: S["timeline"] = TL

# X3: paired telemetry experiment
cells = X3["cells"]; rng = np.random.default_rng(20261017)
QCF = os.path.join(RES, "testbed_x3_qc.json")
QC = json.load(open(QCF)) if os.path.exists(QCF) else None          # testbed/x3_qc.py: windows with a host stall
def valid(key, c):
    """Per interruption window: True unless testbed/x3_qc.py marked it (emulator stall or false detection)."""
    if QC is None: return np.ones(len(c["late_per_outage"]), bool)
    q = QC["cells"][key]
    return np.array([not v for r in c["runs"] for v in q[str(r["seed"])]["invalid"]], bool)
def boot_means(late, ok, n_runs, n=10000):
    """Bootstrap distribution of a cell's mean late count over its valid interruptions: resample runs, then the
    valid interruptions within each resampled run (two stages, so the grouping into runs is respected)."""
    d = np.asarray(late, float).reshape(n_runs, -1); m = np.asarray(ok, bool).reshape(n_runs, -1)
    g = [d[i][m[i]] for i in range(n_runs) if m[i].any()]
    means = np.empty(n)
    for b in range(n):
        tot = cnt = 0.0
        for i in rng.integers(0, len(g), size=len(g)):
            x = g[i][rng.integers(0, len(g[i]), size=len(g[i]))]; tot += x.sum(); cnt += len(x)
        means[b] = tot / cnt
    return means
S["x3"] = {"setup": {k: v for k, v in X3["setup"].items() if k != "profiles"}, "cells": {},
           "qc": None if QC is None else {"stall_ms": QC["stall_ms"], "rule": "a window is invalid if the emulator delivered a frame more than stall_ms late or the client opened a new connection while its current one was alive (testbed/x3_qc.py)"}}
for prof in ("5G-hosp", "5G-tele"):
    kk = f"{prof}|keep|C2|ch2"; keep = cells.get(kk)
    if keep is not None and "late_per_outage" not in keep: keep = None
    for key, c in cells.items():
        if not key.startswith(prof + "|") or "late_per_outage" not in c: continue
        per = [x for r in c["runs"] for x in r.get("per_outage", [])]
        ok = valid(key, c); late = np.array(c["late_per_outage"], float)
        pv = [x for x, o in zip(per, ok) if o]
        rec = [x["resume_delivery_ms"] for x in pv if x["resume_delivery_ms"] == x["resume_delivery_ms"]]
        det = [x["detect_ms"] for x in pv if x["detect_ms"] is not None]; hs = [x["handshake_ms"] for x in pv if x["handshake_ms"] is not None]
        res_ = [x["resumed"] for x in pv if x["resumed"] is not None]
        e = {"n_interruptions": len(per), "n_valid": int(ok.sum()), "late_per_interruption": float(late[ok].mean()), "late_total": int(late[ok].sum()),
             "late_per_interruption_all_windows": float(late.mean()),
             "late_outside_outages": c.get("late_outside_outages", 0), "lost": c["lost"], "dup": c["dup"],
             "resume_delivery_ms_median": float(np.median(rec)) if rec else None, "resume_delivery_ms_p90": float(np.percentile(rec, 90)) if rec else None,
             "gap_ms_max": c["gap_ms_max"], "detect_ms_median": float(np.median(det)) if det else None, "handshake_ms_median": float(np.median(hs)) if hs else None,
             "failed_attempts_per_interruption": float(np.mean([x["failed_attempts"] for x in pv])) if pv else None, "failed_runs": c["failed_runs"],
             "resumed_share": (float(np.mean(res_)) if res_ else None) if key.split("|")[1].endswith("resume") else None,
             "outage_ms_median": float(np.median([x["outage_ms"] for x in per])) if per else None,
             "outage_ms_max": float(np.max([x["outage_ms"] for x in per])) if per else None,
             "late_given_failed_attempt": float(np.mean([x["late"] for x in pv if x["failed_attempts"] > 0])) if any(x["failed_attempts"] > 0 for x in pv) else None,
             "late_given_no_failed_attempt": float(np.mean([x["late"] for x in pv if x["failed_attempts"] == 0])) if any(x["failed_attempts"] == 0 for x in pv) else None}
        if QC is not None and "|keep|" not in key:
            syn = [v for r in c["runs"] for v in QC["cells"][key][str(r["seed"])]["syn_dropped_in_interruption"]]
            e["failed_attempts_valid"] = int(sum(x["failed_attempts"] for x, o in zip(per, ok) if o))
            e["syn_dropped_in_interruption_valid"] = int(sum(v for v, o in zip(syn, ok) if o))
        if keep is not None and key != kk:
            assert [r["seed"] for r in c["runs"]] == [r["seed"] for r in keep["runs"]]          # same interruption draws in both cells
            okk = valid(kk, keep); lk = np.array(keep["late_per_outage"], float)
            # excess = difference of the two cells' means over their own valid interruptions, so Lost - Kept = excess
            # exactly; 95 % interval from independent two-stage bootstraps of the two cells
            dm = boot_means(late, ok, len(c["runs"])) - boot_means(lk, okk, len(keep["runs"]))
            e["excess_over_keep"] = float(late[ok].mean() - lk[okk].mean())
            e["excess_over_keep_ci95"] = [float(np.percentile(dm, 2.5)), float(np.percentile(dm, 97.5))]
            e["excess_over_keep_all_windows"] = float(late.mean() - lk.mean())
        S["x3"]["cells"][key] = e
if QC is not None:
    _l = [e for k, e in S["x3"]["cells"].items() if "|keep|" not in k]
    S["x3"]["failed_attempts_valid_total"] = sum(e["failed_attempts_valid"] for e in _l)
    S["x3"]["syn_dropped_in_interruption_valid_total"] = sum(e["syn_dropped_in_interruption_valid"] for e in _l)
    S["x3"]["windows_total"] = sum(e["n_interruptions"] for e in S["x3"]["cells"].values())
    S["x3"]["windows_invalid"] = sum(e["n_interruptions"] - e["n_valid"] for e in S["x3"]["cells"].values())
json.dump(S, open(os.path.join(RES, "testbed_summary.json"), "w"), indent=1)

def ms(x):
    return f"{x/1e3:.2f}\\,s" if x >= 1000 else f"{x:.0f}" if x >= 100 else f"{x:.1f}"
L = [r"\begin{tabular}{@{}lrrrrrr@{}}\toprule",
     r" & \multicolumn{2}{c}{Bytes} & \multicolumn{4}{c}{Time to first record (ms)} \\ \cmidrule(lr){2-3}\cmidrule(l){4-7}",
     r"Config. & server & total & 5G TCP & 5G QUIC & LTE-M & NB-IoT \\ \midrule"]
for cfg, ch, lab in ROWS:
    r = S["rows"][f"{cfg}|ch{ch}"]
    L.append(f"{lab} & {r['server_flight_B']:,} & {r['hs_bytes']:,} & {ms(r['tcp_ms']['5G-hosp'])} & {ms(r['quic_ms']['5G-hosp'])} & "
             f"{ms(r['tcp_ms']['LTE-M'])} & {ms(r['tcp_ms']['NB-IoT'])} \\\\")
L.append(r"\bottomrule\end{tabular}")
open(os.path.join(OUT, "tab4_testbed.tex"), "w").write("\n".join(L) + "\n")
print("\n".join(L))

# Table V: the paired telemetry experiment
X5 = [("keep", "C2", 2, "Kept (no handshake)"), ("detect", "C0", 2, "Lost, C0"), ("detect", "C1", 2, "Lost, C1"), ("detect", "C2", 2, "Lost, C2"),
      ("detect", "C2", 3, "Lost, C2 + int."), ("detect", "C3m", 3, "Lost, C3m + int."), ("detect-resume", "C2", 3, "Resumed, C2 + int.")]
def f2(x): return "--" if x is None else f"{x:.2f}"
def f0(x): return "--" if x is None else f"{x:.0f}"
L = [r"\begin{tabular}{@{}lrrrr@{}}\toprule",
     r" & \multicolumn{2}{c}{Late per interruption} & \multicolumn{2}{c}{Excess over kept [95\,\% CI]} \\ \cmidrule(lr){2-3}\cmidrule(l){4-5}",
     r"Session, config. & 10\,ms & 18\,ms & 10\,ms & 18\,ms \\ \midrule"]
def exc(e): return "--" if "excess_over_keep" not in e else f"{e['excess_over_keep']:.2f} [{e['excess_over_keep_ci95'][0]:.2f}, {e['excess_over_keep_ci95'][1]:.2f}]"
for pol, cfg, ch, lab in X5:
    a = S["x3"]["cells"].get(f"5G-hosp|{pol}|{cfg}|ch{ch}"); b = S["x3"]["cells"].get(f"5G-tele|{pol}|{cfg}|ch{ch}")
    if a is None or b is None: continue
    L.append(f"{lab} & {f2(a['late_per_interruption'])} & {f2(b['late_per_interruption'])} & {exc(a)} & {exc(b)} \\\\")
L.append(r"\bottomrule\end{tabular}")
open(os.path.join(OUT, "tab5_session.tex"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
print(json.dumps(S["quic_C2_first_bursts"])); print(S["model_check_summary"], S["spread_5g_hosp_p10_p90_max_ms"])
for k, v in err.items(): print(k, round(v["meas_ms"], 1), round(v["model_ms"], 1), f"{100*v['rel']:+.1f}%", v["k_rtt"])
for k, v in S["x3"]["cells"].items(): print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()})
