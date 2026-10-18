"""
testbed_tables.py -- Tables III and IV of the ICC paper and results/testbed_summary.json, from the testbed results
(results/testbed_x12.json: TCP, X1/X2; testbed_x4.json: QUIC, X4; testbed_timeline.json: per-segment timeline of one
C2 and one C2 + intermediate connection; testbed_x3.json: telemetry through handover interruptions, X3).
Handshake bytes are taken from the 5G-hosp runs (no retransmissions): all TCP payload of the first connection
except the client's 1,022-B application record and the server's 24-B close_notify.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import x3_model as M                                   # a-priori model of X3 (no parameter from the telemetry runs)
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(HERE, "..", "paper", "tables")
X12 = json.load(open(os.path.join(RES, "testbed_x12.json")))
X4 = json.load(open(os.path.join(RES, "testbed_x4.json")))
X3 = json.load(open(os.path.join(RES, "testbed_x3.json")))
TL = json.load(open(os.path.join(RES, "testbed_timeline.json"))) if os.path.exists(os.path.join(RES, "testbed_timeline.json")) else None
APP, CLOSE = 1022, 24
ETH_IP_UDP = 14 + 20 + 8          # frame bytes in the X4 log minus these = UDP payload per datagram

ROWS = [("C0", 2, "C0"), ("C1", 2, "C1"), ("C2", 2, "C2"), ("C2u", 2, "C2$'$"),
        ("C2", 3, "C2 + int."), ("C2w", 3, "C2 + int., IW\\,20"), ("C3", 2, "C3"), ("C3", 3, "C3 + int."), ("C3m", 2, "C3m"), ("C3m", 3, "C3m + int.")]
NO_QUIC = {"C2w"}        # the initial-window case is a TCP setting; its QUIC column is not applicable

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
        "quic_ms": {p: (None if cfg in NO_QUIC else X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["median"]) for p in ("5G-hosp", "5G-tele")},
        "quic_p10_p90_ms": {p: (None if cfg in NO_QUIC else [X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["p10"], X4[f"{p}|{cfg}|ch{ch}|noretry"]["t_first_record_ms"]["p90"]]) for p in ("5G-hosp", "5G-tele")},
        "quic_retry_ms": {p: (None if cfg in NO_QUIC else X4[f"{p}|{cfg}|ch{ch}|retry"]["t_first_record_ms"]["median"]) for p in ("5G-hosp", "5G-tele")},
        "n_tcp_5g": X12[f"5G-hosp|{cfg}|ch{ch}"]["n"], "n_quic": None if cfg in NO_QUIC else X4[f"5G-hosp|{cfg}|ch{ch}|noretry"]["n"],
        "tcp_p10_p90_ms_all": {p: [X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["p10"], X12[f"{p}|{cfg}|ch{ch}"]["t_first_record_ms"]["p90"]] for p in ("5G-hosp", "5G-tele", "LTE-M", "NB-IoT")}}
# spread of the 5G cells of Table III (p90 - p10 of the time to the first record)
spr_t = [v["tcp_p10_p90_ms"]["5G-hosp"][1] - v["tcp_p10_p90_ms"]["5G-hosp"][0] for v in S["rows"].values()]
spr_q = [v["quic_p10_p90_ms"]["5G-hosp"][1] - v["quic_p10_p90_ms"]["5G-hosp"][0] for v in S["rows"].values() if v["quic_p10_p90_ms"]["5G-hosp"]]
S["spread_5g_hosp_p10_p90_max_ms"] = max(spr_t + spr_q)
S["spread_5g_hosp_p10_p90_tcp_max_ms"] = max(spr_t); S["spread_5g_hosp_p10_p90_quic_max_ms"] = max(spr_q)

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
    iw = 20 if cfg == "C2w" else 10
    k_rtt = 2.5 + (f[1][2] > iw) + (f[2][2] > iw)
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
    """Per interruption window: True unless testbed/x3_qc.py marked it invalid (emulator stall)."""
    if QC is None: return np.ones(len(c["late_per_outage"]), bool)
    q = QC["cells"][key]
    return np.array([not v for r in c["runs"] for v in q[str(r["seed"])]["invalid"]], bool)
def boot_means(late, ok, n_runs, n=10000):
    """Bootstrap distribution of the mean of `late` over the interruptions marked `ok`: resample runs (the independent
    replicates), then the ok interruptions within each resampled run (two stages, so the grouping into runs is respected).
    Given a per-interruption difference between two cells and the interruptions valid in both, it is the paired bootstrap
    of the contrast: both cells are resampled together, because the difference is formed per interruption."""
    d = np.asarray(late, float).reshape(n_runs, -1); m = np.asarray(ok, bool).reshape(n_runs, -1)
    g = [d[i][m[i]] for i in range(n_runs) if m[i].any()]
    means = np.empty(n)
    for b in range(n):
        tot = cnt = 0.0
        for i in rng.integers(0, len(g), size=len(g)):
            x = g[i][rng.integers(0, len(g[i]), size=len(g[i]))]; tot += x.sum(); cnt += len(x)
        means[b] = tot / cnt
    return means
T975_DF4 = 2.7764451051977987      # Student t, 97.5th percentile, 4 degrees of freedom (five runs)
T975 = {4: T975_DF4, 9: 2.2621571627409915}   # v1.9: also 9 degrees of freedom (the ten runs of the controlled repeat)
REF = "detect|C0|ch2"               # lost session, classical C0: shares the detector and retry policy of every lost cell
S["x3"] = {"setup": {k: v for k, v in X3["setup"].items() if k != "profiles"}, "cells": {},
           "contrast": "per interruption, late in a cell minus late in lost C0 on the same interruption (same seed and index); "
                       "mean over the interruptions valid in both cells; 95 % CI from a paired two-stage bootstrap (runs, then "
                       "interruptions, 10,000 replicates); also over all interruptions, and a t-interval over the five run means",
           "qc": None if QC is None else {"stall_ms": QC["stall_ms"], "rule": "a window is invalid if the emulator delivered a frame more than stall_ms late (testbed/x3_qc.py)"}}
for prof in ("5G-hosp", "5G-tele"):
    kr = f"{prof}|{REF}"; ref = cells.get(kr)
    if ref is not None and "late_per_outage" not in ref: ref = None
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
        if ref is not None and key != kr:
            assert [r["seed"] for r in c["runs"]] == [r["seed"] for r in ref["runs"]]            # same interruption draws in both cells
            okr = valid(kr, ref); lr = np.array(ref["late_per_outage"], float)
            nr = len(c["runs"]); d = late - lr; both = ok & okr                                  # paired: same seed, same interruption index
            bd = boot_means(d, both, nr); ba = boot_means(d, np.ones_like(both), nr)
            rm = np.array([dd[bb].mean() for dd, bb in zip(d.reshape(nr, -1), both.reshape(nr, -1)) if bb.any()])
            hw = T975_DF4 * rm.std(ddof=1) / np.sqrt(len(rm))
            e["diff_from_lost_c0"] = float(d[both].mean())
            e["diff_from_lost_c0_ci95"] = [float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5))]
            e["n_common_with_lost_c0"] = int(both.sum())
            e["diff_from_lost_c0_all_windows"] = float(d.mean())
            e["diff_from_lost_c0_all_windows_ci95"] = [float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))]
            e["diff_from_lost_c0_run_t_ci95"] = [float(rm.mean() - hw), float(rm.mean() + hw)]
            e["diff_from_lost_c0_run_means"] = [float(x) for x in rm]
        S["x3"]["cells"][key] = e
if QC is not None:
    _l = [e for k, e in S["x3"]["cells"].items() if "|keep|" not in k]
    S["x3"]["failed_attempts_valid_total"] = sum(e["failed_attempts_valid"] for e in _l)
    S["x3"]["syn_dropped_in_interruption_valid_total"] = sum(e["syn_dropped_in_interruption_valid"] for e in _l)
    S["x3"]["windows_total"] = sum(e["n_interruptions"] for e in S["x3"]["cells"].values())
    S["x3"]["windows_invalid"] = sum(e["n_interruptions"] - e["n_valid"] for e in S["x3"]["cells"].values())
    _c = [e["n_common_with_lost_c0"] for e in S["x3"]["cells"].values() if "n_common_with_lost_c0" in e]
    S["x3"]["n_common_with_lost_c0_range"] = [min(_c), max(_c)]
    for _pr in ("5G-hosp", "5G-tele"):              # share of valid lost-session intervals whose loss was declared before the interruption ended
        _dv = []
        for k, c in cells.items():
            if not k.startswith(_pr + "|detect"): continue
            _ok = valid(k, c); _per = [x for r in c["runs"] for x in r["per_outage"]]
            _dv += [x["detect_ms"] < x["outage_ms"] for x, o in zip(_per, _ok) if o and x["detect_ms"] is not None]
        S["x3"].setdefault("detect_before_end_share", {})[_pr] = float(np.mean(_dv))
    _o = [q["client_start_after_origin_ms"] for v in QC["cells"].values() for q in v.values() if "client_start_after_origin_ms" in q]
    if _o: S["x3"]["client_start_after_origin_ms_range"] = [min(_o), max(_o)]
# ---------------------------------------------------------------- model of X3 (models/x3_model.py)
PROF = {"5G-hosp": (10.0, 5.0), "5G-tele": (18.0, 9.0)}           # RTT, one-way delay (ms)
def H_of(prof, pol, cfg, ch):
    """Cold connect-to-first-record time of the configuration on the profile (Table III); a resumed session has the
    round trips of C0 (PSK and key share, no certificates), so C0's time stands in for it."""
    return S["rows"]["C0|ch2"]["tcp_ms"][prof] if pol == "detect-resume" else S["rows"][f"{cfg}|ch{ch}"]["tcp_ms"][prof]
def model_cells(x3, qc, tag, filed=None):
    """Per lost-session cell: observed and model-expected late count per interruption over the valid intervals.
    filed: {cell key: per-interruption expectations filed before the runs}; used instead of recomputing when given."""
    out = {}
    for key, c in x3["cells"].items():
        prof, pol, cfg, ch = key.split("|"); ch = int(ch[2:])
        if not pol.startswith("detect"): continue
        rtt, owd = PROF[prof]; H = H_of(prof, pol, cfg, ch)
        ok = np.array([not v for r in c["runs"] for v in qc["cells"][key][str(r["seed"])]["invalid"]], bool)
        per = [x for r in c["runs"] for x in r["per_outage"]]
        ex = [M.late_expect(x["outage_ms"], H, rtt, owd) for x in per]
        obs = np.array([x["late"] for x in per], float); pre = np.array([e[0] for e in ex])
        if filed is not None:       # the filed predictions (4 decimals) are the model's predictions for the drawn durations
            fp, fD = filed[key]
            assert np.allclose(fD, [x["outage_ms"] for x in per], rtol=0, atol=1e-9), key        # same interruptions as filed
            assert np.allclose(fp, [M.late_expect(d, H, rtt, owd)[0] for d in fD], rtol=0, atol=1e-4), key
            pre = np.asarray(fp, float)
        nf = np.array([x["failed_attempts"] for x in per], float); nfp = np.array([e[1] for e in ex])
        retry = nf > 0
        out[key] = {"H_ms": H, "n_valid": int(ok.sum()), "late_obs": float(obs[ok].mean()), "late_model": float(pre[ok].mean()),
                    "mae": float(np.abs(obs[ok] - pre[ok]).mean()), "failed_attempts_obs": float(nf[ok].mean()), "failed_attempts_model": float(nfp[ok].mean()),
                    "late_obs_no_retry": float(obs[ok & ~retry].mean()) if (ok & ~retry).any() else None, "late_model_no_retry": float(pre[ok & ~retry].mean()) if (ok & ~retry).any() else None,
                    "late_obs_retry": float(obs[ok & retry].mean()) if (ok & retry).any() else None, "late_model_retry": float(pre[ok & retry].mean()) if (ok & retry).any() else None,
                    "_obs": obs, "_pre": pre, "_ok": ok, "_nruns": len(c["runs"])}
        _o, _k, _p = obs.reshape(len(c["runs"]), -1), ok.reshape(len(c["runs"]), -1), pre.reshape(len(c["runs"]), -1)   # v1.9: run-level intervals
        _rm = np.array([_o[i][_k[i]].mean() for i in range(len(c["runs"])) if _k[i].any()]); _hw = T975[len(_rm) - 1] * _rm.std(ddof=1) / np.sqrt(len(_rm))
        out[key]["late_obs_run_t_ci95"] = [float(_rm.mean() - _hw), float(_rm.mean() + _hw)]
        _rr = np.array([(_o[i] - _p[i])[_k[i]].mean() for i in range(len(c["runs"])) if _k[i].any()]); _hr = T975[len(_rr) - 1] * _rr.std(ddof=1) / np.sqrt(len(_rr))
        out[key]["obs_minus_model_run_t_ci95"] = [float(_rr.mean() - _hr), float(_rr.mean() + _hr)]   # Fig. 1b bars: measured minus model, over the run means
        _ra = (_o - _p).mean(axis=1); _ha = T975[len(_ra) - 1] * _ra.std(ddof=1) / np.sqrt(len(_ra))     # v1.9c: the same over all intervals (the repeat's markers)
        out[key].update({"late_model_all_windows": float(pre.mean()), "late_obs_all_windows_cell": float(obs.mean()),
                         "obs_minus_model_run_t_ci95_all_windows": [float(_ra.mean() - _ha), float(_ra.mean() + _ha)]})
    allo = np.concatenate([v["_obs"][v["_ok"]] for v in out.values()]); allp = np.concatenate([v["_pre"][v["_ok"]] for v in out.values()])
    summ = {"n_intervals": int(len(allo)), "mae": float(np.abs(allo - allp).mean()), "bias_model_minus_obs": float((allp - allo).mean()),
            "corr": float(np.corrcoef(allo, allp)[0, 1]), "late_obs": float(allo.mean()), "late_model": float(allp.mean()),
            "failed_attempts_obs": float(np.mean([v["failed_attempts_obs"] for v in out.values()])), "failed_attempts_model": float(np.mean([v["failed_attempts_model"] for v in out.values()]))}
    return out, summ
dev_cells, dev_summ = model_cells(X3, QC, "development")
_dev_con = {}                                    # v1.9: the chain's penalty on the development runs, measured and modeled over the same matched intervals
for _p in ("5G-hosp", "5G-tele"):
    _a, _b = dev_cells[f"{_p}|detect|C2|ch3"], dev_cells[f"{_p}|detect|C0|ch2"]; _both = _a["_ok"] & _b["_ok"]
    _dd = float((_a["_obs"] - _b["_obs"])[_both].mean())
    assert abs(_dd - S["x3"]["cells"][f"{_p}|detect|C2|ch3"]["diff_from_lost_c0"]) < 1e-3                           # = Table IV
    _dev_con[f"{_p}|C2int_minus_C0"] = {"diff": _dd, "model_diff_common": float((_a["_pre"] - _b["_pre"])[_both].mean()), "n_common": int(_both.sum())}
S["x3_model"] = {"constants": {"pto_ms": "RTT + 25 + 1 + 0.5 (margin, variation floor, host turnaround per sample)", "period_ms": M.PERIOD_MS, "deadline_ms": M.DEADLINE_MS,
                               "phase": "g0 uniform on [-OWD, 16 - OWD); records generated before the onset were delivered, only their acknowledgments were lost"},
                 "development": {"summary": dev_summ, "cells": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in dev_cells.items()}, "contrasts": _dev_con},
                 "boundary": {}}
for prof, (rtt, owd) in PROF.items():
    S["x3_model"]["boundary"][prof] = {"pto_ms": M.pto_ms(rtt), "H_no_retry_limit_ms": M.DEADLINE_MS - M.pto_ms(rtt), "H_one_retry_limit_ms": M.DEADLINE_MS - 2 * M.pto_ms(rtt), "cells": {}}
    for cfg, ch in (("C0", 2), ("C1", 2), ("C2", 2), ("C2", 3), ("C2w", 3), ("C3m", 3)):
        H = S["rows"][f"{cfg}|ch{ch}"]["tcp_ms"][prof]
        S["x3_model"]["boundary"][prof]["cells"][f"{cfg}|ch{ch}"] = {"H_ms": H, "late_by_retries": [M.late_by_retries(H, rtt, owd, n) for n in (0, 1, 2)]}
# ---------------------------------------------------------------- held-out block (seeds 20261020..24; predictions filed before the runs)
HOF = os.path.join(RES, "testbed_x3_heldout.json"); HOQ = os.path.join(RES, "testbed_x3_heldout_qc.json"); PRE = os.path.join(RES, "testbed_x3_heldout_prereg.json")
HO = None
if os.path.exists(HOF) and os.path.exists(HOQ) and os.path.exists(PRE):
    import hashlib
    X3H = json.load(open(HOF)); QCH = json.load(open(HOQ)); PR = json.load(open(PRE))
    FILED = {k: (np.array([x["late_expected"] for r in v["runs"] for x in r["per_outage"]]), [x["outage_ms"] for r in v["runs"] for x in r["per_outage"]]) for k, v in PR["cells"].items()}
    ho_cells, ho_summ = model_cells(X3H, QCH, "held-out", filed=FILED)
    HO = {"prereg_sha256": hashlib.sha256(open(PRE, "rb").read()).hexdigest(), "prereg_written": PR["written"], "seeds": PR["seeds"], "summary": ho_summ, "cells": {}, "contrasts": {}}
    for key, v in ho_cells.items():
        pr = PR["cells"][key]
        c = X3H["cells"][key]; per = [x for r in c["runs"] for x in r["per_outage"]]
        HO["cells"][key] = {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
        _ok, _obs = v["_ok"], v["_obs"]; _nf = np.array([x["failed_attempts"] for x in per], float)
        HO["cells"][key].update({"late_total_valid": int(_obs[_ok].sum()), "late_in_failed_attempt_intervals_valid": int(_obs[_ok & (_nf > 0)].sum()),
                                 "intervals_with_failed_attempt_valid": int((_ok & (_nf > 0)).sum()),
                                 "late_model_minus_obs": float(v["late_model"] - v["late_obs"])})
        HO["cells"][key].update({"n_interruptions": len(per), "late_prereg": pr["late_per_interruption_expected"], "failed_attempts_prereg": pr["failed_attempts_expected"],
                                 "late_obs_all_windows": float(v["_obs"].mean()), "lost": c["lost"], "dup": c["dup"], "failed_runs": c["failed_runs"],
                                 "outage_ms_median": float(np.median([x["outage_ms"] for x in per])), "outage_ms_max": float(np.max([x["outage_ms"] for x in per])),
                                 "detect_ms_median": float(np.median([x["detect_ms"] for x in per if x["detect_ms"] is not None]))})
    for prof in PROF:
        k0 = f"{prof}|detect|C0|ch2"
        if k0 not in ho_cells: continue
        for ka, kb, name in ((f"{prof}|detect|C2|ch3", k0, "C2int_minus_C0"), (f"{prof}|detect|C2w|ch3", k0, "C2w_minus_C0"), (f"{prof}|detect|C2w|ch3", f"{prof}|detect|C2|ch3", "C2w_minus_C2int")):
            if ka not in ho_cells or kb not in ho_cells: continue
            a, b = ho_cells[ka], ho_cells[kb]; both = a["_ok"] & b["_ok"]; d = a["_obs"] - b["_obs"]; dm = a["_pre"] - b["_pre"]
            assert [r["seed"] for r in X3H["cells"][ka]["runs"]] == [r["seed"] for r in X3H["cells"][kb]["runs"]]
            bd = boot_means(d, both, a["_nruns"]); ba = boot_means(d, np.ones_like(both), a["_nruns"])
            HO["contrasts"][f"{prof}|{name}"] = {"diff": float(d[both].mean()), "ci95": [float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5))], "n_common": int(both.sum()),
                                                "diff_all_windows": float(d.mean()), "ci95_all_windows": [float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))],
                                                "model_diff_common": float(dm[both].mean()), "model_diff_prereg": float(np.mean(dm))}
            HO["contrasts"][f"{prof}|{name}"]["ci_contains_model"] = bool(HO["contrasts"][f"{prof}|{name}"]["ci95"][0] <= HO["contrasts"][f"{prof}|{name}"]["model_diff_common"] <= HO["contrasts"][f"{prof}|{name}"]["ci95"][1])
            _rm = np.array([dd[bb].mean() for dd, bb in zip(d.reshape(a["_nruns"], -1), both.reshape(a["_nruns"], -1)) if bb.any()])   # run means, t-interval (4 df)
            _hw = T975_DF4 * _rm.std(ddof=1) / np.sqrt(len(_rm))
            HO["contrasts"][f"{prof}|{name}"]["run_t_ci95"] = [float(_rm.mean() - _hw), float(_rm.mean() + _hw)]
            HO["contrasts"][f"{prof}|{name}"]["run_t_contains_model"] = bool(_rm.mean() - _hw <= HO["contrasts"][f"{prof}|{name}"]["model_diff_common"] <= _rm.mean() + _hw)
    _D = [x["outage_ms"] for r in X3H["cells"][next(iter(X3H["cells"]))]["runs"] for x in r["per_outage"]]
    HO["outage_ms_median"] = float(np.median(_D)); HO["outage_ms_max"] = float(np.max(_D)); HO["n_interruptions_per_cell"] = len(_D)
    HO["windows_total"] = sum(c["n_interruptions"] for c in HO["cells"].values()); HO["windows_invalid"] = sum(c["n_interruptions"] - c["n_valid"] for c in HO["cells"].values())
    HO["cell_mean_abs_dev_max"] = max(abs(c["late_obs"] - c["late_model"]) for c in HO["cells"].values())
    # where the excluded (host-stall) windows fell, and when their stalls came relative to the onset and the
    # reconnection (testbed/x3_qc.py records both); a stall that came after the reconnection cannot be the window's burst
    _ex, _sf, _ov = {}, [], []
    for key, c in X3H["cells"].items():
        for r in c["runs"]:
            q = QCH["cells"][key][str(r["seed"])]
            for i, bad in enumerate(q["invalid"]):
                if not bad: continue
                _ex[key] = _ex.get(key, 0) + 1; _sf.append(q["stall_first_ms_after_onset"][i])
                rc = q["reconnect_syn_ms_after_onset"][i]
                _ov.append(rc is not None and q["stall_first_ms_after_onset"][i] < rc + 300.0)     # within 300 ms of the reconnection request
    HO["exclusions_per_cell"] = _ex; HO["stall_first_ms_after_onset_range"] = [min(_sf), max(_sf)]; HO["stall_overlaps_reconnection"] = any(_ov)
    HO["late_in_excluded_windows"] = {key: [r["per_outage"][i]["late"] for r in c["runs"] for i, bad in enumerate(QCH["cells"][key][str(r["seed"])]["invalid"]) if bad] for key, c in X3H["cells"].items()}
    for prof in PROF:      # share of valid lost-C0 windows with a failed reconnection attempt
        c0 = HO["cells"].get(f"{prof}|detect|C0|ch2")
        if c0: HO.setdefault("failed_attempt_window_share_C0", {})[prof] = c0["intervals_with_failed_attempt_valid"] / c0["n_valid"]
    # sensitivity to the one assumed constant (host turnaround in the smoothed RTT): mean absolute error over the valid
    # intervals, development and held-out, with the constant at 0 to 2 ms (the model is otherwise unchanged)
    _keep = M.SRTT_EXTRA_MS; _sens = {}
    for _e in (0.0, 0.5, 1.0, 2.0):
        M.SRTT_EXTRA_MS = _e
        _sens[f"{_e:.1f}"] = {"development_mae": model_cells(X3, QC, "development")[1]["mae"], "heldout_mae": model_cells(X3H, QCH, "held-out")[1]["mae"]}
    M.SRTT_EXTRA_MS = _keep
    HO["sensitivity_host_turnaround_ms"] = _sens
    S["x3_model"]["heldout"] = HO
# ---------------------------------------------------------------- v1.9: controlled repeat of the 18 ms comparison (seeds 20261030..39,
# predictions, plan and run order filed before the runs in testbed_x3_repeat_prereg.json; emulator on its own CPU at real-time
# priority, conditions interleaved per seed in the filed random order; stalls attributed by testbed/x3_stallclass.py)
RPF, RPQ, RPP, RPO, RPC = (os.path.join(RES, f"testbed_x3_repeat{x}.json") for x in ("", "_qc", "_prereg", "_order", "_stallclass"))
if all(os.path.exists(f) for f in (RPF, RPQ, RPP, RPO)):
    import hashlib
    X3R = json.load(open(RPF)); QCR = json.load(open(RPQ)); PRR = json.load(open(RPP))
    assert X3R["setup"]["run_order"] == PRR["run_order"] == json.load(open(RPO))            # the runs followed the filed order
    FILR = {k: (np.array([x["late_expected"] for r in v["runs"] for x in r["per_outage"]]), [x["outage_ms"] for r in v["runs"] for x in r["per_outage"]]) for k, v in PRR["cells"].items()}
    rp_cells, rp_summ = model_cells(X3R, QCR, "repeat", filed=FILR)
    RP = {"prereg_sha256": hashlib.sha256(open(RPP, "rb").read()).hexdigest(), "order_sha256": hashlib.sha256(open(RPO, "rb").read()).hexdigest(),
          "prereg_written": PRR["written"], "seeds": PRR["seeds"], "host_control": X3R["setup"]["host_control"], "summary": rp_summ, "cells": {}, "contrasts": {}}
    for key, v in rp_cells.items():
        c = X3R["cells"][key]; per = [x for r in c["runs"] for x in r["per_outage"]]
        _ok, _obs = v["_ok"], v["_obs"]; _nf = np.array([x["failed_attempts"] for x in per], float)
        RP["cells"][key] = {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
        RP["cells"][key].update({"n_interruptions": len(per), "late_obs_all_windows": float(_obs.mean()), "late_prereg": PRR["cells"][key]["late_per_interruption_expected"],
                                 "late_total_valid": int(_obs[_ok].sum()), "late_in_failed_attempt_intervals_valid": int(_obs[_ok & (_nf > 0)].sum()),
                                 "intervals_with_failed_attempt_valid": int((_ok & (_nf > 0)).sum()), "lost": c["lost"], "dup": c["dup"], "failed_runs": c["failed_runs"]})
    prof = PRR["profile"]; k0, ki, kw = (f"{prof}|detect|C0|ch2", f"{prof}|detect|C2|ch3", f"{prof}|detect|C2w|ch3")
    for ka, kb, name in ((ki, k0, "C2int_minus_C0"), (kw, k0, "C2w_minus_C0"), (kw, ki, "C2w_minus_C2int")):
        a, b = rp_cells[ka], rp_cells[kb]; both = a["_ok"] & b["_ok"]; d = a["_obs"] - b["_obs"]; dm = a["_pre"] - b["_pre"]; nr = a["_nruns"]
        assert [r["seed"] for r in X3R["cells"][ka]["runs"]] == [r["seed"] for r in X3R["cells"][kb]["runs"]]
        bd = boot_means(d, both, nr); ba = boot_means(d, np.ones_like(both), nr)
        e = {"diff": float(d[both].mean()), "ci95": [float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5))], "n_common": int(both.sum()),
             "diff_all_windows": float(d.mean()), "ci95_all_windows": [float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))], "n_all": int(len(d)),
             "model_diff_common": float(dm[both].mean()), "model_diff_all": float(dm.mean())}
        for tag, m in (("", both), ("_all_windows", np.ones_like(both))):
            rm = np.array([dd[mm].mean() for dd, mm in zip(d.reshape(nr, -1), m.reshape(nr, -1)) if mm.any()])
            hw = T975[len(rm) - 1] * rm.std(ddof=1) / np.sqrt(len(rm))
            e["run_t_ci95" + tag] = [float(rm.mean() - hw), float(rm.mean() + hw)]
        e["ci_contains_model"] = bool(e["ci95"][0] <= e["model_diff_common"] <= e["ci95"][1])
        e["ci_all_windows_contains_model"] = bool(e["ci95_all_windows"][0] <= e["model_diff_all"] <= e["ci95_all_windows"][1])
        RP["contrasts"][f"{prof}|{name}"] = e
    _ex = {}
    for key, c in X3R["cells"].items():
        for r in c["runs"]:
            n_bad = sum(QCR["cells"][key][str(r["seed"])]["invalid"])
            if n_bad: _ex[key] = _ex.get(key, 0) + n_bad
    RP["exclusions_per_cell"] = _ex
    RP["windows_total"] = sum(c["n_interruptions"] for c in RP["cells"].values()); RP["windows_invalid"] = sum(c["n_interruptions"] - c["n_valid"] for c in RP["cells"].values())
    RP["late_in_excluded_windows"] = {key: [r["per_outage"][i]["late"] for r in c["runs"] for i, bad in enumerate(QCR["cells"][key][str(r["seed"])]["invalid"]) if bad] for key, c in X3R["cells"].items()}
    _D = [x["outage_ms"] for r in X3R["cells"][k0]["runs"] for x in r["per_outage"]]
    RP["outage_ms_median"] = float(np.median(_D)); RP["outage_ms_max"] = float(np.max(_D)); RP["n_interruptions_per_cell"] = len(_D)
    if os.path.exists(RPC):
        SC = json.load(open(RPC)); RP["invalid_by_class"] = SC["invalid_by_class"]
        RP["episodes_by_class"] = {}
        for key, v in SC["cells"].items():
            for q in v.values():
                for ep in q["episodes"]:
                    RP["episodes_by_class"].setdefault(key, {}).setdefault(ep["class"], 0); RP["episodes_by_class"][key][ep["class"]] += 1
    RPD = os.path.join(RES, "testbed_x3_repeat_stalldiag.json")          # post hoc diagnostic (testbed/x3_stalldiag.py), not the filed rule
    if os.path.exists(RPD):
        _sd = json.load(open(RPD)); RP["stalldiag_post_hoc"] = {k: v for k, v in _sd.items() if k not in ("rows", "note")}
    S["x3_model"]["repeat"] = RP
json.dump(S, open(os.path.join(RES, "testbed_summary.json"), "w"), indent=1)

def ms(x):
    return f"{x/1e3:.2f}\\,s" if x >= 1000 else f"{x:.0f}" if x >= 100 else f"{x:.1f}"
L = [r"\begin{tabular}{@{}lrrrrrr@{}}\toprule",
     r" & \multicolumn{2}{c}{Bytes} & \multicolumn{4}{c}{Time to first record (ms)} \\ \cmidrule(lr){2-3}\cmidrule(l){4-7}",
     r"Config. & server & total & 5G TCP & 5G QUIC & LTE-M & NB-IoT \\ \midrule"]
for cfg, ch, lab in ROWS:
    r = S["rows"][f"{cfg}|ch{ch}"]
    L.append(f"{lab} & {r['server_flight_B']:,} & {r['hs_bytes']:,} & {ms(r['tcp_ms']['5G-hosp'])} & {'--' if r['quic_ms']['5G-hosp'] is None else ms(r['quic_ms']['5G-hosp'])} & "
             f"{ms(r['tcp_ms']['LTE-M'])} & {ms(r['tcp_ms']['NB-IoT'])} \\\\")
L.append(r"\bottomrule\end{tabular}")
open(os.path.join(OUT, "tab4_testbed.tex"), "w").write("\n".join(L) + "\n")
print("\n".join(L))

# Table IV: the paired telemetry experiment
X5 = [("keep", "C2", 2, "Kept (no detector)"), ("detect", "C1", 2, "Lost, C1"), ("detect", "C2", 2, "Lost, C2"),
      ("detect", "C2", 3, "Lost, C2 + int."), ("detect", "C3m", 3, "Lost, C3m + int."), ("detect-resume", "C2", 3, "Resumed, C2 + int.")]
def f2(x): return "--" if x is None else (f"$-${-x:.2f}" if round(x, 2) < 0 else f"{abs(x) if round(x, 2) == 0 else x:.2f}")   # true minus sign; no "-0.00"
def f0(x): return "--" if x is None else f"{x:.0f}"
L = [r"\begin{tabular}{@{}lr@{\,}lrr@{\,}lr@{}}\toprule",
     r" & \multicolumn{3}{c}{10\,ms RTT} & \multicolumn{3}{c}{18\,ms RTT} \\ \cmidrule(lr){2-4}\cmidrule(l){5-7}",
     r"Session, config. & \multicolumn{2}{c}{Difference [95\,\% CI]} & $n$ & \multicolumn{2}{c}{Difference [95\,\% CI]} & $n$ \\ \midrule"]
def exc(e):
    if "diff_from_lost_c0" not in e: return r"\multicolumn{3}{c}{reference}"     # its own late level is not on the common intervals, so not printed
    return f"{f2(e['diff_from_lost_c0'])} & [{f2(e['diff_from_lost_c0_ci95'][0])}, {f2(e['diff_from_lost_c0_ci95'][1])}] & {e['n_common_with_lost_c0']}"
for pol, cfg, ch, lab in X5:
    a = S["x3"]["cells"].get(f"5G-hosp|{pol}|{cfg}|ch{ch}"); b = S["x3"]["cells"].get(f"5G-tele|{pol}|{cfg}|ch{ch}")
    if a is None or b is None: continue
    L.append(f"{lab} & {exc(a)} & {exc(b)} \\\\")
# v1.8: held-out block (new seeds; the model's per-interruption predictions were filed before the runs). Each measured
# row is followed by the model's difference on the same intervals.
if HO and all(f"{pr}|{nm}" in HO["contrasts"] for pr in PROF for nm in ("C2int_minus_C0", "C2w_minus_C0")):
    L.append(r"\midrule")
    def hoc(c): return f"{f2(c['diff'])} & [{f2(c['ci95'][0])}, {f2(c['ci95'][1])}] & {c['n_common']}"
    def hom(c): return f"{f2(c['model_diff_common'])} & & "
    for nm, lab in (("C2int_minus_C0", "Held-out, C2 + int."), ("C2w_minus_C0", "Held-out, C2 + int., IW\\,20")):
        a, b = HO["contrasts"][f"5G-hosp|{nm}"], HO["contrasts"][f"5G-tele|{nm}"]
        L.append(f"{lab} & {hoc(a)} & {hoc(b)} \\\\")
        L.append(f"\\quad model, filed & {hom(a)} & {hom(b)} \\\\")
L.append(r"\bottomrule\end{tabular}")
open(os.path.join(OUT, "tab5_session.tex"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
print(json.dumps(S["quic_C2_first_bursts"])); print(S["model_check_summary"], S["spread_5g_hosp_p10_p90_max_ms"])
for k, v in err.items(): print(k, round(v["meas_ms"], 1), round(v["model_ms"], 1), f"{100*v['rel']:+.1f}%", v["k_rtt"])
for k, v in S["x3"]["cells"].items(): print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()})
