"""
figures.py -- Figures 1-2 of the paper, regenerated from results JSON and the raw traces.
Outputs vector PDFs into ../paper/figs/.  Every plotted number comes from
results/urllc_transmission.json, sources/ledger.json (via common.py) or the DATA-01/DATA-02
files with the same filters as trace_profile.py.
"""
import os, glob, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import p

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "paper", "figs"); os.makedirs(OUT, exist_ok=True)
D1 = os.path.join(ROOT, "data", "sigcomm22-5g-mobility", "data")
D2 = os.path.join(ROOT, "data", "ucc-5g-traces", "5G-production-dataset")

# validated categorical slots 1-3 (dataviz reference palette, light mode, all-pairs PASS)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d3"
plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7,
                     "ytick.labelsize": 7, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.labelcolor": INK, "text.color": INK, "pdf.fonttype": 42,
                     "font.family": "DejaVu Sans"})

C0 = p("tls_hs_bytes_ecdsa_ecdhe")
C1 = C0 - 2 * p("p256_uncompressed_point_B") + p("kex_x25519mlkem768_client_B") + p("kex_x25519mlkem768_server_B")
C2 = p("tls_hs_bytes_dil3_kyb3")
BUDGETS = [(p("ras_local_latency_ms"), "2 ms  RAS, local link (in-room)"), (p("rad_latency_ms"), "20 ms  RAS remote / RAD"),
           (p("telemetry_latency_ms"), "100 ms  telemetry")]

def style_axes(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(True, which="major", color=GRID, lw=0.5)
    ax.grid(True, which="minor", color=GRID, lw=0.3, alpha=0.6)
    ax.set_axisbelow(True)

# ================================================================ Fig. 1 airtime vs link rate
ut = json.load(open(os.path.join(ROOT, "results", "urllc_transmission.json")))
rates = np.logspace(np.log10(2e4), np.log10(2e8), 200)
fig, ax = plt.subplots(figsize=(3.45, 2.0))
for B, col, ls, lab in [(C0, BLUE, "-", f"C0 classical, {C0:,} B"),
                        (C1, ORANGE, "--", f"C1 hybrid KEM, {C1:,} B"),
                        (C2, AQUA, ":", f"C2 post-quantum, {C2:,} B")]:
    ax.plot(rates, B * 8 / rates * 1e3, color=col, ls=ls, lw=1.4, label=lab)
short = {"IEEE 802.15.4 / 6LoWPAN, 2.4 GHz (AES-CCM-128 link security)": "802.15.4",
         "IEEE 802.15.6 WBAN narrowband, lowest PHY rate": "NB-IoT UL, WBAN lo",
         "IEEE 802.15.6 WBAN narrowband, highest PHY rate": None,
         "Bluetooth LE 1M (application-rate approximation)": "BLE 1M, WBAN hi",
         "Bluetooth LE 2M (application-rate approximation)": "BLE 2M",
         "NB-IoT uplink (peak, multi-tone)": None, "NB-IoT downlink (peak)": "NB-IoT DL",
         "LTE-M half-duplex uplink": "LTE-M UL",
         "5G NR uplink, measured in a clinical deployment (Chen 2024 avg)": "5G UL",
         "5G NR uplink, measured during telesurgery (Ye 2026)": None}
offs = {"NB-IoT DL": (6, 4, "left"), "NB-IoT UL, WBAN lo": (6, 4, "left"), "802.15.4": (6, 3, "left"),
        "LTE-M UL": (6, 4, "left"), "BLE 1M, WBAN hi": (6, 4, "left"), "BLE 2M": (6, 3, "left"),
        "5G UL": (-4, 8, "right")}   # every label above and right of its marker, clear of the lines below; near-coincident markers share one label
xs, ys = [], []
for row in ut["airtime_table"]:
    lab = short.get(row["link"], "")
    x, y = row["rate_bps"], row["C2_full_pq"]["airtime_s"] * 1e3
    xs.append(x); ys.append(y)
    if lab is None: continue          # marker only: it shares the label of its near-coincident neighbor
    dx, dy, ha = offs.get(lab, (4, 4, "left"))
    ax.annotate(lab, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=6.5, color=INK, ha=ha)
ax.scatter(xs, ys, s=16, facecolor="white", edgecolor=AQUA, lw=1.1, zorder=5, label="C2 per link (Table II)")
for ms, lab in BUDGETS:
    ax.axhline(ms, color=MUTED, ls=(0, (3, 2)), lw=0.7)
    above = ms < 10        # the 2 ms label sits above its line (clear of the legend); 20 and 100 ms below (clear of the point labels)
    ax.text(8e3, ms * 1.18 if above else ms / 1.18, lab, ha="left", va="bottom" if above else "top", fontsize=6.5, color=MUTED)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(7e3, 2e8); ax.set_ylim(0.03, 3e4)
ax.set_xlabel("Link rate (b/s)"); ax.set_ylabel("Handshake airtime (ms)")
ax.set_xticks([1e5, 1e6, 1e7, 1e8]); ax.set_xticklabels(["100 k", "1 M", "10 M", "100 M"])
ax.set_yticks([0.1, 1, 10, 100, 1000, 1e4]); ax.set_yticklabels(["0.1", "1", "10", "100", "1 000", "10 000"])
style_axes(ax)
ax.legend(loc="lower left", frameon=False, handlelength=1.4, handletextpad=0.4, fontsize=6.0, labelspacing=0.2, borderaxespad=0.15, ncol=2, columnspacing=0.6)
fig.tight_layout(pad=0.3)
fig.savefig(os.path.join(OUT, "fig1_airtime.pdf")); plt.close(fig)
print("fig1 points:", list(zip([short.get(r["link"]) for r in ut["airtime_table"]], [round(r["C2_full_pq"]["airtime_s"]*1e3, 2) for r in ut["airtime_table"]])))

# ================================================================ Fig. 2 trace-driven CDFs
ho = pd.read_csv(os.path.join(D1, "figure9-ho_exec_duration", "HO-Duration_Combined.csv"))
ho["T2_ms"] = (ho["HO"] + ho["RCH"]) * 1000.0
# primary-cell handovers only: the user plane of the stream is halted; secondary-cell-group (SCG) events of NSA are
# excluded because a dual-connectivity UE can keep the stream on the LTE leg during them (Hassan et al. 2022)
PRIMARY = {"LTE": ["PCell"], "NSA": ["PCell", "MCG"], "SA": ["MCG"]}
def prim(t): return ho[(ho["Tech"] == t) & (ho["Type"].isin(PRIMARY[t]))]
def pos(t):
    g = prim(t)["T2_ms"]; return g[g > 0]      # events with both timestamps; non-positive artifacts dropped
bnl = pd.read_csv(os.path.join(D1, "figure12-scg_mod_bwd_impact", "BNL-WLOOP-IPERF.csv"), low_memory=False)
tp_all = pd.to_numeric(bnl["Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]"], errors="coerce").dropna().values
us_air = np.where(tp_all > 0, C2 * 8.0 / np.maximum(tp_all, 1e-12) / 1e6 * 1e3, np.inf)   # zero-throughput samples = outage (counted as exceeding every budget)
# Irish traces: seconds in the downloading state only (State "D"; the paper defines I = idle, D = downloading; a few
# rows carry undocumented "V"/"VD" states and are left out). The measurement app pings every ~13 s, and almost every
# second below 10 kb/s sits within 1 s of a ping whose round trip is normal: the transfer paused, not the link. Those
# ping windows are excluded whatever their rate (an outcome-independent filter); the zero-rate seconds that remain
# are counted as outages, exactly as the zero-throughput U.S. samples are.
PING_WIN_S = 1
def near(mask, w):
    out = mask.copy()
    for k in range(1, w + 1):
        out[:-k] |= mask[k:]; out[k:] |= mask[:-k]
    return out
irish_d, ping_diag = [], []
for fp in sorted(glob.glob(os.path.join(D2, "Download", "Driving", "*.csv"))):
    df = pd.read_csv(fp, low_memory=False)
    dl = pd.to_numeric(df["DL_bitrate"], errors="coerce")
    rtt = pd.to_numeric(df["PINGAVG"], errors="coerce"); loss = pd.to_numeric(df["PINGLOSS"], errors="coerce")
    ping = rtt.notna().values
    down = ((df["State"] == "D") & dl.notna()).values
    low5 = down & (dl.fillna(0).values < 10) & (df["NetworkMode"] == "5G").values
    f = pd.DataFrame({"dl": dl.values, "mode": df["NetworkMode"].values, "file": os.path.basename(fp),
                      "near_ping": near(ping, PING_WIN_S), "near_ping2": near(ping, 2)})
    irish_d.append(f[down])
    i = np.where(ping)[0]
    ts = pd.to_datetime(df["Timestamp"], format="%Y.%m.%d_%H.%M.%S", errors="coerce").values[i]
    ping_diag.append(pd.DataFrame({"gap": np.r_[np.nan, np.diff(i)], "gap_s": np.r_[np.nan, np.diff(ts) / np.timedelta64(1, "s")],
                                   "rtt": rtt.values[i], "loss": loss.values[i],
                                   "is5g": df["NetworkMode"].values[i] == "5G", "next_to_low": near(low5, PING_WIN_S)[i]}))
irish_d = pd.concat(irish_d, ignore_index=True); ping_diag = pd.concat(ping_diag, ignore_index=True)
irish = irish_d[~irish_d["near_ping"]].reset_index(drop=True)
def airtime(dl_kbps): dl_kbps = np.asarray(dl_kbps, float); return np.where(dl_kbps > 0, C2 * 8.0 / np.maximum(dl_kbps, 1e-12) / 1e3 * 1e3, np.inf)
ie5 = irish.loc[irish["mode"] == "5G", "dl"].values
ie_all = irish["dl"].values
ie5_air = airtime(ie5)
ie_all_air = airtime(ie_all)

def cdf(ax, a, color, ls, label, show_n=True, lw=1.3):
    a = np.sort(np.asarray(a, float)); n = len(a); a = a[np.isfinite(a) & (a > 0)]
    y = np.arange(1, len(a) + 1) / n                      # infinite (outage) samples never reach 1.0: the CDF stops short of 1
    ax.plot(a, y, color=color, ls=ls, lw=lw, label=(f"{label} (n={n:,})" if show_n else label))
    return a

# v1.6: one panel (handover interruption); the airtime-under-mobility proxy is reported in the text only
fig, a1 = plt.subplots(1, 1, figsize=(3.45, 1.4))
for tech, col, ls, lab in [("LTE", BLUE, "-", "LTE"), ("NSA", ORANGE, "--", "NSA"), ("SA", AQUA, ":", "SA")]:
    cdf(a1, pos(tech), col, ls, lab)
for ms, lab in BUDGETS:
    a1.axvline(ms, color=MUTED, ls=(0, (3, 2)), lw=0.7)
a1.text(20 * 1.08, 0.97, "20 ms", fontsize=6.5, color=MUTED, va="top"); a1.text(100 * 1.08, 0.97, "100 ms", fontsize=6.5, color=MUTED, va="top")
a1.set_xscale("log"); a1.set_xlim(10, 2000); a1.set_ylim(0, 1)
a1.set_xticks([10, 20, 50, 100, 200, 500, 1000, 2000]); a1.set_xticklabels(["10", "20", "50", "100", "200", "500", "1 000", "2 000"])
a1.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
a1.set_xlabel("Handover execution interruption $T_2$ (ms)"); a1.set_ylabel("CDF"); a1.set_yticks([0, 0.5, 1])
a1.legend(loc="center right", frameon=False)
style_axes(a1)
fig.tight_layout(pad=0.4)
fig.savefig(os.path.join(OUT, "fig2_traces.pdf")); plt.close(fig)

# numbers the text quotes from these exact arrays
def share(a, ms): a = np.asarray(a, float); return float((a > ms).mean())        # inf counts as exceeding
def pct(a, q): a = np.asarray(a, float); return float(np.percentile(a, q))      # inf propagates only above the outage share
techs = ("LTE", "NSA", "SA")
stats = {"T2_share_over": {t: {ms: share(pos(t), ms) for ms, _ in BUDGETS} for t in techs},
         "T2_share_over_conservative_missing_as_not_exceeding": {t: {ms: float((pos(t) > ms).sum() / len(prim(t))) for ms, _ in BUDGETS} for t in techs},
         "T2_median": {t: float(pos(t).median()) for t in techs},
         "T2_p90": {t: float(pos(t).quantile(.9)) for t in techs},
         "T2_rows_primary": {t: int(len(prim(t))) for t in techs},
         "T2_missing_rach": {t: int(prim(t)["RCH"].isna().sum()) for t in techs},
         "T2_dropped_nonpositive": {t: int((prim(t)["T2_ms"].dropna() <= 0).sum()) for t in techs},
         "file_rows": int(len(ho)), "scg_rows_excluded": int((ho["Type"].isin(["SCG Add.", "SCG Mod.", "SCG Rel."])).sum()),
         "us_air_pct": {q: pct(us_air, q) for q in (50, 90, 95)},
         "us_air_share_over": {ms: share(us_air, ms) for ms, _ in BUDGETS},
         "us_zero_throughput_samples": int(np.isinf(us_air).sum()),
         "ie5_air_pct": {q: pct(ie5_air, q) for q in (50, 90, 95)},
         "ie5_air_share_over": {ms: share(ie5_air, ms) for ms, _ in BUDGETS},
         "ie5_zero_rate_seconds": int(np.isinf(ie5_air).sum()), "ie_all_zero_rate_seconds": int(np.isinf(ie_all_air).sum()),
         "ie_all_air_pct": {q: pct(ie_all_air, q) for q in (50, 90, 95)},
         "ie_all_air_share_over": {ms: share(ie_all_air, ms) for ms, _ in BUDGETS},
         "ie_non5g_share": float((irish["mode"] != "5G").mean()),
         "n": {"T2_LTE": int(len(pos("LTE"))), "T2_NSA": int(len(pos("NSA"))), "T2_SA": int(len(pos("SA"))),
               "us": int(len(us_air)), "ie5": int(len(ie5_air)), "ie_all": int(len(ie_all_air))}}
# why the ping windows go: the app's ping cadence, where the low-rate seconds sit, and the round trip of those pings
d5 = irish_d[irish_d["mode"] == "5G"]; low = d5["dl"] < 10; high = d5["dl"] >= 100
p5 = ping_diag[ping_diag["is5g"]]
stats["ie_ping_check"] = {
    "window_rows": PING_WIN_S, "ping_gap_median_rows": float(ping_diag["gap"].median()),
    "ping_gap_median_s": float(ping_diag["gap_s"].median()), "ping_gap_share_12_15_s": float(ping_diag["gap_s"].between(12, 15).mean()),
    "ie5_downloading_seconds_before_exclusion": int(len(d5)),
    "ie5_low_rate_seconds": int(low.sum()), "ie5_zero_rate_seconds_before_exclusion": int((d5["dl"] == 0).sum()),
    "ie5_low_rate_share_near_ping": float(d5.loc[low, "near_ping"].mean()),
    "ie5_high_rate_share_near_ping": float(d5.loc[high, "near_ping"].mean()),
    "ie5_excluded_seconds": int(d5["near_ping"].sum()),
    "pings_5g": int(len(p5)), "pings_5g_next_to_low_rate": int(p5["next_to_low"].sum()),
    "rtt_p50_next_to_low_rate_ms": float(p5.loc[p5["next_to_low"], "rtt"].median()),
    "loss_p50_next_to_low_rate_pct": float(p5.loc[p5["next_to_low"], "loss"].median()),
    "rtt_p50_other_ms": float(p5.loc[~p5["next_to_low"], "rtt"].median()),
    # sensitivity of the quoted shares to the rule (not in the paper; CHANGES-review-1.md)
    "ie5_share_over_win2": {ms: share(airtime(d5.loc[~d5["near_ping2"], "dl"]), ms) for ms, _ in BUDGETS},
    "ie5_share_over_no_window_zero_as_outage": {ms: share(airtime(d5["dl"]), ms) for ms, _ in BUDGETS},
    "ie5_share_over_no_window_zero_dropped": {ms: share(airtime(d5.loc[d5["dl"] > 0, "dl"]), ms) for ms, _ in BUDGETS},
    "ie5_p50_win2": pct(airtime(d5.loc[~d5["near_ping2"], "dl"]), 50)}
# T2 lower bound over ALL primary-cell events: on primary-cell rows RCH > 0 always, so T2 > HO; an event without the
# completion stamp whose HO stage alone exceeds 20 ms certainly has T2 > 20 ms
stats["T2_primary_min_RCH_s"] = float(min(prim(t)["RCH"].min() for t in techs if prim(t)["RCH"].notna().any()))
stats["T2_unmeasured_HO_over_20_share"] = {t: float((prim(t).loc[prim(t)["RCH"].isna(), "HO"] * 1e3 > 20).mean()) for t in ("LTE", "NSA")}
stats["T2_share_over_20_lower_bound_all_events"] = {t: float((((prim(t)["T2_ms"] > 20) & prim(t)["RCH"].notna()) |
                                                              ((prim(t)["HO"] * 1e3 > 20) & prim(t)["RCH"].isna())).sum() / len(prim(t))) for t in techs}
stats["T2_SA_operators"] = sorted(prim("SA")["Operator"].unique().tolist())
# the U.S. samples: a third on LTE alone (authors' rule: forward-filled "Event Technology")
et = bnl["Event Technology"].ffill()[pd.to_numeric(bnl["Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]"], errors="coerce").notna()]
lte_alone = (et.str.contains("LTE", na=False) & ~et.str.contains("NSA", na=False)).values
stats["us_lte_alone_share"] = float(lte_alone.mean())
stats["us_share_over_2_lte_alone"] = share(us_air[lte_alone], 2); stats["us_share_over_2_with_nr"] = share(us_air[~lte_alone], 2)
# the U.S. column is the EN-DC total: Total PDU = NR PDU + LTE PDU on every sample that logs all three
nr = pd.to_numeric(bnl["Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(5G-NR PDU) [Mbps]"], errors="coerce")
lte = pd.to_numeric(bnl["Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(LTE PDU) [Mbps]"], errors="coerce")
tot = pd.to_numeric(bnl["Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]"], errors="coerce")
allthree = tot.notna() & nr.notna() & lte.notna()
stats["us_total_is_nr_plus_lte"] = {"rows_with_all_three": int(allthree.sum()),
                                    "max_abs_diff_mbps": float((tot - nr - lte)[allthree].abs().max())}
# the same replay for the other three handshakes (airtime scales with bytes; the outage samples stay inf)
C2u = C2 - p("mldsa65_pk_B") - 2 * p("mldsa65_sig_B")
stats["air_share_over_by_handshake"] = {}
for name, B in (("C0_classical", C0), ("C1_hybrid_kex", C1), ("C2_full_pq", C2), ("C2_server_only_derived", C2u)):
    u = np.where(tp_all > 0, B * 8.0 / np.maximum(tp_all, 1e-12) / 1e6 * 1e3, np.inf)
    i = np.where(ie5 > 0, B * 8.0 / np.maximum(ie5, 1e-12) / 1e3 * 1e3, np.inf)
    stats["air_share_over_by_handshake"][name] = {"bytes": int(B), "us": {ms: share(u, ms) for ms, _ in BUDGETS}, "ie5": {ms: share(i, ms) for ms, _ in BUDGETS}}
json.dump(stats, open(os.path.join(ROOT, "results", "fig2_stats.json"), "w"), indent=1)

# --- robustness statistics quoted in the text: per-operator shares (the Verizon log is nearly complete) and a
#     trace-level (cluster) bootstrap for the Irish 5G seconds, which come from only 15 drives
rng = np.random.default_rng(20261012)
byop = {}
for (op, t), d in ho[ho.apply(lambda r: r["Type"] in PRIMARY[r["Tech"]], axis=1)].groupby(["Operator", "Tech"]):
    m = d["T2_ms"]; m = m[m > 0]
    byop[f"{op}|{t}"] = {"n": int(len(m)), "missing_stamp_share": float(d["RCH"].isna().mean()),
                         "share_over_20": float((m > 20).mean()), "median": float(m.median())}
vzw = {k: v for k, v in byop.items() if k.startswith("VZW")}
stats["T2_by_operator"] = byop
stats["T2_vzw_total_n"] = int(sum(v["n"] for v in vzw.values()))
stats["T2_vzw_max_missing_share"] = float(max(v["missing_stamp_share"] for v in vzw.values()))
stats["T2_vzw_min_share_over_20"] = float(min(v["share_over_20"] for v in vzw.values()))
ie5_traces = [airtime(g["dl"].values) for _, g in irish[irish["mode"] == "5G"].groupby("file") if len(g)]   # same rule as ie5_air
tr_n = np.array([len(x) for x in ie5_traces])
def tshare(thr, B=20000):          # cluster bootstrap of a share: resample whole drives, pooled share per replicate
    k = np.array([(x > thr).sum() for x in ie5_traces]); pick = rng.integers(0, len(ie5_traces), (B, len(ie5_traces)))
    v = k[pick].sum(1) / tr_n[pick].sum(1)
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
def tmedian(B=4000):
    vals = [np.median(np.concatenate([ie5_traces[i] for i in rng.integers(0, len(ie5_traces), len(ie5_traces))])) for _ in range(B)]
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
stats["ie5_trace_bootstrap_95ci"] = {"n_traces": len(ie5_traces), "B_shares": 20000, "share_over_2": tshare(2),
                                     "share_over_20": tshare(20), "share_over_100": tshare(100), "p50": tmedian()}
# U.S. samples are consecutive 1-s samples (autocorrelated): moving-block bootstrap, blocks of 50 samples (20/200 give
# the same intervals to within a point); drawn after the Irish bootstrap so its intervals do not move
def bboot(a, fn, L=50, B=1000):
    n = len(a); nb = int(np.ceil(n / L)); vals = []
    for _ in range(B):
        st = rng.integers(0, n - L + 1, nb); x = np.concatenate([a[k:k + L] for k in st])[:n]; vals.append(fn(x))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
stats["us_block_bootstrap_95ci"] = {"block_len": 50, "share_over_2": bboot(us_air, lambda x: (x > 2).mean()),
                                    "share_over_20": bboot(us_air, lambda x: (x > 20).mean())}
json.dump(stats, open(os.path.join(ROOT, "results", "fig2_stats.json"), "w"), indent=1)
print("robustness:", stats["T2_vzw_total_n"], stats["T2_vzw_max_missing_share"], stats["T2_vzw_min_share_over_20"], stats["ie5_trace_bootstrap_95ci"])

