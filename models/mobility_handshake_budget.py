"""
mobility_handshake_budget.py -- what post-quantum key establishment costs when a
clinical stream's session must be re-established under mobility.

Three handshake configurations (bytes on the wire):
  C0  classical TLS 1.3, ECDSA+ECDHE secp256r1 ........ 2,353 B  measured [PQC-05]
  C1  hybrid X25519MLKEM768 key exchange, classical auth  derived: C0 with the two
      65-byte P-256 shares replaced by the 1216-B / 1120-B hybrid shares [SEC-06b/c/d]
  C2  full PQ (Dilithium3 + Kyber768 = ML-DSA-65/ML-KEM-768 analogue) 20,224 B measured [PQC-05]

Re-establishment triggers (each is a *model*; the paper states which one applies):
  T1  one full handshake per handover  -- an UPPER BOUND.  5G carries the PDU session
      and derives new AS keys at handover from the existing context (TS 33.501 §6.9.2,
      SEC-01), so an application session need not re-handshake; T1 is what happens
      if the transport session is torn down (address change, NAT rebinding without
      CID, app design).
  T2  one handshake per session loss, with loss probability f per handover
      (no public RLF-per-handover statistic: MOB-03 NOT-FOUND -> f swept 1, 5, 10 %).
  T3  policy re-handshake every T hours (PQ forward secrecy); TLS KeyUpdate is
      symmetric and costs nothing PQ-specific.
  T4  NTN: one handshake per LEO cell dwell (TR 38.821: 132.28 s in a 1000 km cell,
      stationary UE, SECONDARY) as the bound; Rel-18 satellite switch with re-sync
      keeps the same PCI in quasi-earth-fixed cells (NTN-06c), so this is again a bound.

Handover rates:
  measured  Hassan et al. SIGCOMM'22: NSA 5G every 0.4 km, SA every 0.9 km,
            mmWave every 0.13 km (freeway); 553 HO/h at 130 km/h [MOB-02]
  analytic  Lin et al. 2013: H = (4/pi) v sqrt(mu) with mu the BS density [MOB-01];
            mu from the TR 38.913 ISDs assuming a hexagonal grid: mu = 2/(sqrt(3) ISD^2)
"""
import math
from common import p, cid, derived, fmt_bytes, fmt_time, save

# ---------------------------------------------------------------- handshake bytes
C0 = p("tls_hs_bytes_ecdsa_ecdhe")
C1 = C0 - 2 * p("p256_uncompressed_point_B") + p("kex_x25519mlkem768_client_B") + p("kex_x25519mlkem768_server_B")
C2 = p("tls_hs_bytes_dil3_kyb3")
HS = {
 "C0_classical": derived(C0, "byte", ["tls_hs_bytes_ecdsa_ecdhe"]),
 "C1_hybrid_kex_classical_auth": derived(C1, "byte",
     ["tls_hs_bytes_ecdsa_ecdhe", "p256_uncompressed_point_B", "kex_x25519mlkem768_client_B", "kex_x25519mlkem768_server_B"],
     assumption="the measured classical handshake carries one 65-B P-256 share per direction; each is replaced by the hybrid share"),
 "C2_full_pq": derived(C2, "byte", ["tls_hs_bytes_dil3_kyb3"],
     note="pre-FIPS Dilithium3/Kyber768 sizes; ML-DSA-65 sig 3309 B vs Dilithium3 3293 B and identical Kyber768/ML-KEM-768 sizes -> +16 B per signature"),
}

# ---------------------------------------------------------------- handover rates
def hex_density_per_m2(isd_m):
    return 2.0 / (math.sqrt(3.0) * isd_m ** 2)

def lin_rate_per_s(v_kmh, isd_m):
    v = v_kmh / 3.6
    return (4.0 / math.pi) * v * math.sqrt(hex_density_per_m2(isd_m))

scen = []
# analytic scenarios from TR 38.913 ISD + speed pairs
for name, isd_key, v_key in [
    ("urban macro, car", "isd_urban_macro_m", "ue_speed_urban_car_kmh"),
    ("dense urban, car", "isd_dense_urban_m", "ue_speed_urban_car_kmh"),
    ("rural, vehicle", "isd_rural_m", "ue_speed_rural_vehicle_kmh"),
    ("highway, low", "isd_highway_m", "ue_speed_highway_avg_kmh_lo"),
    ("highway, high", "isd_highway_m", "ue_speed_highway_avg_kmh_hi"),
    ("high-speed train", "isd_highway_m", "ue_speed_hst_max_kmh")]:
    H = lin_rate_per_s(p(v_key), p(isd_key))
    scen.append({"scenario": name, "kind": "analytic (Lin 2013, hex-grid density from TR 38.913 ISD)",
                 "speed_kmh": p(v_key), "isd_m": p(isd_key), "ho_per_h": round(H * 3600, 1),
                 "ledger": [cid("ho_rate_formula"), cid(isd_key), cid(v_key)]})
# measured scenarios (distance per HO x speed)
for name, dkey, v in [("NSA 5G freeway (low-band)", "ho_dist_nsa5g_freeway_km", 100),
                      ("NSA 5G freeway (low-band)", "ho_dist_nsa5g_freeway_km", 130),
                      ("SA 5G freeway", "ho_dist_sa5g_km", 100),
                      ("SA 5G freeway", "ho_dist_sa5g_km", 130),
                      ("NSA mmWave", "ho_dist_nsa_mmwave_km", 30),
                      ("NSA mmWave", "ho_dist_nsa_mmwave_km", 100),
                      ("4G freeway", "ho_dist_4g_freeway_km", 100)]:
    scen.append({"scenario": name, "kind": "measured distance per HO (Hassan 2022) x assumed speed",
                 "speed_kmh": v, "km_per_ho": p(dkey), "ho_per_h": round(v / p(dkey), 1),
                 "ledger": [cid(dkey)], "assumption": f"vehicle speed {v} km/h (the paper does not state the drive-test speed)"})
scen.append({"scenario": "5G at 130 km/h (authors' own figure)", "kind": "measured (Hassan 2022 §5.3)",
             "speed_kmh": p("ho_speed_for_553_kmh"), "ho_per_h": p("ho_per_hour_130kmh"),
             "ledger": [cid("ho_per_hour_130kmh")], "note": "basis (band/carrier) not stated in the paper; higher than 130/0.4 = 325"})
# NTN cell dwell (stationary UE)
scen.append({"scenario": "LEO 600 km, 1000 km earth-moving cell, stationary UE", "kind": "TR 38.821 cell dwell (SECONDARY)",
             "speed_kmh": 0, "ho_per_h": round(3600 / p("ntn_cell_dwell_1000km_s"), 1),
             "ledger": [cid("ntn_cell_dwell_1000km_s")]})
scen.append({"scenario": "LEO 600 km, 50 km cell, stationary UE", "kind": "TR 38.821 cell dwell (SECONDARY)",
             "speed_kmh": 0, "ho_per_h": round(3600 / p("ntn_cell_dwell_50km_s"), 1),
             "ledger": [cid("ntn_cell_dwell_50km_s")]})

# ---------------------------------------------------------------- streams to compare against
STREAMS = {
 "ECG wearable (3 kb/s)": ("ecg_wban_bps",),
 "ECG 12-lead (288 kb/s)": ("ecg12_bps",),
 "cardiac telemetry TR 22.826 (0.5 Mb/s)": ("telemetry_inhospital_rate_bps",),
 "ambulance vitals TR 22.826 (1 Mb/s)": ("ambulance_vitals_rate_bps",),
 "ambulance video measured (12 Mb/s)": ("ambulance_video_measured_bps",),
 "surgical video measured (40 Mb/s)": ("surg_video_measured_ye2026_bps",),
}

# ---------------------------------------------------------------- budgets
budget = []
for s in scen:
    ho_h = s["ho_per_h"]
    row = {"scenario": s["scenario"], "kind": s["kind"], "ho_per_h": ho_h, "ledger": s["ledger"]}
    for hs_name, hs in HS.items():
        B = hs["value"]
        row[hs_name] = {
            "T1_bytes_per_h": ho_h * B, "T1_pretty": fmt_bytes(ho_h * B),
            "T2_bytes_per_h_f1pct": 0.01 * ho_h * B, "T2_bytes_per_h_f5pct": 0.05 * ho_h * B, "T2_bytes_per_h_f10pct": 0.10 * ho_h * B,
            "T1_share_of_stream_pct": {name: round(100.0 * ho_h * B * 8 / (p(k[0]) * 3600), 2) for name, k in STREAMS.items()},
        }
    budget.append(row)

# policy re-handshake T3 (per hour) is simply B per hour: report share of stream
T3 = {hs_name: {name: round(100.0 * hs["value"] * 8 / (p(k[0]) * 3600), 4) for name, k in STREAMS.items()} for hs_name, hs in HS.items()}

# ---------------------------------------------------------------- latency of one re-establishment (1-RTT handshake)
# TLS 1.3 / DTLS 1.3 full handshake completes in one round trip after transport setup;
# serialization at the link rate is added by urllc_transmission.py.  Here: RTT anchors.
RTT = {
 "5G ambulance field test (Berlet 2022, parked, sliced core)": ("rtt_5g_berlet2022_ms",),
 "5G telesurgery demo (Moustris 2023, ~300 km, one 5G end)": ("rtt_5g_moustris2023_ms",),
 "LEO 600 km transparent (TR 38.821 max RTD)": ("ntn_rtd_leo600_transparent_ms",),
 "LEO 600 km regenerative": ("ntn_rtd_leo600_regen_ms",),
 "GEO transparent": ("ntn_rtd_geo_transparent_ms",),
}
lat = {}
for name, k in RTT.items():
    rtt = p(k[0])
    lat[name] = {"rtt_ms": rtt, "ledger": cid(k[0]),
                 "handshake_1rtt_ms": rtt, "with_transport_setup_2rtt_ms": 2 * rtt,
                 "vs_RAS_local_2ms": round(rtt / p("ras_local_latency_ms"), 1),
                 "vs_RAD_remote_20ms": round(rtt / p("rad_latency_ms"), 2),
                 "vs_telemetry_100ms": round(rtt / p("telemetry_latency_ms"), 2),
                 "vs_measured_5G_HO_interruption_NSA_167ms": round(rtt / p("ho_duration_nsa5g_ms"), 2)}

out = {"handshake_bytes": HS, "handover_scenarios": scen, "budget_T1_T2": budget,
       "policy_rehandshake_T3_share_of_stream_pct_per_hourly_handshake": T3,
       "reestablishment_latency": lat,
       "reading": [
         "T1 is an upper bound: 5G derives fresh AS keys at handover from the existing KAMF-rooted context (TS 33.501 §6.9.2.1.1, SECONDARY) and the PDU session persists; an application-layer PQ re-handshake per handover only happens if the transport session is torn down.",
         "Even so, for a 3 kb/s wearable ECG the per-handover full-PQ bound exceeds the stream itself at highway handover rates (see T1_share_of_stream_pct); DTLS CID (RFC 9146/9147) and PSK resumption (RFC 9846 §2.2) are the mechanisms that keep sessions across address changes.",
         "Every RTT anchor exceeds the 2 ms local-surgery budget by an order of magnitude and the LEO RTD exceeds the 20 ms remote budget: no key establishment can sit inside a URLLC control loop; it must be pre-established and rekeyed symmetrically."]}
save("mobility_handshake_budget.json", out)

print(f"Handshake bytes: C0 {C0} B, C1 {C1} B (derived), C2 {C2} B")
print("\nHandover scenarios (HO/h):")
for s in scen:
    print(f"  {s['ho_per_h']:>7} /h  {s['scenario']}  [{s['kind']}]")
print("\nT1 bound (one full-PQ handshake per handover) as % of stream volume:")
for r in budget:
    sh = r['C2_full_pq']['T1_share_of_stream_pct']
    print(f"  {r['scenario'][:48]:<48} {r['ho_per_h']:>6}/h  C2 {r['C2_full_pq']['T1_pretty']:>9}/h  ECG3k {sh['ECG wearable (3 kb/s)']:>8.1f}%  telemetry {sh['cardiac telemetry TR 22.826 (0.5 Mb/s)']:>6.2f}%  video40M {sh['surgical video measured (40 Mb/s)']:>6.3f}%")
print("\nHourly policy re-handshake (T3), C2 share of stream: " + ", ".join(f"{k}: {v:.4f}%" for k, v in T3['C2_full_pq'].items()))
print("\nRe-establishment latency (1-RTT handshake, transport excluded):")
for n, v in lat.items():
    print(f"  {v['rtt_ms']:>7} ms  {n}  -> {v['vs_RAS_local_2ms']}x the 2 ms local-surgery budget")
