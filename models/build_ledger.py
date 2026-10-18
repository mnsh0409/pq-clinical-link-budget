"""
build_ledger.py -- writes sources/ledger.json, the curated parameter set that the
model scripts read.  EVERY value here is copied from an entry in the five cluster
files under sources/ (ntn.md, medical-urllc.md, mobility-5g-security.md,
constrained-pqc-links.md, clinical-streams.md).  The `id` field is
the ledger entry; `status` is the entry's status tag (VERIFIED / SECONDARY).
No arithmetic is done here.  Derived quantities live in the model scripts and
must cite the ids they combine.

Run:  python3 build_ledger.py   (writes ../sources/ledger.json)
"""
import json, os, datetime

def P(value, unit, id_, status, condition, cite):
    return {"value": value, "unit": unit, "id": id_, "status": status,
            "condition": condition, "cite": cite}

CITES = {
 "ietf-mlkem-05": "K. Kwiatkowski, P. Kampanakis, B. E. Westerbaan, D. Stebila, 'Post-quantum hybrid ECDHE-MLKEM Key Agreement for TLSv1.3', draft-ietf-tls-ecdhe-mlkem-05, 26 May 2026 (IESG approved; RFC Editor queue, no RFC number on 2026-09-27)",
 "fips203": "NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, 13 Aug 2024",
 "fips204": "NIST FIPS 204, Module-Lattice-Based Digital Signature Standard, 13 Aug 2024",
 "falcon-cose-04": "draft-ietf-cose-falcon-04 (Mar 2026), Table 1; FIPS 206 unpublished as of 2026-09-27",
 "pqm4-falcon": "mupq/pqm4 benchmarks.md at commit 94435189596a70ee62815a9ff31f5bb5a74a3c8a (3 Feb 2025), last version listing Falcon-512; 24 MHz",
 "pqm4": "mupq/pqm4 benchmarks.md + README.md (GitHub master, accessed 2026-09-27); 24 MHz, arm-none-eabi-gcc 11.3.1; Nucleo-L4R5ZI default board",
 "tasopoulos2022": "G. Tasopoulos et al., 'Performance Evaluation of Post-Quantum TLS 1.3 on Resource-Constrained Embedded Systems', ISPEC 2022, LNCS 13620, pp. 432-451, doi:10.1007/978-3-031-21280-2_24 (IACR ePrint 2021/1553)",
 "tasopoulos2023": "G. Tasopoulos et al., 'Energy Consumption Evaluation of Post-Quantum TLS 1.3 for Resource-Constrained Embedded Devices', ACM CF'23, pp. 366-374, doi:10.1145/3587135.3592821 (IACR ePrint 2023/506)",
 "rfc4944": "RFC 4944, Transmission of IPv6 Packets over IEEE 802.15.4 Networks, Sept 2007",
 "rfc4919": "RFC 4919, 6LoWPAN overview, Aug 2007",
 "rfc8200": "RFC 8200, IPv6 Specification (STD 86), July 2017",
 "rfc9846": "RFC 9846, TLS 1.3, July 2026 (obsoletes RFC 8446)",
 "rfc9147": "RFC 9147, DTLS 1.3, April 2022",
 "rfc9000": "RFC 9000, QUIC: A UDP-Based Multiplexed and Secure Transport, May 2021",
 "rfc9002": "RFC 9002, QUIC Loss Detection and Congestion Control, May 2021",
 "liboqs-falcon": "open-quantum-safe/liboqs docs/algorithms/sig/falcon.yml at tag 0.16.0 (fetched 2026-10-17)",
 "rfc6928": "RFC 6928, J. Chu, N. Dukkipati, Y. Cheng, M. Mathis, Increasing TCP's Initial Window, April 2013",
 "rfc9146": "RFC 9146, Connection Identifier for DTLS 1.2, March 2022",
 "rfc7925": "RFC 7925, TLS/DTLS Profiles for the Internet of Things, July 2016",
 "ble-sig": "Bluetooth SIG: Karr 2017 blog (Core 4.2/5.0 payload and PHY); LE Primer v1.2.0 (2024); NIST SP 800-121r2-upd1 (LE Secure Connections P-256)",
 "ts36306": "3GPP TS 36.306 (ETSI TS 136 306 V13.2.0 / V14.2.0), UE radio access capabilities",
 "gsma-nbiot": "GSMA, 'What is the Difference in Data Throughput between LTE-M/NB-IoT and 3G or 4G?', 29 Oct 2019",
 "ieee802156": "IEEE Std 802.15.6-2012 via Culjak et al. Sensors 20(12):3587 2020; Ullah et al. IJDSN 9(4):950704 2013; Toorani arXiv:1501.02601. Superseded by IEEE 802.15.6-2026 (published 2026-08-28)",
 "tr38821": "3GPP TR 38.821 V16.0.0 (Rel-16), Solutions for NR to support NTN, Table 4.2-2 (ATIS transposition); latest V16.2.0",
 "tr38811": "3GPP TR 38.811 V15.3.0 (Rel-15), Study on NR to support NTN (ATIS transposition; some clauses via iTecSpec mirror)",
 "tr38913": "ETSI TR 138 913 V19.0.0 (2025-10) = 3GPP TR 38.913 V19.0.0, Tables 6.1.x-1 and clauses 7.7, 7.18",
 "ts38300": "3GPP TS 38.300 Rel-19 §16.14 (ETSI TS 138 300 V19.3.0 TOC; clause bodies via iTecSpec mirror)",
 "lin2013": "X. Lin, R. K. Ganti, P. J. Fleming, J. G. Andrews, 'Towards Understanding the Fundamentals of Mobility in Cellular Networks', IEEE TWC 2013 (arXiv:1204.3447v2, Prop. 7, Eq. 31)",
 "hassan2022": "A. Hassan et al., 'Vivisecting Mobility Management in 5G Cellular Networks', ACM SIGCOMM 2022, doi:10.1145/3544216.3544217 (NSF-PAR copy)",
 "ts33501": "3GPP TS 33.501 (ETSI TS 133 501 V19.7.0, 2026-08); clause text via iTecSpec Rel-20 mirror -- CHECK BY HAND before submission",
 "ts33210": "ETSI TS 133 210 V19.3.0 (2026-02) = 3GPP TS 33.210, NDS/IP, clauses 5.4.2 and 6.2",
 "tr33703": "3GPP TR 33.703, Study on transitioning to PQC in 3GPP, Rel-20, V20.0.1 (2026-07); 3GPP portal specificationId=4422",
 "ts35240": "ETSI TS 135 240 V18.0.0 (2024-05) / V19.0.0 (2026-03) = 3GPP TS 35.240, SNOW 5G 256-bit set (256-NEA4/NIA4/NCA4)",
 "cloudflare": "Cloudflare Blog: Radar Year in Review 15 Dec 2025 (52%); 'Cloudflare targets 2029 for full post-quantum security', 7 Apr 2026 (over 65%)",
 "gsma-pq05": "GSMA PQ.05, Quantum-safe Cryptography for 4G and 5G Roaming, v1.0, 26 June 2025",
 "gsma-pq07": "GSMA PQ.07, Post Quantum Cryptography for Non-Terrestrial Networks, v1.0, 4 Feb 2026",
 "ts22104": "ETSI TS 122 104 V19.2.0 (2026-01) = 3GPP TS 22.104 V19.2.0 Rel-19, Table 5.2-1",
 "rfc10024": "K. Kwiatkowski, P. Kampanakis, B. E. Westerbaan, D. Stebila, 'Post-Quantum Traditional (PQ/T) Hybrid Key Agreement Mechanisms for TLS 1.3', RFC 10024 (Proposed Standard), Aug 2026, doi:10.17487/RFC10024; the published form of draft-ietf-tls-ecdhe-mlkem-05, same share sizes (SEC-06f, read 2026-10-18)",
 "nistir8547": "D. Moody, R. Perlner, A. Regenscheid, A. Robinson, D. Cooper, 'Transition to Post-Quantum Cryptography Standards', NIST IR 8547 initial public draft, 12 Nov 2024; no final version listed on csrc.nist.gov on 2026-10-18 (SEC-09a)",
 "rfc7518": "M. Jones, 'JSON Web Algorithms (JWA)', RFC 7518, May 2015, Sec. 3.4 (ECDSA P-256 SHA-256 signature as R || S) (SEC-09b, read 2026-10-18)",
 "tr22826": "3GPP TR 22.826 V17.2.0 (Rel-17), Study on communication services for critical medical applications -- via tech-invite mirror (SECONDARY)",
 "ts22261": "3GPP TS 22.261 V19.14.0 (ETSI TS 122 261, 2026-07) clause 3.1; Table 7.11-1 via iTecSpec Rel-20 mirror",
 "itu-tactile-2014": "ITU-T Technology Watch Report, 'The Tactile Internet', Aug 2014",
 "itu-m2160": "Rec. ITU-R M.2160-0 (11/2023), Framework and overall objectives of IMT-2030",
 "ieee1918": "IEEE Std 1918.1-2024 (published 2026-01-23); latency figures via Holland et al., Proc. IEEE 107(2):256-279, 2019",
 "tian2020": "W. Tian et al., 'Telerobotic Spinal Surgery Based on 5G Network: The First 12 Cases', Neurospine 17(1):114-120, 2020",
 "ye2026": "Z. Ye et al., '5G wireless + wired network-based multi-console robotic telesurgery ... a case report', Transl. Androl. Urol. 15(4):140, 2026",
 "movassaghi2014": "S. Movassaghi et al., 'Wireless Body Area Networks: A Survey', IEEE COMST 16(3):1658-1686, 2014, Table II (accepted version)",
 "latre2011": "B. Latre et al., 'A survey on wireless body area networks', Wireless Networks 17(1):1-18, 2011, Table 1 (author manuscript)",
 "acns-g1": "ACNS Guideline 1 (Sinha et al.), J Clin Neurophysiol 33(4):303-307, 2016",
 "acns-g4": "ACNS Guideline 4 (Halford et al.), J Clin Neurophysiol 33(4):317-319, 2016",
 "kligfield2007": "P. Kligfield et al., AHA/ACCF/HRS ECG standardization Part I, Circulation 115:1306-1324, 2007 (JACC co-publication text)",
 "mimic3wdb": "Moody et al., MIMIC-III Waveform Database v1.0, PhysioNet 2020, doi:10.13026/c2607m",
 "vitaldb": "Lee et al., VitalDB, Scientific Data 9:279, 2022",
 "steinbach2012": "E. Steinbach et al., 'Haptic Communications', Proc. IEEE 100(4):937-956, 2012",
 "aijaz2017": "A. Aijaz et al., 'Realizing the Tactile Internet', IEEE Wireless Commun. 24(2):82-89, 2017 (arXiv:1510.02826)",
 "moustris2023": "G. Moustris et al., IJCARS 18(9):1577-1587, 2023, doi:10.1007/s11548-023-02913-2 (phantoms; 5G at surgeon side only)",
 "chen2024jmir": "B. Chen et al., J Med Internet Res 26:e52404, 2024, Table 3 and Results",
 "berlet2022": "M. Berlet et al., JMIR Formative Research 6(5):e36824, 2022 (5G ambulance field test, parked)",
 "herman2015": "S. T. Herman et al., Consensus Statement on Continuous EEG ... Part II, J Clin Neurophysiol 32(2):96-108, 2015",
 "chou2026": "M. Chou, P. Cao, arXiv:2604.24869 (2026): post-quantum chain size vs time to first byte (PQC-06, qualitative)",
}

L = {}

# ---------------------------------------------------------------- crypto sizes
L["kex_x25519mlkem768_client_B"] = P(1216, "byte", "SEC-06b", "VERIFIED", "TLS 1.3 ClientHello key_share, X25519MLKEM768 (1184 ML-KEM + 32 X25519)", "rfc10024")
L["kex_x25519mlkem768_server_B"] = P(1120, "byte", "SEC-06c", "VERIFIED", "TLS 1.3 ServerHello key_share (1088 ML-KEM + 32 X25519)", "rfc10024")
L["kex_secp256r1mlkem768_client_B"] = P(1249, "byte", "SEC-06d", "VERIFIED", "65 B secp256r1 + 1184 B ML-KEM", "rfc10024")
L["kex_secp256r1mlkem768_server_B"] = P(1153, "byte", "SEC-06d", "VERIFIED", "1088 B ML-KEM + 65 B secp256r1", "rfc10024")
L["mlkem768_ek_B"] = P(1184, "byte", "PQC-01", "VERIFIED", "FIPS 203 Table 3", "fips203")
L["mlkem768_dk_B"] = P(2400, "byte", "PQC-01", "VERIFIED", "FIPS 203 Table 3", "fips203")
L["mlkem768_ct_B"] = P(1088, "byte", "PQC-01", "VERIFIED", "FIPS 203 Table 3", "fips203")
L["mldsa65_pk_B"] = P(1952, "byte", "PQC-02", "VERIFIED", "FIPS 204 Table 2", "fips204")
L["mldsa65_sig_B"] = P(3309, "byte", "PQC-02", "VERIFIED", "FIPS 204 Table 2", "fips204")
L["mldsa44_pk_B"] = P(1312, "byte", "PQC-02", "VERIFIED", "FIPS 204 Table 2", "fips204")
L["mldsa44_sig_B"] = P(2420, "byte", "PQC-02", "VERIFIED", "FIPS 204 Table 2", "fips204")
L["falcon512_pk_B"] = P(897, "byte", "PQC-03", "SECONDARY", "FN-DSA-512 per draft-ietf-cose-falcon-04 Table 1; FIPS 206 not yet published", "falcon-cose-04")
L["falcon512_sig_B"] = P(666, "byte", "PQC-03", "SECONDARY", "as above", "falcon-cose-04")
L["mldsa65_category"] = P(3, "NIST security category", "PQC-02", "VERIFIED", "FIPS 204 Table 1, claimed security strength", "fips204")
L["falcon512_nist_level"] = P(1, "NIST security level", "PQC-03b", "VERIFIED", "liboqs 0.16.0 falcon.yml, Falcon-512 claimed-nist-level", "liboqs-falcon")
L["falcon1024_nist_level"] = P(5, "NIST security level", "PQC-03b", "VERIFIED", "liboqs 0.16.0 falcon.yml, Falcon-1024 claimed-nist-level", "liboqs-falcon")
L["falcon512_sig_max_B"] = P(752, "byte", "PQC-03b", "VERIFIED", "liboqs 0.16.0 falcon.yml, Falcon-512 (compressed) length-signature, a maximum", "liboqs-falcon")
# RFC-08: QUIC probe timeout form, borrowed by the X3 session-loss detector (fetched 2026-10-17)
L["pto_rttvar_factor"] = P(4, "ratio", "RFC-08", "VERIFIED", "RFC 9002 sec. 6.2.1: PTO = smoothed_rtt + max(4*rttvar, kGranularity) + max_ack_delay", "rfc9002")
L["pto_granularity_ms"] = P(1, "ms", "RFC-08", "VERIFIED", "RFC 9002 sec. 6.1.2: RECOMMENDED kGranularity 1 millisecond", "rfc9002")
L["p256_uncompressed_point_B"] = P(65, "byte", "SEC-06d", "VERIFIED", "secp256r1 share size as stated in RFC 10024 §4.1, as in draft-ietf-tls-ecdhe-mlkem-05 ('65 bytes for the secp256r1 part')", "rfc10024")
# RFC-07: what a transport lets a server send in its first flight (fetched 2026-10-15)
L["quic_amplification_factor"] = P(3, "ratio", "RFC-07", "VERIFIED", "RFC 9000 sec. 8.1: servers MUST NOT send more than three times as many bytes as received before validating the client address", "rfc9000")
L["quic_initial_min_udp_payload_B"] = P(1200, "byte", "RFC-07", "VERIFIED", "RFC 9000 sec. 8.1: UDP datagrams containing Initial packets have UDP payloads of at least 1200 bytes", "rfc9000")
L["tcp_iw_segments"] = P(10, "segment", "RFC-07", "VERIFIED", "RFC 6928: initial window upper bound min(10*MSS, max(2*MSS, 14600))", "rfc6928")
L["tcp_iw_cap_B"] = P(14600, "byte", "RFC-07", "VERIFIED", "RFC 6928: the 14600 in min(10*MSS, max(2*MSS, 14600))", "rfc6928")
L["tcp_mss_ethernet_B"] = P(1460, "byte", "RFC-07", "VERIFIED", "RFC 6928: 14600 = 10 x 1460 (MSS of a 1500-byte MTU); used only to state the window in bytes", "rfc6928")

# ------------------------------------------------- measured PQ-TLS handshakes (Cortex-M4, 180 MHz, wired Ethernet RTT 0.493 ms)
L["tls_hs_bytes_ecdsa_ecdhe"] = P(2353, "byte", "PQC-05", "VERIFIED", "Table 2 'Communication Sizes'; ECDSA+ECDHE secp256r1; wolfSSL; pre-FIPS", "tasopoulos2022")
L["tls_hs_bytes_dil2_kyb1"] = P(14748, "byte", "PQC-05", "VERIFIED", "Dilithium2 + Kyber512", "tasopoulos2022")
L["tls_hs_bytes_dil3_kyb3"] = P(20224, "byte", "PQC-05", "VERIFIED", "Dilithium3 + Kyber768 (pre-FIPS analogues of ML-DSA-65 + ML-KEM-768; notation confirmed 2026-09-27 re-fetch)", "tasopoulos2022")
L["tls_hs_ms_client_ecdsa_ecdhe"] = P(109.171, "ms", "PQC-05", "VERIFIED", "Avg handshake time, client; NUCLEO-F439ZI 180 MHz; Ethernet RTT 0.493 ms", "tasopoulos2022")
L["tls_hs_ms_server_ecdsa_ecdhe"] = P(106.927, "ms", "PQC-05", "VERIFIED", "as above, server", "tasopoulos2022")
L["tls_hs_ms_client_dil3_kyb3"] = P(157.126, "ms", "PQC-05", "VERIFIED", "as above", "tasopoulos2022")
L["tls_hs_ms_server_dil3_kyb3"] = P(153.492, "ms", "PQC-05", "VERIFIED", "as above", "tasopoulos2022")
L["tls_hs_ms_client_dil2_kyb1"] = P(96.318, "ms", "PQC-05", "VERIFIED", "as above", "tasopoulos2022")
L["tls_hs_mJ_client_mut_dil3_kyb3"] = P(25.392, "mJ", "PQC-05", "VERIFIED", "energy per handshake, client, mutual auth (CF'23 Table 2)", "tasopoulos2023")
L["tls_hs_mJ_client_mut_ecdsa_ecdhe"] = P(18.242, "mJ", "PQC-05", "VERIFIED", "as above", "tasopoulos2023")
L["tls_hs_mJ_client_uni_dil3_kyb3"] = P(17.569, "mJ", "PQC-05", "VERIFIED", "client, unilateral auth", "tasopoulos2023")
L["tls_hs_mJ_client_uni_ecdsa_ecdhe"] = P(18.533, "mJ", "PQC-05", "VERIFIED", "client, unilateral auth", "tasopoulos2023")
L["tasopoulos_clock_Hz"] = P(180e6, "Hz", "PQC-05", "VERIFIED", "NUCLEO-F439ZI Cortex-M4", "tasopoulos2022")
L["tasopoulos_bench_rtt_ms"] = P(0.493, "ms", "PQC-05", "VERIFIED", "mean RTT of the wired bench", "tasopoulos2022")

# ------------------------------------------------- pqm4 cycle counts (Cortex-M4 at 24 MHz; AVG)
L["pqm4_clock_Hz"] = P(24e6, "Hz", "PQC-04", "VERIFIED", "README: all cycle counts at 24 MHz", "pqm4")
L["pqm4_mlkem768_keygen_cyc_m4fspeed"] = P(642096, "cycle", "PQC-04", "VERIFIED", "ml-kem-768 m4fspeed AVG", "pqm4")
L["pqm4_mlkem768_encaps_cyc_m4fspeed"] = P(658754, "cycle", "PQC-04", "VERIFIED", "ml-kem-768 m4fspeed AVG", "pqm4")
L["pqm4_mlkem768_decaps_cyc_m4fspeed"] = P(707827, "cycle", "PQC-04", "VERIFIED", "ml-kem-768 m4fspeed AVG", "pqm4")
L["pqm4_mlkem768_keygen_cyc_clean"] = P(988722, "cycle", "PQC-04", "VERIFIED", "ml-kem-768 clean (PQClean reference) AVG", "pqm4")
L["pqm4_mlkem768_encaps_cyc_clean"] = P(1138225, "cycle", "PQC-04", "VERIFIED", "clean AVG", "pqm4")
L["pqm4_mlkem768_decaps_cyc_clean"] = P(1387984, "cycle", "PQC-04", "VERIFIED", "clean AVG", "pqm4")
L["pqm4_mldsa65_keygen_cyc_m4f"] = P(2516006, "cycle", "PQC-04", "VERIFIED", "ml-dsa-65 m4f AVG", "pqm4")
L["pqm4_mldsa65_sign_cyc_m4f"] = P(6193171, "cycle", "PQC-04", "VERIFIED", "ml-dsa-65 m4f AVG (MIN 2,918,295; MAX 26,008,621 -- rejection sampling)", "pqm4")
L["pqm4_mldsa65_verify_cyc_m4f"] = P(2415944, "cycle", "PQC-04", "VERIFIED", "ml-dsa-65 m4f AVG", "pqm4")
L["pqm4_falcon512_keygen_cyc_m4ct"] = P(146357328, "cycle", "PQC-04f", "VERIFIED", "falcon-512 m4-ct AVG (pqm4 @9443518, last version with Falcon)", "pqm4-falcon")
L["pqm4_falcon512_sign_cyc_m4ct"] = P(40191597, "cycle", "PQC-04f", "VERIFIED", "falcon-512 m4-ct sign AVG", "pqm4-falcon")
L["pqm4_falcon512_verify_cyc_m4ct"] = P(482280, "cycle", "PQC-04f", "VERIFIED", "falcon-512 m4-ct verify AVG", "pqm4-falcon")
L["pqm4_falcon512_stack_sign_B_m4ct"] = P(2428, "byte", "PQC-04f", "VERIFIED", "falcon-512 m4-ct sign stack", "pqm4-falcon")
L["pqm4_falcon512_bss_B_m4ct"] = P(39936, "byte", "PQC-04f", "VERIFIED", "falcon-512 m4-ct .bss (static RAM)", "pqm4-falcon")
L["pqm4_falcon512_stack_verify_B_m4ct"] = P(376, "byte", "PQC-04f", "VERIFIED", "falcon-512 m4-ct verify stack", "pqm4-falcon")
L["pqm4_mlkem768_stack_decaps_B_m4fstack"] = P(2844, "byte", "PQC-04", "VERIFIED", "ml-kem-768 m4fstack decapsulation stack", "pqm4")
L["pqm4_mldsa65_stack_verify_B_m4f"] = P(9888, "byte", "PQC-04", "VERIFIED", "ml-dsa-65 m4f verify stack", "pqm4")
L["pqm4_mldsa65_stack_sign_B_m4f"] = P(68872, "byte", "PQC-04", "VERIFIED", "ml-dsa-65 m4f sign stack", "pqm4")

# ------------------------------------------------- link-layer parameters
L["ieee802154_rate_bps"] = P(250e3, "bit/s", "LNK-01", "SECONDARY", "2.4 GHz PHY per RFC 4919 §2 (restating IEEE 802.15.4)", "rfc4919")
L["ieee802154_phy_max_B"] = P(127, "byte", "LNK-01", "SECONDARY", "aMaxPHYPacketSize per RFC 4944 §4", "rfc4944")
L["ieee802154_mac_max_B"] = P(102, "byte", "LNK-01", "SECONDARY", "max MAC frame with 25-octet overhead, RFC 4944 §4", "rfc4944")
L["ieee802154_payload_ccm128_B"] = P(81, "byte", "LNK-02", "VERIFIED", "octets left with AES-CCM-128 link security, RFC 4944 §4", "rfc4944")
L["ipv6_min_mtu_B"] = P(1280, "byte", "LNK-02", "VERIFIED", "RFC 8200 §5", "rfc8200")
L["ble_le1m_protocol_bps"] = P(1e6, "bit/s", "LNK-03", "SECONDARY", "LE 1M PHY protocol data rate (Bluetooth LE Primer §6.3)", "ble-sig")
L["ble_le1m_app_bps_approx"] = P(800e3, "bit/s", "LNK-03", "SECONDARY", "Primer: 'Approximate Max. Application Data Rate' LE 1M", "ble-sig")
L["ble_le2m_protocol_bps"] = P(2e6, "bit/s", "LNK-03", "SECONDARY", "LE 2M PHY (Core 5.0, optional)", "ble-sig")
L["ble_le2m_app_bps_approx"] = P(1400e3, "bit/s", "LNK-03", "SECONDARY", "Primer approximate max application rate LE 2M", "ble-sig")
L["ble_ll_payload_B"] = P(251, "byte", "LNK-03", "SECONDARY", "LL data PDU payload, Core 4.2+ (Data Length Extension)", "ble-sig")
L["ble_ll_payload_legacy_B"] = P(27, "byte", "LNK-03", "SECONDARY", "Core 4.0/4.1", "ble-sig")
L["nbiot_peak_dl_bps"] = P(26e3, "bit/s", "LNK-04", "SECONDARY", "GSMA 2019, NB-IoT (Cat-NB1) peak DL", "gsma-nbiot")
L["nbiot_peak_ul_bps"] = P(66e3, "bit/s", "LNK-04", "SECONDARY", "GSMA 2019, NB-IoT peak UL (multi-tone)", "gsma-nbiot")
L["ltem_hd_dl_bps"] = P(300e3, "bit/s", "LNK-04", "SECONDARY", "GSMA 2019, LTE-M half duplex 'around 300 kbps' DL", "gsma-nbiot")
L["ltem_hd_ul_bps"] = P(380e3, "bit/s", "LNK-04", "SECONDARY", "GSMA 2019, LTE-M half duplex 'around 380 kbps' UL", "gsma-nbiot")
L["nb1_max_tbs_dl_bit"] = P(680, "bit/TTI", "LNK-04", "VERIFIED", "TS 36.306 Table 4.1C-1 Cat NB1 (Rel-13)", "ts36306")
L["nb1_max_tbs_ul_bit"] = P(1000, "bit/TTI", "LNK-04", "VERIFIED", "TS 36.306 Table 4.1C-2 Cat NB1 (Rel-13)", "ts36306")
L["wban_nb_rate_min_bps"] = P(75.9e3, "bit/s", "LNK-05", "SECONDARY", "IEEE 802.15.6-2012 narrowband PHY, across seven bands (Culjak 2020)", "ieee802156")
L["wban_nb_rate_max_bps"] = P(971.4e3, "bit/s", "LNK-05", "SECONDARY", "as above", "ieee802156")
L["wban_frame_body_max_B"] = P(255, "byte", "LNK-05", "SECONDARY", "max MAC frame body (Ullah 2013)", "ieee802156")
L["wban_2026_scope_rate_bps"] = P(50e6, "bit/s", "LNK-05", "VERIFIED", "IEEE 802.15.6-2026 scope: 'data rates up to 50 Mbps'", "ieee802156")

# measured 5G application-layer capacities and RTTs (clinical deployments)
L["ul_5g_ye2026_bps"] = P(101e6, "bit/s", "MED-09d", "VERIFIED", "Beijing 5G CPE side upstream, measured during telesurgery", "ye2026")
L["dl_5g_ye2026_bps"] = P(177e6, "bit/s", "MED-09d", "VERIFIED", "Beijing 5G side downstream", "ye2026")
L["ul_5gsa_chen2024_avg_bps"] = P(91e6, "bit/s", "STR-06b", "VERIFIED", "private 5G SA hospital network, average upload", "chen2024jmir")
L["dl_5gsa_chen2024_avg_bps"] = P(790e6, "bit/s", "STR-06b", "VERIFIED", "average download", "chen2024jmir")
L["ul_5g_moustris2023_bps_lo"] = P(60e6, "bit/s", "STR-06", "VERIFIED", "portable 5G at surgeon site, speed test UL 60-70 Mbps", "moustris2023")
L["rtt_5g_berlet2022_ms"] = P(10, "ms", "STR-07", "VERIFIED", "E2E RTT incl. RAN and core, ambulance parked, core slicing", "berlet2022")
L["rtt_5g_berlet2022_noslice_ms"] = P(400, "ms", "STR-07", "VERIFIED", "latency rose 'up to 400 ms' without core slicing under added uplink load", "berlet2022")
L["rtt_5g_moustris2023_ms"] = P(18, "ms", "STR-06", "VERIFIED", "controllers-to-robot-and-back ping, ~300 km, 5G at one end", "moustris2023")
L["latency_5g_tian2020_ms"] = P(28, "ms", "MED-09a", "VERIFIED", "mean network latency, 12 clinical telerobotic cases, operator-reported; one-way/RTT unstated", "tian2020")
L["latency_5g_ye2026_ms"] = P(220, "ms", "MED-09b", "VERIFIED", "console-to-patient-cart, 5G + wired, ~700 km", "ye2026")

# ------------------------------------------------- mobility
L["ho_dist_nsa5g_freeway_km"] = P(0.4, "km", "MOB-02a", "VERIFIED", "NSA 5G HO every 0.4 km on average, freeway drive tests, US commercial networks", "hassan2022")
L["ho_dist_4g_freeway_km"] = P(0.6, "km", "MOB-02a", "VERIFIED", "4G HO every 0.6 km", "hassan2022")
L["ho_dist_sa5g_km"] = P(0.9, "km", "MOB-02b", "VERIFIED", "SA 5G HO every 0.9 km", "hassan2022")
L["ho_dist_nsa_mmwave_km"] = P(0.13, "km", "MOB-02c", "VERIFIED", "NSA mmWave", "hassan2022")
L["ho_dist_nsa_midband_km"] = P(0.35, "km", "MOB-02c", "VERIFIED", "NSA mid-band", "hassan2022")
L["ho_dist_nsa_lowband_km"] = P(0.4, "km", "MOB-02c", "VERIFIED", "NSA low-band", "hassan2022")
L["ho_per_hour_130kmh"] = P(553, "HO/h", "MOB-02d", "VERIFIED", "'a smartphone traveling at 130 km/h for 1 hour can witness on average 553 5G HOs' (basis not stated)", "hassan2022")
L["ho_speed_for_553_kmh"] = P(130, "km/h", "MOB-02d", "VERIFIED", "as above", "hassan2022")
L["ho_duration_nsa5g_ms"] = P(167, "ms", "MOB-02e", "VERIFIED", "average control-plane HO duration NSA 5G", "hassan2022")
L["ho_duration_sa5g_ms"] = P(110, "ms", "MOB-02e", "VERIFIED", "SA 5G", "hassan2022")
L["ho_duration_lte_ms"] = P(76, "ms", "MOB-02e", "VERIFIED", "4G/LTE", "hassan2022")
L["ho_rate_formula"] = P("H = (4/pi) * v * sqrt(mu)", "1/s", "MOB-01a", "VERIFIED", "PPP base stations of intensity mu (per m^2), nearest-BS association, constant speed v, no pause (Lin et al. Prop. 7 simplification, Eq. 31)", "lin2013")
L["isd_indoor_hotspot_m"] = P(20, "m", "NTN-04a", "VERIFIED", "TR 38.913 Table 6.1.1-1", "tr38913")
L["isd_dense_urban_m"] = P(200, "m", "NTN-04b", "VERIFIED", "TR 38.913 Table 6.1.2-1 macro layer", "tr38913")
L["isd_urban_macro_m"] = P(500, "m", "NTN-04d", "VERIFIED", "TR 38.913 Table 6.1.4-1", "tr38913")
L["isd_rural_m"] = P(1732, "m", "NTN-04c", "VERIFIED", "TR 38.913 Table 6.1.3-1 ISD 1 (ISD 2 = 5000 m)", "tr38913")
L["isd_highway_m"] = P(1732, "m", "NTN-04f", "VERIFIED", "TR 38.913 Table 6.1.8-1 (500 m optional)", "tr38913")
L["ue_speed_urban_car_kmh"] = P(30, "km/h", "NTN-04d", "VERIFIED", "TR 38.913 urban macro: 20% outdoor in cars 30 km/h", "tr38913")
L["ue_speed_rural_vehicle_kmh"] = P(120, "km/h", "NTN-04c", "VERIFIED", "TR 38.913 rural: 50% outdoor vehicles 120 km/h", "tr38913")
L["ue_speed_highway_avg_kmh_lo"] = P(100, "km/h", "NTN-04f", "VERIFIED", "TR 38.913 highway average speed 100-300 km/h", "tr38913")
L["ue_speed_highway_avg_kmh_hi"] = P(300, "km/h", "NTN-04f", "VERIFIED", "as above", "tr38913")
L["ue_speed_hst_max_kmh"] = P(500, "km/h", "NTN-04e", "VERIFIED", "TR 38.913 high-speed train max", "tr38913")
L["mobility_interruption_target_ms"] = P(0, "ms", "MOB-03b", "VERIFIED", "TR 38.913 §7.7 target for mobility interruption time", "tr38913")

# ------------------------------------------------- NTN
L["c_m_per_s"] = P(299792458, "m/s", "NTN-01g", "VERIFIED", "TR 38.821 Table 4.2-2 NOTE 4", "tr38821")
L["ntn_alt_leo1_km"] = P(600, "km", "NTN-01a", "VERIFIED", "TR 38.821 Table 4.2-2", "tr38821")
L["ntn_alt_leo2_km"] = P(1200, "km", "NTN-01a", "VERIFIED", "TR 38.821 Table 4.2-2", "tr38821")
L["ntn_alt_geo_km"] = P(35786, "km", "NTN-01a", "VERIFIED", "TR 38.821 Table 4.2-2", "tr38821")
L["ntn_min_elev_deg"] = P(10, "deg", "NTN-01c", "VERIFIED", "TR 38.821: 10 deg service link and feeder link", "tr38821")
L["ntn_slant_leo600_km"] = P(1932, "km", "NTN-01d", "VERIFIED", "max satellite-UE distance at 10 deg, 600 km", "tr38821")
L["ntn_slant_leo1200_km"] = P(3131, "km", "NTN-01d", "VERIFIED", "1200 km", "tr38821")
L["ntn_slant_geo_km"] = P(40581, "km", "NTN-01d", "VERIFIED", "GEO", "tr38821")
L["ntn_rtd_leo600_transparent_ms"] = P(25.77, "ms", "NTN-01e", "VERIFIED", "max RTD propagation only, service+feeder links, 600 km", "tr38821")
L["ntn_rtd_leo1200_transparent_ms"] = P(41.77, "ms", "NTN-01e", "VERIFIED", "1200 km transparent", "tr38821")
L["ntn_rtd_leo600_regen_ms"] = P(12.89, "ms", "NTN-01e", "VERIFIED", "600 km regenerative (service link only)", "tr38821")
L["ntn_rtd_geo_transparent_ms"] = P(541.46, "ms", "NTN-01e", "VERIFIED", "GEO transparent", "tr38821")
L["ntn_rtd_geo_regen_ms"] = P(270.73, "ms", "NTN-01e", "VERIFIED", "GEO regenerative", "tr38821")
L["ntn_diffdelay_leo600_ms"] = P(3.12, "ms", "NTN-01f", "VERIFIED", "max differential delay within a cell, 600 km", "tr38821")
L["ntn_beam_max_leo_km"] = P(1000, "km", "NTN-01h", "VERIFIED", "max beam footprint edge to edge, LEO", "tr38821")
L["ntn_sat_speed_600km_kms"] = P(7.5622, "km/s", "NTN-01j", "SECONDARY", "TR 38.811 §5.3.4.3 via iTecSpec", "tr38811")
L["ntn_sat_speed_tr38821_kms"] = P(7.56, "km/s", "NTN-01i", "SECONDARY", "TR 38.821 Table 7.3.2.1.4-1 (altitude not stated, NOTE 1)", "tr38821")
L["ntn_oneway_leo600_transparent_ms"] = P(14.204, "ms", "NTN-03k", "SECONDARY", "TR 38.811 Table 5.3.4.1-1, GW 5 deg / UE 10 deg", "tr38811")
L["ntn_oneway_leo600_regen_ms"] = P(6.44, "ms", "NTN-03k", "SECONDARY", "as above, regenerative", "tr38811")
L["ntn_oneway_geo_transparent_ms"] = P(272.375, "ms", "NTN-03j", "VERIFIED", "TR 38.811 Table 5.3.2.1-1 bent pipe one-way", "tr38811")
L["ntn_cell_dwell_50km_s"] = P(6.61, "s", "NTN-05c", "SECONDARY", "TR 38.821 §7.3.2.1.4: max time in a 50 km LEO cell, UE stationary, 7.56 km/s", "tr38821")
L["ntn_cell_dwell_1000km_s"] = P(132.28, "s", "NTN-05c", "SECONDARY", "table value (text says 132.38 -- mismatch flagged)", "tr38821")
L["ntn_ue_speed_leo_kmh"] = P(500, "km/h", "NTN-02a", "VERIFIED", "TR 38.821: 500 km/h (HST), possibly 1200 km/h (aircraft)", "tr38821")
L["ntn_leo_inview_2h_orbit_min"] = P(20, "min", "NTN-05a", "SECONDARY", "TR 38.811 §7.3.2.1.1: 2-hour orbit, horizon to horizon, stationary UE (NOT 600 km / 10 deg)", "tr38811")

# ------------------------------------------------- medical KPIs (normative TS 22.104 first)
L["ras_local_latency_ms"] = P(2, "ms", "MED-04a", "VERIFIED", "TS 22.104 Table 5.2-1 Robotic Aided Surgery local: < 2 ms, one wireless link, one-way", "ts22104")
L["ras_local_rate_lo_bps"] = P(2e6, "bit/s", "MED-04a", "VERIFIED", "2 Mbit/s to 16 Mbit/s", "ts22104")
L["ras_local_rate_hi_bps"] = P(16e6, "bit/s", "MED-04a", "VERIFIED", "as above", "ts22104")
L["ras_local_msg_lo_B"] = P(250, "byte", "MED-04a", "VERIFIED", "message size 250 to 2,000 B", "ts22104")
L["ras_local_msg_hi_B"] = P(2000, "byte", "MED-04a", "VERIFIED", "as above", "ts22104")
L["ras_local_interval_ms"] = P(1, "ms", "MED-04a", "VERIFIED", "transfer interval 1 ms", "ts22104")
L["ras_local_availability"] = P("99.999 999 %", "%", "MED-04a", "VERIFIED", ">99.999 999 %, MTBF > 10 years", "ts22104")
L["ras_remote_latency_ms"] = P(20, "ms", "MED-04b", "VERIFIED", "TS 22.104 RAS remote: < 20 ms, < 400 km", "ts22104")
L["ras_remote_distance_km"] = P(400, "km", "MED-04b", "VERIFIED", "max straight-line distance between UEs", "ts22104")
L["ras_remote_rate_lo_bps"] = P(2e6, "bit/s", "MED-04b", "VERIFIED", "2 Mbit/s to 16 Mbit/s", "ts22104")
L["ras_remote_rate_hi_bps"] = P(16e6, "bit/s", "MED-04b", "VERIFIED", "as above", "ts22104")
L["rad_latency_ms"] = P(20, "ms", "MED-04c", "VERIFIED", "TS 22.104 Robotic Aided Diagnosis: < 20 ms, < 50 km", "ts22104")
L["rad_msg_B"] = P(80, "byte", "MED-04c", "VERIFIED", "message size 80 B", "ts22104")
L["rad_interval_ms"] = P(1, "ms", "MED-04c", "VERIFIED", "transfer interval 1 ms", "ts22104")
L["rad_rate_lo_bps"] = P(2e6, "bit/s", "MED-04c", "VERIFIED", "2-16 Mbit/s", "ts22104")
L["rad_rate_hi_bps"] = P(16e6, "bit/s", "MED-04c", "VERIFIED", "2 Mbit/s to 16 Mbit/s", "ts22104")
# TR 22.826 (SECONDARY)
L["telemetry_inhospital_rate_bps"] = P(0.5e6, "bit/s", "MED-03a", "SECONDARY", "TR 22.826 §5.4.2 cardiac telemetry inside hospital: 0.5 Mbit/s, <100 ms, <=1000 B, <=1000/km2", "tr22826")
L["telemetry_latency_ms"] = P(100, "ms", "MED-03a", "SECONDARY", "< 100 ms", "tr22826")
L["telemetry_msg_max_B"] = P(1000, "byte", "MED-03a", "SECONDARY", "<= 1000 B", "tr22826")
L["telemetry_density_per_km2"] = P(1000, "1/km2", "MED-03a", "SECONDARY", "<= 1000 per km2 (hospital)", "tr22826")
L["telemetry_outside_speed_kmh"] = P(500, "km/h", "MED-03b", "SECONDARY", "TR 22.826 §5.5.3 outside hospital: <= 500 km/h", "tr22826")
L["wearable_battery_V"] = P(3.3, "V", "MED-03c", "SECONDARY", "TR 22.826 §5.5.3 note", "tr22826")
L["wearable_battery_mAh_max"] = P(1000, "mAh", "MED-03c", "SECONDARY", "< 1000 mAh, >= 1 month without recharging", "tr22826")
L["wearable_tx_peak_mA_max"] = P(50, "mA", "MED-03c", "SECONDARY", "peak transmit current below 50 mA", "tr22826")
L["wearable_life_months_min"] = P(1, "month", "MED-03c", "SECONDARY", "at least 1 month", "tr22826")
L["ambulance_4k_rate_bps"] = P(25e6, "bit/s", "MED-03d", "SECONDARY", "TR 22.826 §5.5.2 compressed 4K 60 fps, <100 ms, UE speed 150 (unit not in cell)", "tr22826")
L["ambulance_scan_rate_bps"] = P(670e6, "bit/s", "MED-03e", "SECONDARY", "uncompressed 2048x2048x16-bit 10 fps scan stream", "tr22826")
L["ambulance_vitals_rate_bps"] = P(1e6, "bit/s", "MED-03f", "SECONDARY", "physical vital signs stream, ~80 B messages, <100 ms", "tr22826")
L["ambulance_vitals_msg_B"] = P(80, "byte", "MED-03f", "SECONDARY", "~80 B", "tr22826")
L["ambulance_ecg_payload_B"] = P(10, "byte", "MED-03g", "SECONDARY", "10 B digitised ECG at 200 Hz + 40 B IPv6/20 B IPv4 + 22 B Ethernet + 4 B CRC", "tr22826")
L["ambulance_ecg_rate_Hz"] = P(200, "Hz", "MED-03g", "SECONDARY", "as above", "tr22826")
L["ambulance_audio_rate_bps"] = P(128e3, "bit/s", "MED-03h", "SECONDARY", "~300 B every ~16 ms", "tr22826")
L["teleus_latency_oneway_ms"] = P(20, "ms", "MED-02a", "SECONDARY", "TR 22.826 §5.3.2 tele-ultrasound below 20 ms one-way", "tr22826")
L["teleus_4k_rate_bps"] = P(25e6, "bit/s", "MED-02c", "SECONDARY", "compressed 4K 60 fps, UL", "tr22826")
L["teleus_probe_rate_bps"] = P(160e6, "bit/s", "MED-02d", "SECONDARY", "uncompressed probe stream", "tr22826")
L["surgery_sensor_msg_B"] = P(50, "byte", "MED-01g", "SECONDARY", "TR 22.826 §5.2.4.1.1: sensor return messages 50 B at 1 kHz", "tr22826")
L["surgery_sensor_rate_Hz"] = P(1000, "Hz", "MED-01g", "SECONDARY", "as above", "tr22826")
L["surgery_per_link_latency_ms"] = P(2, "ms", "MED-01h", "SECONDARY", "'roughly 2 ms end-to-end latency constraint on each of the four radio links'", "tr22826")
L["surgery_video_8k_bps"] = P(240e9, "bit/s", "MED-01a", "SECONDARY", "stereoscopic uncompressed 8K 120 fps", "tr22826")
L["surgery_video_4k_lossless_bps"] = P(24e9, "bit/s", "MED-01b", "SECONDARY", "stereoscopic 4K 120 fps lossless (ratio 2.5)", "tr22826")
L["surgery_remote_video_bps"] = P(6e9, "bit/s", "MED-01k", "SECONDARY", "remote telesurgery stereoscopic 4K 60 fps lossless, < 250 ms", "tr22826")
# tactile / 6G
L["tactile_rtt_ms"] = P(1, "ms", "MED-07a", "VERIFIED", "ITU-T 2014: ideal round-trip 1 ms for ~1000 Hz haptics", "itu-tactile-2014")
L["tactile_access_oneway_us"] = P(200, "us", "MED-07c", "VERIFIED", "access-network one-way 200 us share", "itu-tactile-2014")
L["telemed_e2e_lo_ms"] = P(1, "ms", "MED-07d", "VERIFIED", "tele-medical end-to-end 1-10 ms (one-way/RTT unstated)", "itu-tactile-2014")
L["telemed_e2e_hi_ms"] = P(10, "ms", "MED-07d", "VERIFIED", "as above", "itu-tactile-2014")
L["imt2030_ota_latency_lo_ms"] = P(0.1, "ms", "MED-08a", "VERIFIED", "IMT-2030 over-the-air research target 0.1-1 ms", "itu-m2160")
L["imt2030_ota_latency_hi_ms"] = P(1, "ms", "MED-08a", "VERIFIED", "as above", "itu-m2160")
L["imt2030_reliability_lo"] = P("1-10^-5", "prob", "MED-08b", "VERIFIED", "reliability research target 1-10^-5 to 1-10^-7", "itu-m2160")
L["ieee1918_telesurg_haptic_lo_ms"] = P(10, "ms", "MED-06b", "SECONDARY", "Holland et al. 2019: telesurgery-class haptic 10-100 ms", "ieee1918")
L["ieee1918_telesurg_haptic_hi_ms"] = P(100, "ms", "MED-06b", "SECONDARY", "as above", "ieee1918")
L["ts22261_haptic_msg_per_dof_lo_B"] = P(2, "byte", "MED-05d", "SECONDARY", "TS 22.261 Table 7.11-1 remote control robot: 2-8 B (1 DoF), 1-20 ms, 99.999%", "ts22261")
L["ts22261_haptic_msg_per_dof_hi_B"] = P(8, "byte", "MED-05d", "SECONDARY", "as above", "ts22261")

# ------------------------------------------------- clinical streams
L["haptic_rate_Hz"] = P(1000, "Hz", "STR-05", "VERIFIED", "Steinbach 2012: local 1 kHz control loop; packet rate 1 kHz", "steinbach2012")
L["haptic_bits_per_dof"] = P(16, "bit", "STR-05c", "VERIFIED", "Aijaz 2017: 16 bit per DoF", "aijaz2017")
L["haptic_payload_3dof_B"] = P(6, "byte", "STR-05c", "VERIFIED", "Aijaz 2017: 6-byte payload for 3 DoF", "aijaz2017")
L["ipv4_header_B"] = P(20, "byte", "STR-05c", "VERIFIED", "Aijaz 2017", "aijaz2017")
L["ipv6_header_B"] = P(40, "byte", "STR-05c", "VERIFIED", "Aijaz 2017", "aijaz2017")
L["ecg_wban_bps"] = P(3e3, "bit/s", "STR-01", "VERIFIED", "Movassaghi 2014 Table II ECG '3 Kbps' (lead count unstated)", "movassaghi2014")
L["spo2_wban_bps"] = P(32e3, "bit/s", "STR-01", "VERIFIED", "Movassaghi Table II SpO2 32 Kbps", "movassaghi2014")
L["bp_wban_bps"] = P(10, "bit/s", "STR-01", "VERIFIED", "Blood Pressure < 10 bps", "movassaghi2014")
L["capsule_endoscope_bps"] = P(2e6, "bit/s", "STR-01", "VERIFIED", "Endoscope capsule > 2 Mbps", "movassaghi2014")
L["ecg12_bps"] = P(288e3, "bit/s", "STR-01b", "VERIFIED", "Latre 2011 Table 1: ECG 12 leads 288 kbps, 12 bits", "latre2011")
L["ecg6_bps"] = P(71e3, "bit/s", "STR-01b", "VERIFIED", "ECG 6 leads 71 kbps", "latre2011")
L["emg_bps"] = P(320e3, "bit/s", "STR-01b", "VERIFIED", "EMG 320 kbps, 16 bits", "latre2011")
L["eeg12_bps"] = P(43.2e3, "bit/s", "STR-01b", "VERIFIED", "EEG 12 leads 43.2 kbps, 12 bits", "latre2011")
L["glucose_bps"] = P(1600, "bit/s", "STR-01b", "VERIFIED", "Glucose monitoring 1600 bps", "latre2011")
L["temperature_bps"] = P(120, "bit/s", "STR-01b", "VERIFIED", "Temperature 120 bps", "latre2011")
L["eeg_min_samples_per_s"] = P(256, "S/s", "STR-02b", "VERIFIED", "ACNS Guideline 4: minimum 256 samples/s (512 Hz preferable)", "acns-g4")
L["eeg_pref_samples_per_s"] = P(512, "S/s", "STR-02b", "VERIFIED", "as above", "acns-g4")
L["eeg_min_bits"] = P(16, "bit", "STR-02b", "VERIFIED", "at least 16 bits per sample; 24-bit typical", "acns-g4")
L["eeg_typical_bits"] = P(24, "bit", "STR-02b", "VERIFIED", "as above", "acns-g4")
L["eeg_min_channels"] = P(16, "ch", "STR-02", "VERIFIED", "ACNS Guideline 1: 16 channels minimum; 21 electrodes", "acns-g1")
L["ceeg_typical_channels"] = P(32, "ch", "STR-08", "VERIFIED", "Herman 2015 Part II: typical equipment 32 or more channels plus video", "herman2015")
L["ceeg_min_hours"] = P(24, "h", "STR-08b", "VERIFIED", "Herman 2015 Part I: at least 24 h for most indications", "herman2015")
L["ceeg_storage_GB_per_day_video_eeg"] = P(12, "GB/day", "STR-08", "VERIFIED", "Herman 2015 Part II example: 12 GB/day (video + EEG) per machine ('+' glyph unverified)", "herman2015")
L["ecg_diag_samples_per_s"] = P(500, "S/s", "STR-03", "VERIFIED", "Kligfield 2007: 500 samples/s needed for 150 Hz cutoff (adults)", "kligfield2007")
L["ecg_diag_kB_per_10s_lead"] = P(10, "kB", "STR-03", "VERIFIED", "~10 kB per 10 s of one lead at 500 S/s", "kligfield2007")
L["icu_mimic3_channels"] = P(8, "ch", "STR-04", "VERIFIED", "MIMIC-III waveforms: up to eight simultaneous signals", "mimic3wdb")
L["icu_mimic3_rate_Hz"] = P(125, "Hz", "STR-04", "VERIFIED", "digitised at 125 Hz (stored rate)", "mimic3wdb")
L["icu_mimic3_bits_lo"] = P(8, "bit", "STR-04", "VERIFIED", "8-, 10-, or (occasionally) 12-bit", "mimic3wdb")
L["icu_mimic3_bits_hi"] = P(12, "bit", "STR-04", "VERIFIED", "as above", "mimic3wdb")
L["or_vitaldb_rate_lo_Hz"] = P(62.5, "Hz", "STR-04c", "VERIFIED", "VitalDB waveform tracks 62.5-500 Hz, up to 12 tracks", "vitaldb")
L["or_vitaldb_rate_hi_Hz"] = P(500, "Hz", "STR-04c", "VERIFIED", "as above", "vitaldb")
L["surg_video_1080p_bps_lo"] = P(1.5e6, "bit/s", "STR-06", "VERIFIED", "Moustris 2023: 1080p25 H264 VBR 1.5-2 Mbps (configured; phantoms)", "moustris2023")
L["surg_video_1080p_bps_hi"] = P(2e6, "bit/s", "STR-06", "VERIFIED", "as above", "moustris2023")
L["clinical_4k_video_need_bps"] = P(36e6, "bit/s", "STR-06b", "VERIFIED", "Chen 2024 Table 3: 4K video 'Basic needs' 36 Mbps (ward rounds, not surgery)", "chen2024jmir")
L["surg_video_measured_ye2026_bps"] = P(40e6, "bit/s", "MED-09c", "VERIFIED", "Ye 2026: real-time video 40 Mbps during telesurgery", "ye2026")
L["ambulance_video_measured_bps"] = P(12e6, "bit/s", "STR-07", "VERIFIED", "Berlet 2022: measured video stream 12 Mbps (parked ambulance, 5G)", "berlet2022")
L["ambulance_ultrasound_measured_bps"] = P(4e6, "bit/s", "STR-07", "VERIFIED", "measured ultrasound ~4 Mbps", "berlet2022")
L["remote_ultrasound_ul_avg_bps"] = P(2e6, "bit/s", "STR-06b", "VERIFIED", "Chen 2024: remote ultrasound average uplink 2 Mbps", "chen2024jmir")



# ------------------------------------------------- deployment / policy status
L["pq_tls_share_dec2025"] = P(52, "%", "SEC-07a", "VERIFIED", "Cloudflare: PQ-encrypted share of human web traffic, early Dec 2025 (29% at start of 2025)", "cloudflare")
L["pq_tls_share_apr2026"] = P(65, "%", "SEC-07c", "VERIFIED", "'over 65%' (blog 7 Apr 2026)", "cloudflare")
L["tr33703_release"] = P("Rel-20", "-", "SEC-04a", "VERIFIED", "TR 33.703 PQC transition study, V20.0.1 2026-07, 'Under change control'", "tr33703")
L["rel20_freeze"] = P("mid-2027", "-", "SEC-04f", "VERIFIED", "3GPP article June 2026: Rel-20 frozen by mid-2027; Rel-21 not before early 2029", "tr33703")
L["suci_profile_a"] = P("Curve25519 / X25519", "-", "SEC-02a", "SECONDARY", "TS 33.501 Annex C.3.4.1", "ts33501")
L["suci_profile_b"] = P("secp256r1", "-", "SEC-02b", "SECONDARY", "TS 33.501 Annex C.3.4.2", "ts33501")
L["nr_as_algorithms"] = P("128-NEA1/2/3, 128-NIA1/2/3", "-", "SEC-03a", "SECONDARY", "TS 33.501 §5.11.1; no 256-bit identifier listed", "ts33501")
L["snow5g_256_spec"] = P("TS 35.240 V18.0.0 (2024-05) / V19.0.0 (2026-03)", "-", "SEC-03d", "VERIFIED", "256-NEA4/NIA4/NCA4 published; integration into AS/NAS still a Rel-20 6G study (TR 33.771)", "ts35240")
L["ble_pairing_curve"] = P("P-256 ECDH (LE Secure Connections, Core 4.2)", "-", "LNK-03", "SECONDARY", "NIST SP 800-121r2", "ble-sig")
L["wban_assoc_curve"] = P("P-256 ECDH (IEEE 802.15.6-2012 security association)", "-", "LNK-05", "SECONDARY", "Toorani 2015 / Ullah 2013", "ieee802156")
L["ikev2_dh_group_shall"] = P("group 19 (256-bit random ECP)", "-", "SEC-08f", "VERIFIED", "TS 33.210 V19.3.0 §5.4.2", "ts33210")
L["nist_ec_disallowed_after_year"] = P(2035, "year", "SEC-09a", "VERIFIED", "NIST IR 8547 ipd Table 4: Elliptic Curve DH and MQV, >= 128 bits of security strength, 'Disallowed after 2035'; Table 3: ECDSA, >= 128 bits, 'Disallowed after 2035'", "nistir8547")
L["ecdsa_p256_sig_B"] = P(64, "byte", "SEC-09b", "VERIFIED", "RFC 7518 Sec. 3.4: 'The resulting 64-octet sequence is the JWS Signature value.' (ECDSA P-256 SHA-256, R and S 32 octets each; TLS carries it DER-encoded)", "rfc7518")
L["n32_tls_kex"] = P("ECDHE or DHE", "-", "SEC-05b", "VERIFIED", "GSMA PQ.05 p.17: N32 TLS 1.2/1.3 'relies on either ECDHE or DHE'", "gsma-pq05")

out = {"meta": {"built": datetime.date.today().isoformat(),
                "access_date_of_sources": "2026-09-27 (SEC-06f, SEC-09: 2026-10-18)",
                "rule": "Every value copied verbatim from sources/*.md; ids refer to entries there; no arithmetic in this file.",
                "status_tags": "VERIFIED = quoted from primary; SECONDARY = via mirror/secondary (check by hand before submission)"},
       "cites": CITES, "params": L}
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, "..", "sources", "ledger.json")
with open(dst, "w") as f:
    json.dump(out, f, indent=1)
print(f"wrote {os.path.normpath(dst)}: {len(L)} parameters, {len(CITES)} citations")
