"""
tables.py -- Tables I-II of the paper (and tab3_handshakes.tex, the configuration table that v1.6 folded
into Sec. III and the Table II caption) as LaTeX fragments, generated from
sources/ledger.json and results/urllc_transmission.json so that every cell is traceable.
Writes ../paper/tables/*.tex
"""
import os, json
from common import p, cid, PARAMS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "paper", "tables"); os.makedirs(OUT, exist_ok=True)
ut = json.load(open(os.path.join(ROOT, "results", "urllc_transmission.json")))

def kb(bps):
    if bps >= 1e6: return f"{bps/1e6:.3g}\\,Mb/s"
    if bps >= 1e3: return f"{bps/1e3:.3g}\\,kb/s"
    return f"{bps:.3g}\\,b/s"

def ms(s):
    v = s * 1e3
    if v >= 1000: return f"{v/1000:.2f}\\,s"
    if v >= 100: return f"{v:.0f}"
    if v >= 10: return f"{v:.0f}"
    if v >= 1: return f"{v:.1f}"
    return f"{v:.2f}"

# ---------------------------------------------------------------- Table I: streams and budgets
rows = [
 ("Wearable ECG, survey rate", p("ecg_wban_bps"), "--", "movassaghi2014"),
 ("12-lead ECG, 12 bit, survey rate", p("ecg12_bps"), "--", "latre2011"),
 ("ICU monitor as archived, $8{\\times}125$\\,Hz${\\times}12$\\,bit", p("icu_mimic3_channels")*p("icu_mimic3_rate_Hz")*p("icu_mimic3_bits_hi"), "--", "mimic3wdb"),
 ("Cardiac telemetry, TR 22.826", p("telemetry_inhospital_rate_bps"), "$<$100\\,ms", "tr22826"),
 ("RAD, 80\\,B/1\\,ms", (p("rad_rate_lo_bps"), p("rad_rate_hi_bps")), "$<$20\\,ms", "ts22104"),   # TS 22.104 service bit rate 2-16 Mbit/s (MED-04c); 80 B/1 ms alone would be 640 kb/s
 ("RAS, local link, 250--2,000\\,B/1\\,ms", (p("ras_local_rate_lo_bps"), p("ras_local_rate_hi_bps")), "$<$2\\,ms", "ts22104"),   # MED-04a
 ("RAS, remote ($<$400\\,km)", (p("ras_remote_rate_lo_bps"), p("ras_remote_rate_hi_bps")), "$<$20\\,ms", "ts22104"),   # MED-04b
 ("Ambulance vital signs, TR 22.826", p("ambulance_vitals_rate_bps"), "$<$100\\,ms", "tr22826"),
 # v1.8: row dropped for space (not used in the text): ("Ambulance video, measured", p("ambulance_video_measured_bps"), "$<$100\\,ms~\\cite{tr22826}", "berlet2022"),
 # v1.8: row dropped for space (not used in the text): ("Surgical video, measured", p("surg_video_measured_ye2026_bps"), "--", "ye2026"),
]
L = []
L.append("\\begin{tabular}{@{}lrr@{}}\\toprule")
L.append("Stream & Rate & Latency req. \\\\ \\midrule")
for name, bps, basis, key in rows:
    rate = (f"{bps[0]/1e6:.0f}--{bps[1]/1e6:.0f}\\,Mb/s" if isinstance(bps, tuple) else kb(bps))   # v1.9 proofreading: the 3GPP service bit rates from the ledger
    L.append(f"{name}~\\cite{{{key}}} & {rate} & {basis} \\\\")
L.append("\\bottomrule\\end{tabular}")
open(os.path.join(OUT, "tab1_streams.tex"), "w").write("\n".join(L) + "\n")

# ---------------------------------------------------------------- Table II: link classes and airtime
short = {
 "IEEE 802.15.4 / 6LoWPAN, 2.4 GHz (AES-CCM-128 link security)": ("802.15.4, 81\\,B/frame", "rfc4944"),
 "IEEE 802.15.6 WBAN narrowband, lowest PHY rate": ("802.15.6 NB, lowest", "culjak2020"),
 "IEEE 802.15.6 WBAN narrowband, highest PHY rate": ("802.15.6 NB, highest", "culjak2020"),
 "Bluetooth LE 1M (application-rate approximation)": ("BLE 1M, app.\\ rate", "blesig"),
 "Bluetooth LE 2M (application-rate approximation)": ("BLE 2M, app.\\ rate", "blesig"),
 "NB-IoT uplink (peak, multi-tone)": ("NB-IoT UL, peak", "gsmanbiot"),
 "NB-IoT downlink (peak)": ("NB-IoT DL, peak", "gsmanbiot"),
 "LTE-M half-duplex uplink": ("LTE-M UL, half duplex", "gsmanbiot"),
 "5G NR uplink, measured in a clinical deployment (Chen 2024 avg)": ("5G UL, hospital, meas.", "chen2024"),
 "5G NR uplink, measured during telesurgery (Ye 2026)": ("5G UL, telesurgery, meas.", "ye2026"),
}
L = []
L.append("\\begin{tabular}{@{}lrrrrr@{}}\\toprule")
L.append("Link class & Rate & C0 & C1 & C2 & $<$100\\,ms \\\\ \\midrule")
tel = p("telemetry_latency_ms") / 1e3
for r in ut["airtime_table"]:
    name, key = short[r["link"]]
    c0, c1, c2 = (r[k]["airtime_s"] for k in ("C0_classical", "C1_hybrid_kex", "C2_full_pq"))
    # C0 / C1 / C2 airtime below the 100 ms telemetry budget; n/a where the link cannot carry the 0.5 Mb/s stream itself
    v = "n/a" if r["rate_bps"] < p("telemetry_inhospital_rate_bps") else "/".join("yes" if c < tel else "no" for c in (c0, c1, c2))
    L.append(f"{name}~\\cite{{{key}}} & {kb(r['rate_bps'])} & {ms(c0)} & {ms(c1)} & {ms(c2)} & {v} \\\\")
L.append("\\bottomrule\\end{tabular}")
open(os.path.join(OUT, "tab2_links.tex"), "w").write("\n".join(L) + "\n")

# ---------------------------------------------------------------- Table III: handshake configurations
C0 = p("tls_hs_bytes_ecdsa_ecdhe")
C1 = C0 - 2 * p("p256_uncompressed_point_B") + p("kex_x25519mlkem768_client_B") + p("kex_x25519mlkem768_server_B")
C2 = p("tls_hs_bytes_dil3_kyb3")
L = []
L.append("\\begin{tabular}{@{}llrl@{}}\\toprule")
L.append("Config. & Key exchange / authentication & Bytes & Basis \\\\ \\midrule")
L.append(f"C0 & ECDHE / ECDSA P-256, mutual & {C0:,} & measured~\\cite{{tasopoulos2022}} \\\\")
L.append(f"C1 & X25519MLKEM768 / ECDSA & {C1:,} & C0 + hybrid shares~\\cite{{rfc10024}} \\\\")
L.append(f"C2 & Kyber-768 / Dilithium-3, mutual & {C2:,} & measured~\\cite{{tasopoulos2022}} \\\\")
C2U = C2 - p("mldsa65_pk_B") - 2 * p("mldsa65_sig_B")
L.append(f"C2$'$ & C2, server-only auth. & {C2U:,} & C2 $-$ client cert./CV \\\\")
L.append("\\bottomrule\\end{tabular}")
open(os.path.join(OUT, "tab3_handshakes.tex"), "w").write("\n".join(L) + "\n")
print("tables written:", os.listdir(OUT))
print("C0,C1,C2 =", C0, C1, C2)
