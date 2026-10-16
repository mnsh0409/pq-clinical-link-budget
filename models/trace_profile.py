"""
trace_profile.py -- profile of the two measured-trace datasets fetched on 2026-09-28
(data/DATA-LEDGER.md: DATA-01 SIGCOMM'22 5G-mobility artifact, DATA-02 UCC Irish 5G traces)
against what Sections IV-V of the paper need.  Reads raw CSVs under ../data/, takes the
handshake sizes and latency budgets from the ledger through common.py, and writes
../results/trace_profile.json.  Nothing here is an input to the paper until it is quoted
into the ledger with its DATA id; this script exists so the numbers are reproducible.

What is computed (each block names the file it reads):
  A  handover duration, 43,856 measured events (T1 = MR->HO command, T2 = HO command->RACH)
  B  handover spacing in metres along freeway drives (fig. 11 files) -> HO/km, HO/h at speed
  C  handover rate re-derived from the 1-s GPS+PCI traces (fig. 10 file) as an independent check
  D  TCP RTT time series across NSA modes, with RTT after handover events (fig. 7 file)
  E  5G NSA PDSCH throughput along a driving loop (fig. 12 file) -> airtime of the three
     handshake sizes at measured throughput
  F  video-conferencing latency/loss while driving with handoff timestamps (fig. 4 files)
  G  UCC Irish 5G traces: per-second DL bitrate, RTT, cell changes per km, static vs driving
  H  paper-facing summary: airtime percentiles for C0/C1/C2 over measured throughput, and
     the share of measured handover interruptions that exceed each latency budget
"""
import os, glob, math, json
import numpy as np
import pandas as pd
from common import p, cid, derived, save

HERE = os.path.dirname(os.path.abspath(__file__))
D1 = os.path.join(HERE, "..", "data", "sigcomm22-5g-mobility", "data")
D2 = os.path.join(HERE, "..", "data", "ucc-5g-traces", "5G-production-dataset")

# ---------------------------------------------------------------- ledger inputs
C0 = p("tls_hs_bytes_ecdsa_ecdhe")
C1 = C0 - 2 * p("p256_uncompressed_point_B") + p("kex_x25519mlkem768_client_B") + p("kex_x25519mlkem768_server_B")
C2 = p("tls_hs_bytes_dil3_kyb3")
HS = {"C0_classical": C0, "C1_hybrid_kex": C1, "C2_full_pq": C2}
HS_IDS = ["tls_hs_bytes_ecdsa_ecdhe", "p256_uncompressed_point_B", "kex_x25519mlkem768_client_B",
          "kex_x25519mlkem768_server_B", "tls_hs_bytes_dil3_kyb3"]
BUDGETS_MS = {"ras_local": p("ras_local_latency_ms"), "ras_remote": p("ras_remote_latency_ms"),
              "rad": p("rad_latency_ms"), "telemetry": p("telemetry_latency_ms")}
BUDGET_IDS = ["ras_local_latency_ms", "ras_remote_latency_ms", "rad_latency_ms", "telemetry_latency_ms"]

PCT = [5, 10, 25, 50, 75, 90, 95, 99]

def pct(a, unit, n_note=None):
    a = np.asarray(a, dtype=float)
    a = a[np.isfinite(a)]
    if a.size == 0:
        return {"n": 0}
    d = {"n": int(a.size), "unit": unit, "mean": float(a.mean()), "min": float(a.min()), "max": float(a.max())}
    for q in PCT:
        d[f"p{q}"] = float(np.percentile(a, q))
    if n_note: d["note"] = n_note
    return d

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = p2 - p1
    dl = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))

out = {"meta": {
    "generated": "2026-09-28",
    "datasets": {
        "DATA-01": "SIGCOMM'22 'Vivisecting Mobility Management in 5G Cellular Networks' artifact, "
                   "github.com/SIGCOMM22-5GMobility/artifact @ c612c6fe (2022-06-26); U.S. commercial networks "
                   "(Verizon/T-Mobile/AT&T), Minneapolis-area drives; Git-LFS files D1/D2 not fetched",
        "DATA-02": "UCC MISL 'Beyond Throughput, the Next Generation: a 5G Dataset with Channel and Context Metrics' "
                   "(MMSys'20), github.com/uccmisl/5Gdataset @ 306d92eb (2020-06-19); one Irish operator, Cork, "
                   "static + car, 83 one-second traces",
    },
    "handshake_bytes": {k: derived(v, "byte", HS_IDS) for k, v in HS.items()},
    "latency_budgets_ms": {k: derived(v, "ms", [i]) for (k, v), i in zip(BUDGETS_MS.items(), BUDGET_IDS)},
}}

# ================================================================ A. handover duration
f = os.path.join(D1, "figure9-ho_exec_duration", "HO-Duration_Combined.csv")
ho = pd.read_csv(f)
ho["T1_ms"] = ho["MR"] * 1000.0                # preparation: measurement report -> HO command
ho["T2_ms"] = (ho["HO"] + ho["RCH"]) * 1000.0  # execution: HO command -> RACH complete (data plane halted)
ho["total_ms"] = ho["T1_ms"] + ho["T2_ms"]
full_check = float(np.nanmax(np.abs((ho["HO"] + ho["RCH"]) - ho["FULL"])))
A = {"file": os.path.relpath(f, HERE), "n_events": int(len(ho)),
     "definition": "T1 = 'MR' column (s); T2 = 'HO'+'RCH' columns (s), as in the artifact's figure-9 script; "
                   "'FULL' equals HO+RCH (max |diff| = %.3g s)" % full_check,
     "by_tech_all_types": {}, "by_tech_type": {}, "by_operator_tech_pcell": {},
     "share_of_T2_exceeding_budget": {}}
for tech, g in ho.groupby("Tech"):
    A["by_tech_all_types"][tech] = {"T1_ms": pct(g["T1_ms"], "ms"), "T2_ms": pct(g["T2_ms"], "ms"),
                                    "total_ms": pct(g["total_ms"], "ms")}
for (tech, typ), g in ho.groupby(["Tech", "Type"]):
    A["by_tech_type"][f"{tech}|{typ}"] = {"n": int(len(g)), "T1_mean_ms": float(g["T1_ms"].mean()),
                                          "T2_mean_ms": float(g["T2_ms"].mean()), "total_mean_ms": float(g["total_ms"].mean()),
                                          "T2_p50_ms": float(g["T2_ms"].median()), "T2_p90_ms": float(g["T2_ms"].quantile(.9)),
                                          "T2_p99_ms": float(g["T2_ms"].quantile(.99))}
pc = ho[ho["Type"].isin(["PCell", "MCG"])]
for (op, tech), g in pc.groupby(["Operator", "Tech"]):
    A["by_operator_tech_pcell"][f"{op}|{tech}"] = {"n": int(len(g)), "total_mean_ms": float(g["total_ms"].mean()),
                                                   "T2_mean_ms": float(g["T2_ms"].mean())}
for tech, g in ho.groupby("Tech"):
    A["share_of_T2_exceeding_budget"][tech] = {k: float((g["T2_ms"] > v).mean()) for k, v in BUDGETS_MS.items()}
A["nulls"] = {c: int(ho[c].isna().sum()) for c in ["HO", "MR", "RCH", "FULL"]}
A["cross_check_MOB-02e"] = {
    "paper_quote": "average HO duration NSA 167 ms, LTE 76 ms, SA 110 ms (Hassan et al. §5.2)",
    "reproduced_total_mean_ms_all_types": {t: float(g["total_ms"].mean()) for t, g in ho.groupby("Tech")},
    "reproduced_total_median_ms_all_types": {t: float(g["total_ms"].median()) for t, g in ho.groupby("Tech")},
    "reproduced_total_mean_ms_PCell_MCG_only": {t: float(g["total_ms"].mean()) for t, g in pc.groupby("Tech")},
    "reproduced_total_mean_ms_T1_le_1s": {t: float(g["total_ms"].mean()) for t, g in ho[ho["T1_ms"] <= 1000].groupby("Tech")},
    "verdict": "NOT REPRODUCED by simple statistics of the released file: the SA median (110 ms) matches the quoted "
               "SA figure, LTE/NSA do not under any of the subsets tried (all types, PCell/MCG only, T1 <= 1 s). "
               "The file has missing RCH in 11,101 rows and missing MR in 3,919, and T1 is heavy-tailed (NSA mean "
               "303 ms vs median 65 ms; 4.9 % of NSA events have T1 > 1 s). The authors' filtering is not in the "
               "artifact. Consequence for the paper: quote MOB-02e only as the authors' stated averages; for any "
               "figure or per-budget share, use the released per-event distribution and say so.",
}
out["A_handover_duration"] = A

# ================================================================ B. handover spacing (m) on freeway drives
B = {"files": {}, "note": "distance between consecutive handovers in metres as released for the paper's Fig. 11 "
                          "('distance_ho'); '_ideal_' files are distances between PCI changes ('distance_pci'). "
                          "HO/km = 1000/mean spacing; HO/h = HO/km x speed."}
for name in ["nsa_low", "nsa_mid", "sa_low"]:
    fpath = os.path.join(D1, "figure11-coverage_footprint", f"{name}_coverage.csv")
    s = pd.read_csv(fpath)["distance_ho"].astype(float)
    d = pct(s, "m")
    d["HO_per_km_from_mean"] = 1000.0 / d["mean"]
    d["HO_per_km_from_median"] = 1000.0 / d["p50"]
    d["HO_per_h_at_kmh"] = {str(v): v * 1000.0 / d["mean"] for v in (30, 60, 100, 130)}
    B["files"][name] = d
fpath = os.path.join(D1, "figure10-ho_energy_consumption", "distance.json")
B["authors_distance_json_m"] = json.load(open(fpath))
B["cross_check_MOB-02c"] = "paper: mmWave HO every 0.13 km, mid-band 0.35 km, low-band 0.4 km; distance.json: "
B["cross_check_MOB-02c"] += ", ".join(f"{k}={v} m" for k, v in B["authors_distance_json_m"].items())
out["B_handover_spacing"] = B

# ================================================================ C. HO rate from the 1-s GPS+PCI traces
f = os.path.join(D1, "figure10-ho_energy_consumption", "handoff-energy_combined.csv")
tr = pd.read_csv(f)
C = {"file": os.path.relpath(f, HERE), "n_rows_1s": int(len(tr)), "runs": {}}
for (loc, run), g in tr.groupby(["location", "run_number"]):
    g = g.sort_values("time_since_start").reset_index(drop=True)
    dist = haversine_m(g["latitude"].values[:-1], g["longitude"].values[:-1],
                       g["latitude"].values[1:], g["longitude"].values[1:])
    dt = np.diff(g["time_since_start"].values)
    ok = (dt > 0) & (dist / np.maximum(dt, 1e-9) < 60.0)   # drop GPS jumps > 60 m/s (216 km/h)
    dist_m = float(dist[ok].sum())
    dur_s = float(g["time_since_start"].iloc[-1] - g["time_since_start"].iloc[0])
    lte_ho = int((g["pci"].ne(g["pci"].shift(1)) & g["pci"].shift(1).notna()).sum())
    nr = g["nr_pci"]
    nr_ho = int((nr.ne(nr.shift(1)) & nr.notna() & nr.shift(1).notna()).sum())
    evt = int((g["handoffType"] != 0).sum())
    C["runs"][f"{loc}|run{run}"] = {
        "duration_s": dur_s, "distance_km": dist_m / 1000.0,
        "mean_speed_kmh": (dist_m / dur_s * 3.6) if dur_s > 0 else None,
        "lte_pci_changes": lte_ho, "nr_pci_changes": nr_ho, "handoffType_nonzero_rows": evt,
        "lte_pci_changes_per_km": (lte_ho / (dist_m / 1000.0)) if dist_m > 500 else None,
        "nr_pci_changes_per_km": (nr_ho / (dist_m / 1000.0)) if dist_m > 500 else None,
        "network_share": {k: float(v) for k, v in (g["network"].value_counts(normalize=True)).items()},
    }
C["note"] = ("PCI-change counts are an independent re-derivation from the released 1-s trace, not the authors' "
             "number; runs with < 0.5 km of GPS travel (HOME) get no per-km rate. handoffType is the 5G-Tracker "
             "app's own event code (0 = none).")
out["C_handover_rate_from_gps_trace"] = C

# ================================================================ D. TCP RTT across NSA modes, RTT after HO events
f = os.path.join(D1, "figure7-nsa_modes", "TCP-EXPERIMENTS.csv")
tcp = pd.read_csv(f, low_memory=False)
D = {"file": os.path.relpath(f, HERE), "n_rows": int(len(tcp)),
     "time_unit_note": "time_since_start advances in steps of 100 (ms assumed: 10 samples/s); SS_RTT_AVG is the "
                       "kernel's smoothed RTT (ms) as reported by `ss`", "by_mode": {}}
tcp["t"] = pd.to_numeric(tcp["time_since_start"], errors="coerce")
tcp["rtt"] = pd.to_numeric(tcp["SS_RTT_AVG"], errors="coerce")
for mode, g in tcp.groupby("mode"):
    g = g.sort_values("t")
    ev_t = g.loc[g["nr_ho_category"].notna(), "t"].values
    after = np.zeros(len(g), dtype=bool)
    tv = g["t"].values
    for et in ev_t:
        after |= (tv > et) & (tv <= et + 2000.0)
    D["by_mode"][mode] = {
        "rows": int(len(g)), "ho_events": int(len(ev_t)),
        "ho_event_categories": {k: int(v) for k, v in g["nr_ho_category"].value_counts().items()},
        "rtt_all_ms": pct(g["rtt"], "ms"),
        "rtt_within_2s_after_ho_ms": pct(g.loc[after, "rtt"], "ms"),
        "rtt_elsewhere_ms": pct(g.loc[~after, "rtt"], "ms"),
    }
out["D_tcp_rtt_nsa_modes"] = D

# ================================================================ E. 5G NSA PDSCH throughput along a driving loop
f = os.path.join(D1, "figure12-scg_mod_bwd_impact", "BNL-WLOOP-IPERF.csv")
bnl = pd.read_csv(f, low_memory=False)
tcol = "Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]"
bnl["tech"] = bnl["Event Technology"].ffill()
bnl["tput"] = pd.to_numeric(bnl[tcol], errors="coerce")
bnl["ts"] = pd.to_datetime(bnl["TIME_STAMP"], errors="coerce")
E = {"file": os.path.relpath(f, HERE), "n_rows": int(len(bnl)),
     "span_s": float((bnl["ts"].max() - bnl["ts"].min()).total_seconds()),
     "tput_samples_n": int(bnl["tput"].notna().sum()),
     "note": "PDSCH = NR-leg downlink PHY throughput under a saturating iperf download while driving (Verizon, "
             "mmWave/low-band NSA loop); this is the direction that carries the server's Certificate + signature "
             "flight, the largest flight of a PQ handshake",
     "pdsch_mbps_all": pct(bnl["tput"], "Mbps"),
     "pdsch_mbps_by_tech": {str(k): pct(g["tput"], "Mbps") for k, g in bnl.groupby("tech") if g["tput"].notna().sum() > 50},
     "nr_scg_mobility_events": {str(k): int(v) for k, v in bnl["5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type"].value_counts().items()},
     "lte_ho_events": {str(k): int(v) for k, v in bnl["HO Statistics Intra-LTE HO HO Type"].value_counts().items()},
}
tp = bnl["tput"].dropna()
tp = tp[tp > 0]
E["airtime_ms_at_measured_pdsch"] = {k: pct(v * 8.0 / (tp.values * 1e6) * 1e3, "ms",
                                            "bytes x 8 / measured PDSCH Mbps, per sample; lower bound (no scheduling delay, no "
                                            "retransmission). The p99/max tail comes from samples at a few kbit/s (outage or "
                                            "idle scheduler moments), i.e. a handshake started there stalls rather than 'takes 3 min'")
                                     for k, v in HS.items()}
E["share_of_samples_where_C2_airtime_exceeds_budget"] = {
    b: float(((C2 * 8.0 / (tp.values * 1e6) * 1e3) > ms).mean()) for b, ms in BUDGETS_MS.items()}
out["E_5g_nsa_pdsch_throughput_driving"] = E

# ================================================================ F. video conferencing while driving
f1 = os.path.join(D1, "figure4-video_conf", "laptop_driving_merged.csv")
f2 = os.path.join(D1, "figure4-video_conf", "driving_2_5g_tracker.csv")
vc = pd.read_csv(f1)
hoev = pd.read_csv(f2)
F = {"files": [os.path.relpath(f1, HERE), os.path.relpath(f2, HERE)], "n_rows": int(len(vc)),
     "span_s": float(vc["time_stamp(s)"].max() - vc["time_stamp(s)"].min()),
     "handoff_events": int(len(hoev)), "handoff_types": {str(k): int(v) for k, v in hoev["handoffType"].value_counts().items()},
     "latency_send_ms": pct(vc["latency_send(ms)"], "ms"), "latency_receive_ms": pct(vc["latency_receive(ms)"], "ms"),
     "packet_loss_avg_send_pct": pct(vc["packet_loss_avg_send(%)"], "%"),
     "packet_loss_avg_receive_pct": pct(vc["packet_loss_avg_receive(%)"], "%")}
t = vc["time_stamp(s)"].values
near = np.zeros(len(vc), dtype=bool)
for et in hoev["timestamp"].values:
    near |= (t >= et) & (t <= et + 5.0)
F["latency_send_within_5s_after_handoff_ms"] = pct(vc.loc[near, "latency_send(ms)"], "ms")
F["latency_send_elsewhere_ms"] = pct(vc.loc[~near, "latency_send(ms)"], "ms")
F["share_of_samples_over_budget_send"] = {b: float((vc["latency_send(ms)"] > ms).mean()) for b, ms in BUDGETS_MS.items()}
F["note"] = ("Application-reported one-way latency of a laptop video call tethered to a 5G phone while driving "
             "(artifact's Fig. 4); the relevant clinical analogue is the ambulance video/telemetry stream, not surgery")
out["F_video_conf_driving"] = F

# ================================================================ G. UCC Irish 5G traces
files = sorted(glob.glob(os.path.join(D2, "**", "*.csv"), recursive=True))
rows = []
per_trace = []
for fp in files:
    df = pd.read_csv(fp, low_memory=False)
    rel = os.path.relpath(fp, D2).replace(os.sep, "/")
    app = rel.split("/")[0]; mob = rel.split("/")[1]
    df["app"] = app; df["mobility"] = mob; df["trace"] = rel
    for c in ["DL_bitrate", "UL_bitrate", "Speed", "RSRP", "SNR", "CQI", "PINGAVG", "PINGLOSS", "Longitude", "Latitude"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # distance: GPS fixes update only every ~10-15 rows, so integrate the per-row Speed (km/h) over the
    # row-to-row time step (capped at 5 s) and keep the GPS path length over distinct fixes as a cross-check
    ts = pd.to_datetime(df["Timestamp"], format="%Y.%m.%d_%H.%M.%S", errors="coerce")
    dt = ts.diff().dt.total_seconds().fillna(1.0).clip(lower=0.0, upper=5.0).values
    dist_speed_m = float(np.nansum(df["Speed"].fillna(0).values / 3.6 * dt))
    fix = df.loc[(df["Latitude"].ne(df["Latitude"].shift(1))) | (df["Longitude"].ne(df["Longitude"].shift(1))), ["Latitude", "Longitude"]].copy()
    fix["t"] = ts[fix.index]
    dist_gps_m = 0.0
    if len(fix) > 1:
        seg = haversine_m(fix["Latitude"].values[:-1], fix["Longitude"].values[:-1], fix["Latitude"].values[1:], fix["Longitude"].values[1:])
        segdt = np.diff(fix["t"].values).astype("timedelta64[s]").astype(float)
        okk = np.isfinite(seg) & (segdt > 0) & (seg / np.maximum(segdt, 1e-9) <= 60.0)
        dist_gps_m = float(seg[okk].sum())
    d_m = dist_speed_m
    cell_changes = int((df["RAWCELLID"].ne(df["RAWCELLID"].shift(1)) & df["RAWCELLID"].shift(1).notna()).sum())
    per_trace.append({"trace": rel, "app": app, "mobility": mob, "seconds": int(len(df)),
                      "distance_km": float(d_m / 1000.0), "distance_km_gps_crosscheck": float(dist_gps_m / 1000.0),
                      "cell_changes": cell_changes,
                      "cell_changes_per_km": (cell_changes / (d_m / 1000.0)) if d_m > 500 else None,
                      "mean_speed_kmh": float(df["Speed"].mean()) if df["Speed"].notna().any() else None,
                      "network_modes": {str(k): int(v) for k, v in df["NetworkMode"].value_counts().items()},
                      "dl_kbps_active_p50": float(df.loc[df["DL_bitrate"] > 0, "DL_bitrate"].median()) if (df["DL_bitrate"] > 0).any() else None,
                      "ping_avg_ms_median": float(df["PINGAVG"].median()) if df["PINGAVG"].notna().any() else None})
    rows.append(df)
allrows = pd.concat(rows, ignore_index=True)
G = {"root": os.path.relpath(D2, HERE), "n_traces": len(files), "n_rows_1s": int(len(allrows)),
     "columns": list(pd.read_csv(files[0], nrows=1).columns),
     "traces_by_app_mobility": {f"{a}|{m}": int(n) for (a, m), n in allrows.groupby(["app", "mobility"])["trace"].nunique().items()},
     "network_mode_rows": {str(k): int(v) for k, v in allrows["NetworkMode"].value_counts().items()},
     "per_trace": per_trace}
dl = allrows[(allrows["app"] == "Download")]
for mob, g in dl.groupby("mobility"):
    act = g.loc[g["DL_bitrate"] > 0, "DL_bitrate"]
    G[f"download_{mob}_dl_kbps_active_seconds"] = pct(act, "kbit/s", "file-download traces, seconds with DL_bitrate > 0 (application-layer rate; the only traffic class here that is not rate-limited by a player)")
    G[f"download_{mob}_dl_kbps_by_network_mode"] = {str(k): pct(gg.loc[gg["DL_bitrate"] > 0, "DL_bitrate"], "kbit/s")
                                                    for k, gg in g.groupby("NetworkMode") if (gg["DL_bitrate"] > 0).sum() > 30}
for mob, g in allrows.groupby("mobility"):
    G[f"{mob}_ping_avg_ms"] = pct(g["PINGAVG"], "ms", "PINGAVG column where numeric (ICMP to a fixed host, per the dataset README)")
    G[f"{mob}_speed_kmh"] = pct(g["Speed"], "km/h")
    if mob == "Driving":
        cc = [x["cell_changes_per_km"] for x in per_trace if x["mobility"] == mob and x["cell_changes_per_km"] is not None]
        G["Driving_cell_changes_per_km_over_traces"] = pct(cc, "changes/km", "RAWCELLID changes per speed-integrated km, one value per driving trace") if cc else {"n": 0}
        G["Driving_totals"] = {"traces": len(cc), "km_speed_integrated": float(sum(x["distance_km"] for x in per_trace if x["mobility"] == mob)),
                               "km_gps_crosscheck": float(sum(x["distance_km_gps_crosscheck"] for x in per_trace if x["mobility"] == mob)),
                               "hours": float(sum(x["seconds"] for x in per_trace if x["mobility"] == mob) / 3600.0),
                               "cell_changes": int(sum(x["cell_changes"] for x in per_trace if x["mobility"] == mob)),
                               "note": "GPS fixes repeat for 10-15 rows and several fixes share a 1-s timestamp, so the GPS path "
                                       "length under-counts; the speed-integrated figure is used for per-km rates"}
    else:
        hrs = sum(x["seconds"] for x in per_trace if x["mobility"] == mob) / 3600.0
        G["Static_cell_changes_per_hour"] = float(sum(x["cell_changes"] for x in per_trace if x["mobility"] == mob) / hrs)
        G["Static_totals"] = {"traces": sum(1 for x in per_trace if x["mobility"] == mob), "hours": float(hrs)}
act = dl.loc[(dl["mobility"] == "Driving") & (dl["DL_bitrate"] > 0), "DL_bitrate"].values  # kbit/s
G["airtime_ms_at_measured_dl_driving_download"] = {
    k: pct(v * 8.0 / (act * 1e3) * 1e3, "ms", "bytes x 8 / per-second application DL rate, driving file-download seconds; lower bound")
    for k, v in HS.items()}
G["share_of_driving_download_seconds_where_C2_airtime_exceeds_budget"] = {
    b: float(((C2 * 8.0 / (act * 1e3) * 1e3) > ms).mean()) for b, ms in BUDGETS_MS.items()}
out["G_ucc_irish_5g_traces"] = G

# ================================================================ H. paper-facing summary
H = {
 "what_each_dataset_gives": {
   "DATA-01 (SIGCOMM'22)": [
     "Section IV: distribution (not just the mean) of handover interruption T2 for LTE/NSA/SA, 43,856 events -> the "
     "user-plane outage a clinical stream sees per handover, and the share exceeding the 2/20/100 ms budgets",
     "Section IV: HO spacing distributions on freeway drives (Fig. 11 files) -> HO/km and HO/h at speed as a "
     "distribution; distance.json reproduces MOB-02c (0.13/0.35/0.4 km)",
     "Section IV/V: RTT time series around handover events (Fig. 7 file) -> RTT anchor measured, not assumed",
     "Section V: measured NSA downlink PHY throughput while driving (Fig. 12 file) -> airtime of C0/C1/C2 as a "
     "distribution; Section VII: a video call under mobility with handoff timestamps (Fig. 4 files) as the "
     "ambulance-stream analogue",
   ],
   "DATA-02 (UCC Irish 5G)": [
     "Section V: per-second application DL rate under driving with cell id, RSRP/SNR/CQI and ICMP RTT -> a second "
     "operator/country for the airtime distribution and a cell-change rate per km in a city (Cork) rather than a freeway",
   ],
 },
 "caveats_to_state": [
   "Both are downlink-centric consumer measurements (phones/laptops), U.S. and Irish networks, 2019-2022; no NB-IoT, "
   "LTE-M, BLE or 802.15.6 traces -> the constrained-link rows of Table II stay nominal unless a third dataset is added",
   "Application-layer DL rates (DATA-02) and PHY PDSCH (DATA-01) are not the same quantity; airtime from either is a lower bound",
   "DATA-01 has no stated license in the repository; DATA-02 is GPL-3.0 (fine to analyse and cite; ask before bundling as SM)",
 ],
}
out["H_summary"] = H
save("trace_profile.json", out)
print("A: events", A["n_events"], "| total mean ms by tech:", {k: round(v, 1) for k, v in A["cross_check_MOB-02e"]["reproduced_total_mean_ms_all_types"].items()})
print("B: HO/km from mean spacing:", {k: round(v["HO_per_km_from_mean"], 2) for k, v in B["files"].items()})
print("E: PDSCH p10/p50/p90 Mbps:", [round(E["pdsch_mbps_all"][q], 1) for q in ("p10", "p50", "p90")])
print("G: traces", G["n_traces"], "rows", G["n_rows_1s"])
