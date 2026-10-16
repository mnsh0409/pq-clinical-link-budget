"""
urllc_transmission.py -- can a cold post-quantum handshake fit a clinical latency
budget on each wireless link class, and where does the time go (bytes on air vs
computation vs round trips)?

Inputs (all ledger): handshake sizes (C0/C1/C2 as in mobility_handshake_budget.py),
link PHY rates and per-frame payload limits, pqm4 cycle counts at 24 MHz, the
Tasopoulos measured handshake at 180 MHz, 3GPP medical latency budgets.

Serialization model (lower bound on airtime): frames = ceil(B / payload_per_frame);
airtime = frames * frame_size * 8 / PHY_rate.  No MAC contention, ACKs, retries,
duty cycling or scheduling delay -- so real times are longer.  For links whose
"rate" is an application-level or peak figure, airtime = B*8/rate.
"""
import math
from common import p, cid, derived, fmt_time, fmt_bytes, save

C0 = p("tls_hs_bytes_ecdsa_ecdhe")
C1 = C0 - 2 * p("p256_uncompressed_point_B") + p("kex_x25519mlkem768_client_B") + p("kex_x25519mlkem768_server_B")
C2 = p("tls_hs_bytes_dil3_kyb3")
C2_UNI = C2 - p("mldsa65_pk_B") - 2 * p("mldsa65_sig_B")   # derived: drop the client certificate (one key + one CA signature) and the client CertificateVerify
HS = {"C0_classical": C0, "C1_hybrid_kex": C1, "C2_full_pq": C2, "C2_server_only_derived": C2_UNI}
KEX_ONLY = p("kex_x25519mlkem768_client_B") + p("kex_x25519mlkem768_server_B")   # 2336 B, the key-share bytes alone

# ---------------------------------------------------------------- link classes
LINKS = [
 # name, rate bit/s, payload per frame (None = no framing model), frame size on air, ledger keys, condition
 {"name": "IEEE 802.15.4 / 6LoWPAN, 2.4 GHz (AES-CCM-128 link security)", "rate": p("ieee802154_rate_bps"),
  "payload": p("ieee802154_payload_ccm128_B"), "frame": p("ieee802154_phy_max_B"),
  "ledger": [cid("ieee802154_rate_bps"), cid("ieee802154_payload_ccm128_B"), cid("ieee802154_phy_max_B")],
  "condition": "250 kb/s PHY, 127-B frames, 81 B payload after MAC + CCM-128 overhead (RFC 4944 §4)"},
 {"name": "IEEE 802.15.6 WBAN narrowband, lowest PHY rate", "rate": p("wban_nb_rate_min_bps"),
  "payload": p("wban_frame_body_max_B"), "frame": p("wban_frame_body_max_B") + 9,
  "ledger": [cid("wban_nb_rate_min_bps"), cid("wban_frame_body_max_B")],
  "condition": "75.9 kb/s; 255-B frame body; +9 B MAC header/FCS assumed (SECONDARY sources; 2012 standard)"},
 {"name": "IEEE 802.15.6 WBAN narrowband, highest PHY rate", "rate": p("wban_nb_rate_max_bps"),
  "payload": p("wban_frame_body_max_B"), "frame": p("wban_frame_body_max_B") + 9,
  "ledger": [cid("wban_nb_rate_max_bps"), cid("wban_frame_body_max_B")], "condition": "971.4 kb/s"},
 {"name": "Bluetooth LE 1M (application-rate approximation)", "rate": p("ble_le1m_app_bps_approx"),
  "payload": p("ble_ll_payload_B"), "frame": None,
  "ledger": [cid("ble_le1m_app_bps_approx"), cid("ble_ll_payload_B")],
  "condition": "~800 kb/s application throughput per Bluetooth SIG Primer; 251-B LL payload (Core 4.2+)"},
 {"name": "Bluetooth LE 2M (application-rate approximation)", "rate": p("ble_le2m_app_bps_approx"),
  "payload": p("ble_ll_payload_B"), "frame": None, "ledger": [cid("ble_le2m_app_bps_approx")], "condition": "~1400 kb/s"},
 {"name": "NB-IoT uplink (peak, multi-tone)", "rate": p("nbiot_peak_ul_bps"), "payload": None, "frame": None,
  "ledger": [cid("nbiot_peak_ul_bps")], "condition": "66 kb/s peak per GSMA (Cat-NB1); the client share travels uplink"},
 {"name": "NB-IoT downlink (peak)", "rate": p("nbiot_peak_dl_bps"), "payload": None, "frame": None,
  "ledger": [cid("nbiot_peak_dl_bps")], "condition": "26 kb/s peak per GSMA"},
 {"name": "LTE-M half-duplex uplink", "rate": p("ltem_hd_ul_bps"), "payload": None, "frame": None,
  "ledger": [cid("ltem_hd_ul_bps")], "condition": "~380 kb/s per GSMA"},
 {"name": "5G NR uplink, measured in a clinical deployment (Chen 2024 avg)", "rate": p("ul_5gsa_chen2024_avg_bps"), "payload": None, "frame": None,
  "ledger": [cid("ul_5gsa_chen2024_avg_bps")], "condition": "91 Mb/s average upload, private 5G SA hospital network"},
 {"name": "5G NR uplink, measured during telesurgery (Ye 2026)", "rate": p("ul_5g_ye2026_bps"), "payload": None, "frame": None,
  "ledger": [cid("ul_5g_ye2026_bps")], "condition": "101 Mb/s upstream at the 5G CPE side"},
]

def airtime(B, link):
    if link["payload"] and link["frame"]:
        frames = math.ceil(B / link["payload"])
        return frames, frames * link["frame"] * 8 / link["rate"]
    if link["payload"]:
        frames = math.ceil(B / link["payload"])
        return frames, B * 8 / link["rate"]
    return None, B * 8 / link["rate"]

BUDGETS = {
 "RAS local <2 ms (TS 22.104)": p("ras_local_latency_ms") / 1e3,
 "RAS remote / RAD <20 ms (TS 22.104)": p("rad_latency_ms") / 1e3,
 "cardiac telemetry <100 ms (TR 22.826, SECONDARY)": p("telemetry_latency_ms") / 1e3,
 "Tactile Internet 1 ms RTT (ITU-T 2014)": p("tactile_rtt_ms") / 1e3,
}

table = []
for link in LINKS:
    row = {"link": link["name"], "condition": link["condition"], "rate_bps": link["rate"], "ledger": link["ledger"]}
    for hs_name, B in HS.items():
        frames, t = airtime(B, link)
        row[hs_name] = {"bytes": B, "frames": frames, "airtime_s": t, "airtime": fmt_time(t),
                        "x_budget": {bn: round(t / bv, 1) for bn, bv in BUDGETS.items()}}
    table.append(row)

# ---------------------------------------------------------------- device computation (Cortex-M4)
clk24 = p("pqm4_clock_Hz"); clk180 = p("tasopoulos_clock_Hz")
kem_client_cyc = p("pqm4_mlkem768_keygen_cyc_m4fspeed") + p("pqm4_mlkem768_decaps_cyc_m4fspeed")   # client: keygen + decaps
kem_server_cyc = p("pqm4_mlkem768_encaps_cyc_m4fspeed")
sig_verify_cyc = p("pqm4_mldsa65_verify_cyc_m4f")
sig_sign_cyc = p("pqm4_mldsa65_sign_cyc_m4f")
def ms(cyc, clk): return cyc / clk * 1e3
compute = {
 "note": "pqm4 counts are at 24 MHz on a Cortex-M4 (Nucleo-L4R5ZI default board); the 180 MHz column is a linear rescaling (assumption: no wait states) and is bracketed by the Tasopoulos measurement on a 180 MHz Cortex-M4",
 "ML-KEM-768 client (keygen+decaps)": {"cycles": kem_client_cyc, "ms_at_24MHz": round(ms(kem_client_cyc, clk24), 1), "ms_at_180MHz_scaled": round(ms(kem_client_cyc, clk180), 1),
     "ledger": [cid("pqm4_mlkem768_keygen_cyc_m4fspeed"), cid("pqm4_mlkem768_decaps_cyc_m4fspeed")]},
 "ML-KEM-768 server (encaps)": {"cycles": kem_server_cyc, "ms_at_24MHz": round(ms(kem_server_cyc, clk24), 1), "ms_at_180MHz_scaled": round(ms(kem_server_cyc, clk180), 1),
     "ledger": [cid("pqm4_mlkem768_encaps_cyc_m4fspeed")]},
 "ML-DSA-65 verify (one certificate or CertificateVerify)": {"cycles": sig_verify_cyc, "ms_at_24MHz": round(ms(sig_verify_cyc, clk24), 1), "ms_at_180MHz_scaled": round(ms(sig_verify_cyc, clk180), 1),
     "ledger": [cid("pqm4_mldsa65_verify_cyc_m4f")]},
 "ML-DSA-65 sign (mutual auth, client)": {"cycles": sig_sign_cyc, "ms_at_24MHz": round(ms(sig_sign_cyc, clk24), 1), "ms_at_180MHz_scaled": round(ms(sig_sign_cyc, clk180), 1),
     "ledger": [cid("pqm4_mldsa65_sign_cyc_m4f")]},
 "client total, unilateral auth (KEM client + 2 verifies)": {"ms_at_24MHz": round(ms(kem_client_cyc + 2 * sig_verify_cyc, clk24), 1), "ms_at_180MHz_scaled": round(ms(kem_client_cyc + 2 * sig_verify_cyc, clk180), 1),
     "assumption": "two signature verifications (server CertificateVerify + one CA certificate)"},
 "measured full PQ-TLS handshake, client, 180 MHz, wired (Tasopoulos 2022)": {"ms": p("tls_hs_ms_client_dil3_kyb3"), "ledger": cid("tls_hs_ms_client_dil3_kyb3")},
 "measured classical handshake, client, 180 MHz, wired": {"ms": p("tls_hs_ms_client_ecdsa_ecdhe"), "ledger": cid("tls_hs_ms_client_ecdsa_ecdhe")},
 "measured energy per handshake, client, mutual auth (CF'23)": {"PQ_mJ": p("tls_hs_mJ_client_mut_dil3_kyb3"), "classical_mJ": p("tls_hs_mJ_client_mut_ecdsa_ecdhe"),
     "ledger": [cid("tls_hs_mJ_client_mut_dil3_kyb3"), cid("tls_hs_mJ_client_mut_ecdsa_ecdhe")]},
}

# wearable energy envelope: how many PQ handshakes per day would spend 1% of a 1000 mAh 3.3 V battery over one month?
battery_J = p("wearable_battery_mAh_max") / 1000.0 * 3600 * p("wearable_battery_V")     # 1000 mAh * 3.3 V = 11,880 J
hs_J = p("tls_hs_mJ_client_mut_dil3_kyb3") / 1000.0
per_day_1pct_month = 0.01 * battery_J / hs_J / 30.0
energy = {"battery_J": battery_J, "pq_handshake_J": hs_J,
          "handshakes_per_day_costing_1pct_battery_over_30_days": round(per_day_1pct_month),
          "ledger": [cid("wearable_battery_mAh_max"), cid("wearable_battery_V"), cid("wearable_life_months_min"), cid("tls_hs_mJ_client_mut_dil3_kyb3")],
          "assumption": "TR 22.826 wearable envelope (3.3 V, <1000 mAh, >=1 month); Tasopoulos bench energy (180 MHz Cortex-M4, wired Ethernet, radio energy excluded)",
          "reading": "the handshake's cryptographic energy is not the wearable's constraint; radio airtime for 20 kB on a constrained link is (not measured here)"}

# ---------------------------------------------------------------- per-packet overhead (unchanged by PQ migration)
TAG = 16          # AEAD tag, bytes (AES-GCM / ChaCha20-Poly1305 / AES-CCM-128)
DTLS13_HDR = 5    # DTLS 1.3 unified header: 1 B flags + 2 B seq + 2 B length (assumption: 16-bit seq, length present, no CID)
INNER_TYPE = 1    # TLSInnerPlaintext content-type byte (TLS 1.3 / DTLS 1.3), encrypted with the payload
CID_B = 4         # example connection-identifier length for the CID variant (RFC 9147 sec. 9 allows 0-255 B)
payloads = {
 "haptic 3-DoF (Aijaz 2017)": p("haptic_payload_3dof_B"),
 "surgery sensor msg (TR 22.826)": p("surgery_sensor_msg_B"),
 "RAD msg (TS 22.104)": p("rad_msg_B"),
 "RAS min msg (TS 22.104)": p("ras_local_msg_lo_B"),
 "RAS max msg (TS 22.104)": p("ras_local_msg_hi_B"),
 "telemetry max msg (TR 22.826)": p("telemetry_msg_max_B"),
}
OVH = TAG + DTLS13_HDR + INNER_TYPE
pp = {name: {"payload_B": B, "overhead_B": OVH, "overhead_pct": round(100.0 * OVH / B, 1),
             "overhead_pct_with_4B_cid": round(100.0 * (OVH + CID_B) / B, 1)} for name, B in payloads.items()}
pp["note"] = ("per-record cost is symmetric (AEAD) and identical before and after PQ migration; PQ changes the handshake and "
              "certificates only. 16-B tag + 5-B DTLS 1.3 unified header + 1-B inner content type = 22 B assumed; a connection "
              "identifier adds its length (4 B shown); AES-CCM-8 profiles (RFC 7925) halve the tag; IP/UDP headers excluded.")

resume = {}
for link in LINKS:
    if "802.15.4" in link["name"]:
        _, t = airtime(KEX_ONLY, link); resume["802.15.4, both shares"] = {"bytes": KEX_ONLY, "airtime_s": t}
    if link["name"].startswith("NB-IoT uplink"):
        _, tu = airtime(p("kex_x25519mlkem768_client_B"), link); resume.setdefault("NB-IoT, client share uplink + server share downlink", {})["uplink_s"] = tu
    if link["name"].startswith("NB-IoT downlink"):
        _, td = airtime(p("kex_x25519mlkem768_server_B"), link); resume.setdefault("NB-IoT, client share uplink + server share downlink", {})["downlink_s"] = td
r = resume["NB-IoT, client share uplink + server share downlink"]; r["total_s"] = r["uplink_s"] + r["downlink_s"]; r["bytes"] = KEX_ONLY
resume["note"] = "psk_dhe_ke resumption re-sends the hybrid key shares (RFC 9846 sec. 4.2.9/2.2); psk_ke sends none but has no forward secrecy"

# F20: clock sensitivity of the client computation and the ML-DSA-65 signing range (rejection sampling)
clk64 = 64e6
compute["client total, unilateral auth, ms_at_64MHz_scaled"] = round(ms(kem_client_cyc + 2 * sig_verify_cyc, clk64), 1)
compute["ML-DSA-65 sign range (pqm4 MIN/MAX of 1000 executions, m4f)"] = {"cycles_min": 2918295, "cycles_max": 26008621,
    "ms_at_24MHz_min": round(ms(2918295, clk24), 1), "ms_at_24MHz_max": round(ms(26008621, clk24), 1),
    "ledger": "PQC-04 quote (g) in sources/constrained-pqc-links.md (benchmarks.md row ml-dsa-65 m4f)"}

# F21: server first-flight bounds per configuration and what each transport lets the server send first (RFC-07)
srv_C2_max = C2 - p("mlkem768_ek_B") - p("mldsa65_pk_B") - 2 * p("mldsa65_sig_B")   # total less client share, client cert (key + CA sig), client CertificateVerify
srv_C2_min = p("mlkem768_ct_B") + p("mldsa65_pk_B") + 2 * p("mldsa65_sig_B")        # ciphertext + server cert (key + CA sig) + server CertificateVerify
srv_C1_max = C1 - p("kex_x25519mlkem768_client_B")
srv_C0_max = C0 - p("p256_uncompressed_point_B")
tcp_iw_B = p("tcp_iw_segments") * p("tcp_mss_ethernet_B")
quic_one_dgram_allow = p("quic_amplification_factor") * p("quic_initial_min_udp_payload_B")
first_flight = {"server_flight_C2_B": {"min": srv_C2_min, "max": srv_C2_max},
  "server_flight_C1_max_B": srv_C1_max, "server_flight_C0_max_B": srv_C0_max,
  "tcp_initial_window_B_at_mss1460": tcp_iw_B, "C2_fits_tcp_iw": srv_C2_max <= tcp_iw_B,
  "quic_allowance_after_one_1200B_datagram_B": quic_one_dgram_allow,
  "C1_fits_quic_after_one_datagram": srv_C1_max <= quic_one_dgram_allow,
  "quic_client_bytes_needed_for_C2_B": srv_C2_min / p("quic_amplification_factor"),
  "C2_one_send_with_one_tx_cert_per_side": "a side sending two ML-DSA-65 certificates needs >= 2*(pk+sig)+sig bytes; with the other side's cert+CV and both KEM objects this exceeds the 20,224-B total, so each side sends one certificate",
  "C2_with_two_certs_one_side_min_B": 2 * (p("mldsa65_pk_B") + p("mldsa65_sig_B")) + p("mldsa65_sig_B") + p("mldsa65_pk_B") + 2 * p("mldsa65_sig_B") + p("mlkem768_ek_B") + p("mlkem768_ct_B"),
  "ledger": ["RFC-07", "PQC-02", "SEC-06b", "SEC-06d", "PQC-05"]}

out = {"handshake_bytes": {**HS, "key_share_bytes_only_X25519MLKEM768": KEX_ONLY,
                           "C2_server_only_derivation": "C2 - ML-DSA-65 public key (1952 B) - 2 x ML-DSA-65 signature (3309 B): client certificate and CertificateVerify removed; FIPS 204 sizes, 16 B above Dilithium3 per signature"},
       "resumption_key_share_airtime": resume, "first_flight": first_flight, "budgets_s": BUDGETS,
       "airtime_table": table, "device_compute": compute, "wearable_energy": energy, "per_packet_overhead": pp,
       "reading": [
         "On every constrained radio (802.15.4, WBAN, BLE, NB-IoT, LTE-M) a cold full-PQ handshake's airtime alone is 10^2-10^4 times the 2 ms surgery budget and 1-60 times the 100 ms telemetry budget; even the hybrid-KEM-only configuration exceeds 2 ms on all of them.",
         "On 5G-class uplinks the bytes serialize in ~2 ms, so the round trip (10-28 ms measured; 25.77 ms LEO) is what breaks the 2 ms budget -- not the bytes.",
         "On a 24 MHz Cortex-M4 the client's computation (KEM + two ML-DSA-65 verifications) is ~260 ms, comparable to the airtime on a 250 kb/s link; on a 180 MHz M4 it is ~35 ms (measured full handshake 157 ms incl. wolfSSL and Ethernet). The August plan's claim that 'computation is not the binding constraint' holds for x86-class endpoints only; on sensor-class MCUs computation and transmission are both binding.",
         "Conclusion for the design section: key establishment must be pre-established and amortised (PSK resumption, DTLS CID, session survival across handovers); the per-packet cost inside the control loop is symmetric and unchanged."]}
save("urllc_transmission.json", out)

print(f"Handshake bytes: {HS}; key shares alone {KEX_ONLY} B\n")
print(f"{'link':<62} {'C0 2.35kB':>10} {'C1 4.56kB':>10} {'C2 20.2kB':>10}   C2 vs 2 ms / 20 ms / 100 ms")
for r in table:
    xb = r['C2_full_pq']['x_budget']
    print(f"{r['link'][:62]:<62} {r['C0_classical']['airtime']:>10} {r['C1_hybrid_kex']['airtime']:>10} {r['C2_full_pq']['airtime']:>10}   {xb['RAS local <2 ms (TS 22.104)']:>7}x / {xb['RAS remote / RAD <20 ms (TS 22.104)']:>6}x / {xb['cardiac telemetry <100 ms (TR 22.826, SECONDARY)']:>5}x")
print("\nDevice compute (Cortex-M4):")
for k, v in compute.items():
    if isinstance(v, dict) and 'ms_at_24MHz' in v:
        print(f"  {k:<58} {v['ms_at_24MHz']:>7} ms @24 MHz   {v['ms_at_180MHz_scaled']:>6} ms @180 MHz (scaled)")
print(f"  measured full PQ handshake @180 MHz wired: {p('tls_hs_ms_client_dil3_kyb3')} ms; classical {p('tls_hs_ms_client_ecdsa_ecdhe')} ms")
print(f"\nWearable energy: {energy['handshakes_per_day_costing_1pct_battery_over_30_days']} PQ handshakes/day = 1% of a 1000 mAh battery over 30 days (crypto only)")
print("\nPer-packet AEAD overhead (unchanged by PQ):")
for k, v in pp.items():
    if isinstance(v, dict): print(f"  {k:<34} payload {v['payload_B']:>5} B  overhead {v['overhead_pct']:>6}%")
