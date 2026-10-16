"""
testbed_tables.py -- Table IV of the paper and results/testbed_summary.json, from the testbed results
(results/testbed_x12.json: TCP, X1/X2; testbed_x4.json: QUIC, X4; testbed_x3.json: telemetry through handovers, X3).
Handshake bytes are taken from the 5G-hosp runs (no retransmissions): all TCP payload of the first connection
except the client's 1,022-B application record and the server's 24-B close_notify.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(HERE, "..", "paper", "tables")
X12 = json.load(open(os.path.join(RES, "testbed_x12.json")))
X4 = json.load(open(os.path.join(RES, "testbed_x4.json")))
X3 = json.load(open(os.path.join(RES, "testbed_x3.json")))["cells"]
APP, CLOSE = 1022, 24

ROWS = [("C0", 2, "C0"), ("C1", 2, "C1"), ("C2", 2, "C2"), ("C2u", 2, "C2$'$"),
        ("C2", 3, "C2 + int."), ("C3", 2, "C3 (Falcon-512)"), ("C3", 3, "C3 + int.")]

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
        "quic_ms": {p: X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["median"] for p in ("5G-hosp", "5G-tele")},
        "quic_retry_ms": {p: X4[f"{p}|{cfg}|ch{ch}|retry"]["t_first_record_ms"]["median"] for p in ("5G-hosp", "5G-tele")},
        "n_tcp_5g": X12[f"5G-hosp|{cfg}|ch{ch}"]["n"], "n_quic": X4[f"5G-hosp|{cfg}|ch{ch}|noretry"]["n"]}
fq = X4["5G-hosp|C2|ch2|noretry"]["flights_first_conn"]
# model check: k RTTs (2.5 for TCP setup + handshake + first record, +1 per flight exceeding the 10-segment initial window)
# plus TCP/IP-framed bytes per direction over that direction's rate (66 B of headers per segment)
X12P = {k.split("|")[0]: v["profile"] for k, v in X12.items()}
err = {}
for cfg, ch, lab in ROWS:
    f = X12[f"5G-hosp|{cfg}|ch{ch}"]["flights_first_conn"]
    k_rtt = 2.5 + (f[1][2] > 10) + (f[2][2] > 10)
    cs = sum(x[1] + 66 * x[2] for x in f[:3] if x[0] == "C>S"); sc = sum(x[1] + 66 * x[2] for x in f[:3] if x[0] == "S>C")
    for p in ("5G-hosp", "5G-tele", "LTE-M", "NB-IoT"):
        pr = X12P[p]; model = k_rtt * 2 * pr["owd_ms"] + cs * 8 / pr["ul"] * 1e3 + sc * 8 / pr["dl"] * 1e3
        m = X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["median"]
        err[f"{p}|{cfg}|ch{ch}"] = {"model_ms": model, "meas_ms": m, "diff_ms": m - model, "rel": (m - model) / model, "k_rtt": k_rtt}
S["model_check"] = err
pq_slow = [v for k, v in err.items() if k.split("|")[0] in ("LTE-M", "NB-IoT") and k.split("|")[1] not in ("C0", "C1")]
S["model_check_summary"] = {"pq_constrained_max_abs_rel": max(abs(v["rel"]) for v in pq_slow),
                            "5g_diff_ms_range": [min(v["diff_ms"] for k, v in err.items() if k.startswith("5G")), max(v["diff_ms"] for k, v in err.items() if k.startswith("5G"))]}
S["quic_C2_first_bursts"] = {"client_B": fq[0][1], "server_B": fq[1][1], "ratio": fq[1][1] / fq[0][1]}
S["x3"] = {k: {"reestablish_ms_median": v["reestablish_ms_median"], "misses_per_outage": v["misses_per_outage"],
              "longest_gap_ms_max": v["longest_gap_ms_max"], "n_outages": sum(len(r["outage_ms"]) for r in v["runs"]),
              "failed_runs": v.get("failed_runs", 0)} for k, v in X3.items()}
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
print(json.dumps({k: (v["hs_bytes"], v["server_flight_B"], {p: round(t, 1) for p, t in v["tcp_ms"].items()}, {p: round(t, 1) for p, t in v["quic_ms"].items()}) for k, v in S["rows"].items()}, indent=0))
print(S["quic_C2_first_bursts"]); print(S["model_check_summary"])
for k, v in err.items(): print(k, round(v["meas_ms"], 1), round(v["model_ms"], 1), f"{100*v['rel']:+.1f}%", v["k_rtt"])
for k, v in S["x3"].items(): print(k, v)
