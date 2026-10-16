# mobility-5g-security.md — handover models and measurements, TS 33.501, PQC study status, hybrid TLS

Cluster file for the source ledger (see `README.md`). All entries were
collected on **2026-09-27** using WebSearch/WebFetch only. Quotes are copied from the
fetched text and each is 60 words or fewer. `…` marks text omitted from a longer sentence
or list. Maths is reproduced as the fetch tool returned it (plain text/Unicode). There is
no arithmetic in this file.

Sub-ids (`MOB-02a`, `MOB-02b`, …) keep one quote per entry. The parent id is the one
named in the collection brief.

## Status summary

| id | status | headline |
|---|---|---|
| MOB-01 | VERIFIED (arXiv v2) | H = (4/π)ν√μ (μ = BS intensity, ν = speed; no pause, constant velocity) |
| MOB-02 | VERIFIED (NSF-PAR author copy) | NSA 5G HO every 0.4 km (freeway); SA every 0.9 km; mmWave every 0.13 km; 553 5G HOs in 1 hour at 130 km/h; HO duration 167 ms (NSA) / 110 ms (SA) / 76 ms (LTE) |
| MOB-03 | NOT-FOUND (TR 36.839) | supplementary MOB-03b/c from TR 38.913 V19.0.0: interruption target 0ms, mobility target 500km/h |
| SEC-01 | SECONDARY (itecspec mirror of TS 33.501) | KNG-RAN* from the active KgNB (horizontal) or NH (vertical); target AMF re-derives NAS keys from the existing KAMF |
| SEC-02 | SECONDARY (itecspec mirror) | Profile A: Curve25519 / X25519, point compression N/A; Profile B: secp256r1 / Elliptic Curve Cofactor Diffie-Hellman Primitive, point compression true |
| SEC-03 | 33.501 lists SECONDARY; 256-bit status VERIFIED | 128-NEA1/2/3 and 128-NIA1/2/3 only; TS 35.240 V18.0.0 (2024-05, "Release 18") and V19.0.0 (2026-03, "Release 19"); TS 35.243/35.246 ETSI directories 18.00.00 (2024-05-24) and 19.00.00 (2026); 3GPP article (June 2026): "as part of 3GPP Release 20"; TR 33.771 AEAD study (Rel-20) |
| SEC-04 | metadata VERIFIED; scope text SECONDARY | TR 33.703 "Study on transitioning to Post Quantum Cryptography (PQC) in 3GPP", Rel-20, "Under change control", V20.0.0 2026-06-25 / V20.0.1 2026-07-03 |
| SEC-05 | VERIFIED | GSMA PQ.01–PQ.07 (Feb 2023 – May 2026); PQ.05: TLS 1.2/1.3 on N32 "relies on either ECDHE or DHE" |
| SEC-06 | VERIFIED | draft-ietf-tls-ecdhe-mlkem-05: "Approved-announcement sent", RFC Editor "In Progress", no RFC number yet; client share 1216 bytes, server share 1120 bytes |
| SEC-07 | VERIFIED | Cloudflare: 29% → 52% (1 Jan – 2 Dec 2025); "over 65%" (blog of 7 Apr 2026) |
| SEC-08 | 33.501 SECONDARY; TS 33.210 VERIFIED | NFs "shall support mutually authenticated TLS"; N2 IPsec/IKEv2 + DTLS; TS 33.210 V19.3.0: DH group 19 shall, secp256r1 shall (TLS 1.2) |

## How the TS 33.501 text was obtained (affects SEC-01, SEC-02, SEC-03a–c, SEC-08a–e)

The primary document is ETSI TS 133 501 V19.7.0 (2026-08), "(3GPP TS 33.501 version 19.7.0
Release 19)". On 2026-09-27 its latest directory was `19.07.00_60`, dated 8/21/2026. It was
fetched from
`https://www.etsi.org/deliver/etsi_ts/133500_133599/133501/19.07.00_60/ts_133501v190700p.pdf`.
The fetch tool truncated the text inside the table of contents, so no body clause was
visible. An early fetch returned "quotes" for clause 6.9, and the tool then confirmed they
were not in the text it had received, so they were discarded. The clause text below comes
from the third-party rendering at itecspec.com. Its pages are labelled "Rel-20", and the
exact version number was not shown. SEC-01 sentences were spot-checked against
tech-invite.com (V18.6.0). These entries are therefore `SECONDARY`. **Before submission,
check each quoted clause by hand against the ETSI PDF.**

## Fetch log (pages that could NOT be read; none of their content is used)

- ETSI TS 133 501 V19.7.0 PDF (URL above): truncated inside the table of contents (see above).
- `https://api.crossref.org/works?query.bibliographic=Towards+Understanding+...`: the proxy returned HTTP 429 (rate limited) and said not to retry. It was not retried, so the MOB-01 volume and pages are unverified.
- `https://ieeexplore.ieee.org/document/6477064/`: the page came back empty. `https://publications.iitm.ac.in/publication/towards-understanding-the-fundamentals-of-mobility-in-cellular`: showed only the abstract, with no bibliographic fields.
- `https://arxiv.org/abs/1204.3447` and `/abs/1204.3447v2`: the metadata fields (journal-ref, DOI, submission history) were not visible to the tool. `https://export.arxiv.org/abs/1204.3447` and `https://dblp.org/search?...` are blocked by robots.txt.
- `https://www.etsi.org/deliver/etsi_tr/136800_136899/136839/`: 404. `https://itecspec.com/3gpp/36.839`: 404. `https://itecspec.com/archive/3gpp-specification-tr-36-839/`: listed versions and zip links only. The 3GPP FTP serves TR 36.839 only as zip files, which WebFetch cannot open.
- `https://www.etsi.org/deliver/etsi_tr/133800_133899/133841/` and `.../133700_133799/133703/`: 404 (ETSI does not publish TR 33.841 or TR 33.703).
- `https://itecspec.com/3gpp/33.501/s/C.3.4` and `/s/C.3` (uppercase): 404. The lowercase URLs worked.
- `https://whatthespec.net/friendlyspec/spec/33.501/19.7.0`: truncated before clause 6.9 and Annex C.
- `https://www.gsma.com/solutions-and-impact/technologies/security/gsma_resources/post-quantum-telco-network-impact-assessment-whitepaper-pq-01/` and `.../post-quantum-cryptography-guidelines-for-telecom-use-cases-pq-03-2/`: HTTP 403.
- GSMA "Post-Quantum Cryptography Documents" page: the download-link targets (hrefs) were not visible to the tool. No full-text PDF URL was found for PQ.01, PQ.03 (full document) or PQ.06.
- The IETF liaison attachment "Post Quantum Cryptography Guidelines for Telecom Use - TG Approval DRAFT & CONFIDENTIAL" was deliberately **not** fetched or used.
- `https://www.rfc-editor.org/rfc/rfc8446.html`: truncated at §4.2.3, before §9.1 (mandatory-to-implement groups). `https://queue.rfc-editor.org/`: the queue table is rendered by JavaScript, so no rows were visible.
- `https://radar.cloudflare.com/post-quantum`: the chart values are rendered by JavaScript. Only the chart title and description were visible.

---

## MOB-01 — Lin, Ganti, Fleming, Andrews: handover rate in Poisson-Voronoi networks

### MOB-01a
- **Citation:** X. Lin, R. K. Ganti, P. J. Fleming, J. G. Andrews, "Towards Understanding the Fundamentals of Mobility in Cellular Networks," IEEE Trans. Wireless Commun., 2013 (IEEE Xplore document 6477064, from the search-result URL; page not readable). arXiv:1204.3447v2 (the PDF header reads "Date revised: January 17, 2013"). Volume, issue and pages: memory suggests vol. 12, no. 4, pp. 1686–1698 — UNVERIFIED.
- **Fetched URL:** https://arxiv.org/pdf/1204.3447v2 (cross-checked with https://arxiv.org/html/1204.3447v2)
- **Location:** Sec. V "Applications to Poisson-Voronoi modeled cellular networks", subsection A "Handover Rate", text after Proposition 7, Eq. (31); p. 8 of the arXiv v2 PDF.
- **Quote:** "If we assume no pause time and constant velocity ν, H in Prop. 7 can be simplified as H = (4/π)ν√μ, which is consistent with the one given in [37]."
- **Figure(s):** H = (4/π)ν√μ (handover rate, handovers per unit time)
- **Condition:** Analytical, not measured. BSs form a homogeneous PPP of intensity **μ**, and users associate with the nearest BS (Poisson-Voronoi cells). Users follow the modified random-waypoint model. **No pause time; constant velocity ν.** Notation: the paper uses **μ for BS density** and **λ for the mobility (waypoint-PPP) parameter**. The brief's "λ" for BS density is therefore the paper's μ.
- **Use in paper:** Mobility budget. Handover rate as a function of speed and cell density sets how many AS key refreshes (KNG-RAN* derivations, SEC-01) occur per hour.
- **Status:** VERIFIED (arXiv version of the peer-reviewed paper).

### MOB-01b
- **Citation / Fetched URL:** as MOB-01a (https://arxiv.org/pdf/1204.3447v2)
- **Location:** Proposition 7, Sec. V-A, p. 8 (arXiv v2 PDF)
- **Quote:** "Let μ be the intensity of the homogeneously PPP distributed BSs and λ the mobility parameter. The expected number of handovers E[N] during one movement period is given by E[N] = (2/π)√(μ/λ). The handover rate H = E[N]/E[T_p] is then given by H = 1/(E[T] + E[S]) · (2/π)√(μ/λ)."
- **Figure(s):** E[N] = (2/π)√(μ/λ); H = 1/(E[T] + E[S]) · (2/π)√(μ/λ)
- **Condition:** Analytical. General form, with mean transition time E[T] and mean pause time E[S] per movement period.
- **Use in paper:** Lets the model include pauses (e.g., ambulance stops, walking patient) instead of assuming constant speed.
- **Status:** VERIFIED

### MOB-01c
- **Citation / Fetched URL:** as MOB-01a (https://arxiv.org/pdf/1204.3447v2)
- **Location:** Sec. II "Proposed RWP mobility model on infinite planes"
- **Quote:** "Given the waypoint X_{n-1}, a homogeneous PPP Φ(n) with intensity λ is independently generated and then the nearest point in Φ(n) is selected as the next waypoint, i.e., X_n = arg min_{x ∈ Φ(n)} ||x - X_{n-1}||. … Velocities V_n are i.i.d. with distribution P_V(·). Pause times S_n are also i.i.d. with distribution P_S(·)."
- **Figure(s):** — (model assumptions)
- **Condition:** Mobility-model assumptions behind MOB-01a/b. The arXiv HTML rendering also gives the transition-length CDF "P(L < l) = 1 - exp(-λ π l²), l > 0" (Rayleigh). That formula is from the HTML fetch only.
- **Use in paper:** States the assumptions whenever MOB-01a is used.
- **Status:** VERIFIED

### MOB-01d
- **Citation / Fetched URL:** as MOB-01a (https://arxiv.org/pdf/1204.3447v2)
- **Location:** Abstract
- **Quote:** "We present analytic expressions for both handover rate and sojourn time, which have the expected property that the handover rate is proportional to the square root of BS density."
- **Figure(s):** handover rate ∝ √(BS density) (qualitative)
- **Condition:** Analytical, PPP BSs.
- **Use in paper:** One-line justification of the √density scaling.
- **Status:** VERIFIED

---

## MOB-02 — Hassan et al., "Vivisecting Mobility Management in 5G Cellular Networks," ACM SIGCOMM 2022

Common fields for MOB-02a–g:
- **Citation:** A. Hassan, A. Narayanan, A. Zhang, W. Ye, R. Zhu, S. Jin, J. Carpenter, Z. M. Mao, F. Qian, Z.-L. Zhang, "Vivisecting Mobility Management in 5G Cellular Networks," Proc. ACM SIGCOMM '22, Amsterdam, Netherlands, 22–26 Aug 2022. DOI 10.1145/3544216.3544217 (from the ACM DL URL in the search results; the ACM page was not fetched).
- **Fetched URL:** https://par.nsf.gov/servlets/purl/10355260 (NSF Public Access Repository copy of the paper; the author list and "SIGCOMM '22, August 22–26, 2022, Amsterdam, Netherlands" are printed on p. 1)
- **Condition (all):** Deployed commercial networks of three major U.S. carriers (anonymised OpX, OpY, OpZ), with NSA and SA 5G across low-band, mid-band and mmWave. The test phones were Samsung Galaxy S21 Ultra and S20 Ultra ("A total of four mobile phones (three S21U and one S20U) are used in our study"). The authors report "a total travel distance of 6,200 km+". **The dates of data collection are not stated** in the text seen.

### MOB-02a
- **Location:** §5.1 (Handover Frequency)
- **Quote:** "Specifically, in our freeway drive tests (Table 1), NSA 5G HOs are triggered every 0.4 km on average, in contrast to every 0.6 km for 4G HOs."
- **Figure(s):** NSA 5G HOs "every 0.4 km on average"; 4G HOs "every 0.6 km"
- **Condition:** Freeway drive tests, measured. The sentence does not state the vehicle speed. It gives one NSA 5G average with no band breakdown; per-band values are in MOB-02c.
- **Use in paper:** Measured HO density at driving speed, to set against the analytical MOB-01.
- **Status:** VERIFIED

### MOB-02b
- **Location:** §5.1
- **Quote:** "On the other hand, SA 5G experiences an HO every 0.9 km."
- **Figure(s):** SA 5G "an HO every 0.9 km"
- **Condition:** Drive tests, SA 5G (commercial U.S. network), measured.
- **Use in paper:** SA vs NSA contrast.
- **Status:** VERIFIED

### MOB-02c
- **Location:** §5.1
- **Quote:** "For different bands within NSA, mmWave 5G sees a HO every 0.13 km, mid-band every 0.35 km, and low-band every 0.4 km."
- **Figure(s):** mmWave "a HO every 0.13 km"; mid-band "every 0.35 km"; low-band "every 0.4 km"
- **Condition:** NSA 5G, by band, measured.
- **Use in paper:** Worst case for a dense or mmWave deployment.
- **Status:** VERIFIED

### MOB-02d
- **Location:** §5.3 (heading reported by the tool as "Handover Energy Consumption")
- **Quote:** "We find that a smartphone traveling at 130 km/h for 1 hour can witness on average 553 5G HOs. This will result in ∼34.7 mAh energy drain."
- **Figure(s):** "553 5G HOs" in "1 hour" at "130 km/h"; "∼34.7 mAh"
- **Condition:** The authors' figure inside the energy analysis. **The band, carrier and derivation behind this number were not confirmed** in the text I could read. A tool-generated explanation of it was discarded as inference. Use only as quoted.
- **Use in paper:** Time-based handover rate at highway speed (ambulance-transport scenario).
- **Status:** VERIFIED (sentence); basis of the estimate unclear

### MOB-02e
- **Location:** §5.2 (Handover Duration)
- **Quote:** "The average HO duration in NSA 5G is 167 ms, a 119% increase compared to 76 ms for 4G/LTE HOs. … SA 5G HOs, on the other hand, are significantly shorter (110 ms) on average despite its high variation."
- **Figure(s):** NSA 5G 167 ms; LTE 76 ms; SA 5G 110 ms (average HO duration)
- **Condition:** Measured control-plane HO duration = preparation stage T₁ (starts when the "primary cell is notified about a measurement event via MR") + execution stage T₂ ("The HO ends with a successful completion of RACH procedure").
- **Use in paper:** Existing HO time against which to set any added PQ cryptographic latency.
- **Status:** VERIFIED

### MOB-02f
- **Location:** §5.2
- **Quote:** "Additionally, the data plane operations are completely halted, hence the duration spent on T2 is critical to upper-layer application performance and user QoE. The HO ends with a successful completion of RACH procedure. … Due to additional signaling overheads, NSA 5G leads to a higher T₂ that is 1.4-5.4× compared to LTE."
- **Figure(s):** NSA 5G T₂ = 1.4–5.4× LTE (relative)
- **Condition:** T₂ is the execution stage, during which the data plane is halted (per the paper). Measured.
- **Use in paper:** Defines the user-plane interruption window for clinical streams.
- **Status:** VERIFIED

### MOB-02g
- **Location:** §5.2
- **Quote:** "Fig. 8 shows the time consumed by OpY in T₁ stage across their deployments: LTE vs. NSA vs. SA. We clearly notice that NSA 5G takes on average 92 ms (which is almost 48%) more time than LTE."
- **Figure(s):** NSA 5G T₁ = +92 ms vs LTE (≈48%), OpY
- **Condition:** One carrier (OpY), preparation stage T₁, measured.
- **Use in paper:** Optional detail.
- **Status:** VERIFIED

---

## MOB-03 — 3GPP TR 36.839 HOF/RLF vs UE speed

### MOB-03 (requested figure)
- **Citation:** 3GPP TR 36.839, "Evolved Universal Terrestrial Radio Access (E-UTRA); Mobility enhancements in heterogeneous networks" (Rel-11)
- **Fetched URL:** none returned text
- **Location / Quote / Figure(s):** —
- **Condition:** —
- **Use in paper:** HOF/RLF rate vs speed (optional)
- **Status:** NOT-FOUND. Tried: ETSI deliver TR 136 839 (404); itecspec.com /3gpp/36.839 (404) and its archive page (zip links only); WebSearch. The 3GPP FTP has zip files only. TR 38.913 (below) gives no HOF/RLF-versus-speed figures (the tool checked).

### MOB-03b (supplementary: not a HOF/RLF figure)
- **Citation:** ETSI TR 138 913 V19.0.0 (2025-10), "5G; Study on scenarios and requirements for next generation access technologies (3GPP TR 38.913 version 19.0.0 Release 19)" (cover page).
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf
- **Location:** Clause 7.7 "Mobility interruption time"
- **Quote:** "Mobility interruption time means the shortest time duration supported by the system during which a user terminal cannot exchange user plane packets with any base station during transitions. The target for mobility interruption time should be 0ms."
- **Figure(s):** target 0ms
- **Condition:** 3GPP NR design target (requirement), not a measurement. The clause adds: "This KPI is for both intra-frequency and inter-frequency mobility for intra-NR mobility."
- **Use in paper:** Contrast the 0ms requirement with the measured 110–167 ms (MOB-02e).
- **Status:** VERIFIED

### MOB-03c (supplementary)
- **Citation / Fetched URL:** as MOB-03b
- **Location:** Clause 7.18 "Mobility"
- **Quote:** "Mobility means the maximum user speed at which a defined QoS can be achieved (in km/h). The target for mobility target should be 500km/h."
- **Figure(s):** 500km/h
- **Condition:** Design target (requirement); "Evaluation methodology should be link level evaluation with deployment scenario specific operating point."
- **Use in paper:** Upper speed bound for the mobility sweep.
- **Status:** VERIFIED

---

## SEC-01 — TS 33.501 key handling at handover (clause 6.9.2)

Common fields: **Citation:** 3GPP TS 33.501, "Security architecture and procedures for 5G system" (primary: ETSI TS 133 501 V19.7.0 (2026-08), Release 19; text taken from the itecspec.com "Rel-20" rendering). **Condition (all):** NR/5GC, normative text, release as labelled. Clause 6.9.1 is "Void" in the Rel-20 rendering.

### SEC-01a
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.1.1
- **Location:** Clause 6.9.2.1.1 "Access stratum"
- **Quote:** "Whenever an initial AS security context needs to be established between UE and gNB/ng-eNB, AMF and the UE shall derive a KgNB and a Next Hop parameter (NH). The KgNB and the NH are derived from the KAMF."
- **Figure(s):** — (key hierarchy: KAMF → KgNB, NH)
- **Use in paper:** Handover keys are rooted in KAMF, which comes from primary authentication.
- **Status:** SECONDARY (via itecspec.com rendering of TS 33.501 Rel-20; the first sentence was cross-checked on tech-invite.com V18.6.0)

### SEC-01b
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.1.1 (cross-check: https://www.tech-invite.com/3m33/toc/tinv-3gpp-33-501_r.html, V18.6.0)
- **Location:** Clause 6.9.2.1.1
- **Quote:** "On handovers and at transitions from RRC_INACTIVE to RRC_CONNECTED states (defined in clause 6.8.2.1), the basis for the KgNB that will be used between the UE and the target gNB/ng-eNB, called KNG-RAN*, is derived from either the currently active KgNB or from the NH parameter."
- **Figure(s):** —
- **Use in paper:** A new AS key is derived at every handover.
- **Status:** SECONDARY (itecspec Rel-20; same sentence on tech-invite V18.6.0, where the rendering drops "6.8.2.1)")

### SEC-01c
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.1.1
- **Location:** Clause 6.9.2.1.1
- **Quote:** "If KNG-RAN* is derived from the currently active KgNB this is referred to as a horizontal key derivation (see Figure 6.9.2.1.1-1) and if the KNG-RAN* is derived from the NH parameter the derivation is referred to as a vertical key derivation (see Figure 6.9.2.1.1-1)."
- **Figure(s):** horizontal vs vertical key derivation
- **Use in paper:** Names the two derivations.
- **Status:** SECONDARY (itecspec Rel-20; first half cross-checked on tech-invite V18.6.0)

### SEC-01d
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.1.1
- **Location:** Clause 6.9.2.1.1
- **Quote:** "As NH parameters are only computable by the UE and the AMF, it is arranged so that NH parameters are provided to gNB/ng-eNBs from the AMF in such a way that forward security can be achieved."
- **Figure(s):** —
- **Use in paper:** Security property of vertical derivation.
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-01e
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.3.2
- **Location:** Clause 6.9.2.3.2 "Xn-handover"
- **Quote:** "The source gNB/ng-eNB shall first compute KNG-RAN* from target PCI, its frequency ARFCN-DL/EARFCN-DL, and either from currently active KgNB in case of horizontal key derivation or from the NH in case of vertical key derivation as described in Annex A.11/A.12. … The target gNB/ng-eNB shall use the received KNG-RAN* directly as KgNB to be used with the UE."
- **Figure(s):** — (KDF inputs: target PCI, ARFCN-DL/EARFCN-DL, KgNB or NH; Annex A.11/A.12)
- **Use in paper:** Xn handover uses only symmetric KDF operations. This is an inference from the quoted text; check the wording before using it in the paper.
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-01f
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.3.2
- **Location:** Clause 6.9.2.3.2
- **Quote:** "Upon reception of the NGAP PATH SWITCH REQUEST, the AMF shall increase its locally kept NCC value by one and compute a new fresh NH from its stored data using the function defined in Annex A.10."
- **Figure(s):** NCC incremented by one per path switch
- **Use in paper:** Core-side cost per Xn handover (one NH derivation).
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-01g
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.1.2 (cross-check: https://www.tech-invite.com/3m33/toc/tinv-3gpp-33-501_r.html, V18.6.0)
- **Location:** Clause 6.9.2.1.2 "Non access stratum"
- **Quote:** "In this case, the target AMF re-derives the NAS keys from the existing KAMF (if unchanged) or derives the NAS keys from the new KAMF (if changed) using the NAS algorithm identities and NAS algorithm types as input to the NAS key derivation functions (see Annex A.8)."
- **Figure(s):** —
- **Condition:** Applies at AMF change during mobility when the NAS algorithms differ. The KAMF itself may or may not change.
- **Use in paper:** The NAS security context (KAMF) is carried over rather than re-established by authentication.
- **Status:** SECONDARY (itecspec Rel-20; identical sentence without "(see Annex A.8)" on tech-invite V18.6.0)

### SEC-01h
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/6.9.2.1.2
- **Location:** Clause 6.9.2.1.2
- **Quote:** "When the KAMF has not changed, all inputs, in particular the KAMF, will be the same in the re-derivation except for the NAS algorithm identity. When the KAMF has changed, new NAS keys are derived irrespective of change in NAS algorithms."
- **Figure(s):** —
- **Condition:** as SEC-01g. **No sentence was found saying explicitly that primary authentication is not run at handover.** The quotes show handover and mobility reuse or derive keys from the existing KAMF. KAMF change is signalled by indicators (NOTE 2 of 6.9.2.1.2: keyAmfChangeInd, keyAmfHDerivationInd, K_AMF_change_flag, NSCI, keySetChangeIndicator).
- **Use in paper:** Word the claim as "handover re-keys the AS from the existing KAMF-rooted context (TS 33.501 §6.9.2.1.1–6.9.2.1.2)". Do not write "the spec says no authentication at handover".
- **Status:** SECONDARY (itecspec Rel-20)

---

## SEC-02 — TS 33.501 Annex C: SUCI ECIES profiles

Common fields: **Citation:** 3GPP TS 33.501 Annex C.3.4 (primary ETSI TS 133 501 V19.7.0; text from the itecspec.com "Rel-20" rendering). **Condition (all):** normative. In the Rel-20 rendering, C.3.4 has only C.3.4.0 General, C.3.4.1 Profile A and C.3.4.2 Profile B. No post-quantum or KEM profile is listed. **Use in paper:** SUCI concealment is the device-side public-key operation of 5G registration, and it is quantum-vulnerable (see SEC-04c).

### SEC-02a
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/c.3.4.1
- **Location:** Clause C.3.4.1 "Profile A"
- **Quote:** "The ME and SIDF shall implement this profile. The ECIES parameters for this profile shall be the following: - EC domain parameters: Curve25519 [46] - EC Diffie-Hellman primitive: X25519 [46] - point compression: N/A"
- **Figure(s):** Curve25519; X25519; point compression N/A
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-02b
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/c.3.4.2
- **Location:** Clause C.3.4.2 "Profile B"
- **Quote:** "The ME and SIDF shall implement this profile. The ECIES parameters for this profile shall be the following: - EC domain parameters: secp256r1 [30] - EC Diffie-Hellman primitive: Elliptic Curve Cofactor Diffie-Hellman Primitive [29] - point compression: true"
- **Figure(s):** secp256r1; Elliptic Curve Cofactor Diffie-Hellman Primitive; point compression true
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-02c
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/c.3.4.1 (the same lines appear in c.3.4.2)
- **Location:** Clauses C.3.4.1 and C.3.4.2 (identical symmetric parameters)
- **Quote:** "- KDF: ANSI-X9.63-KDF [29] - Hash: SHA-256 … - MAC: HMAC–SHA-256 - mackeylen: 32 octets (256 bits) - maclen: 8 octets (64 bits) - SharedInfo2: the empty string - ENC: AES–128 in CTR mode - enckeylen: 16 octets (128 bits) - icblen: 16 octets (128 bits) - backwards compatibility mode: false"
- **Figure(s):** maclen 8 octets; mackeylen 32 octets; enckeylen 16 octets; icblen 16 octets
- **Condition:** Both profiles.
- **Use in paper:** Symmetric part of SUCI (AES-128-CTR, HMAC-SHA-256 with an 8-octet tag). The tag size enters the SUCI length budget.
- **Status:** SECONDARY (itecspec Rel-20)

---

## SEC-03 — NR ciphering/integrity algorithms and status of 256-bit algorithms

### SEC-03a
- **Citation:** 3GPP TS 33.501, clause 5.11.1.1 "Ciphering algorithm identifier values" (itecspec "Rel-20" rendering)
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/5.11.1.1
- **Location:** Clause 5.11.1.1
- **Quote:** "\"0000₂\" NEA0 Null ciphering algorithm; \"0001₂\" 128-NEA1 128-bit SNOW 3G based algorithm; \"0010₂\" 128-NEA2 128-bit AES based algorithm; \"0011₂\" 128-NEA3 128-bit ZUC based algorithm. … Full details of the algorithms are specified in Annex D."
- **Figure(s):** 4-bit identifiers; 128-NEA1 (SNOW 3G), 128-NEA2 (AES, "128-bit AES in CTR mode"), 128-NEA3 (ZUC)
- **Condition:** The list separators are as rendered by the tool; ₂ marks binary. In this rendering **no 256-bit identifier appears** in 5.11.1.1.
- **Use in paper:** Current NR AS/NAS ciphers are 128-bit.
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-03b
- **Citation:** 3GPP TS 33.501, clause 5.11.1.2 "Integrity algorithm identifier values" (itecspec "Rel-20")
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/5.11.1.2
- **Location:** Clause 5.11.1.2
- **Quote:** "Each integrity algorithm used for 5G will be assigned a 4-bit identifier. … \"0000₂\" NIA0 Null Integrity Protection algorithm; \"0001₂\" 128-NIA1 128-bit SNOW 3G based algorithm; \"0010₂\" 128-NIA2 128-bit AES based algorithm; \"0011₂\" 128-NIA3 128-bit ZUC based algorithm"
- **Figure(s):** 128-NIA1/2/3; 128-NIA2 = "128-bit AES [15] in CMAC mode [17]"
- **Condition:** The tool rendered "0000₂" as "00002" (subscript lost). No 256-bit identifier appears in this rendering.
- **Use in paper:** as SEC-03a
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-03c
- **Citation:** 3GPP TS 33.501 Annex D (itecspec "Rel-20")
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/annex-d and https://itecspec.com/3gpp/33.501/s/d.2
- **Location:** Annex D headings: D.1 Null ciphering and integrity protection algorithms; D.2 Ciphering algorithms (D.2.1 "128-bit Ciphering algorithms": D.2.1.2 128-NEA1, D.2.1.3 128-NEA2, D.2.1.4 128-NEA3); D.3 Integrity algorithms; D.4 Test Data
- **Quote:** "D.2.1 128-bit Ciphering algorithms … D.2.1.2 128-NEA1 … D.2.1.3 128-NEA2 … D.2.1.4 128-NEA3" (headings only)
- **Figure(s):** —
- **Condition:** Headings only; the tool did not return the body text. No 256-bit sub-clause is listed under D.2.
- **Use in paper:** Reference for the algorithm specs.
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-03d
- **Citation:** ETSI TS 135 240 V18.0.0 (2024-05), "5G; Specification of the Snow 5G based 256-bits algorithm set: specification of the 256-NEA4 encryption, the 256-NIA4 integrity, and the 256-NCA4 authenticated encryption algorithm for 5G; Document 1: algorithm specification", "(3GPP TS 35.240 version 18.0.0 Release 18)". Also ETSI TS 135 240 V19.0.0 (2026-03), "(3GPP TS 35.240 version 19.0.0 Release 19)", with the same Scope sentence.
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/135200_135299/135240/18.00.00_60/ts_135240v180000p.pdf (also .../19.00.00_60/ts_135240v190000p.pdf)
- **Location:** Cover page; Clause 1 "Scope"
- **Quote:** "The present document contains the algorithm specification which could be used as the encryption and integrity protection function 256-NEA4, 256-NIA4 and the combined authenticated encryption 256-NCA4 protection function for 3GPP systems."
- **Figure(s):** 256-NEA4 / 256-NIA4 / 256-NCA4 (SNOW 5G based); published 2024-05 (V18.0.0) and 2026-03 (V19.0.0)
- **Condition:** Algorithm specification only ("could be used"). The V19.0.0 text has no rationale sentence about quantum computing (the tool checked).
- **Use in paper:** 256-bit symmetric algorithms exist as published 3GPP specifications.
- **Status:** VERIFIED

### SEC-03e
- **Citation:** 3GPP TS 35.243 (AES based 256-bit set), from the 3GPP 35-series list; ETSI TS 135 243 directories 18.00.00_60 (5/24/2024) and 19.00.00_60 (3/30/2026)
- **Fetched URL:** https://www.3gpp.org/dynareport?code=35-series.htm (directory: https://www.etsi.org/deliver/etsi_ts/135200_135299/135243/)
- **Location:** 35-series spec list, entry TS 35.243
- **Quote:** "Specification of the AES based 256-bits algorithm set: Specification of the 256-NEA5 encryption, the 256-NIA5 integrity, and the 256-NCA5 authenticated encryption algorithm for 5G; Document 1: algorithm specification"
- **Figure(s):** 256-NEA5 / 256-NIA5 / 256-NCA5. Test data are in TS 35.244 and 35.245.
- **Condition:** The dates are ETSI directory timestamps, not cover dates.
- **Use in paper:** as SEC-03d
- **Status:** VERIFIED

### SEC-03f
- **Citation:** 3GPP TS 35.246 (ZUC based 256-bit set); ETSI TS 135 246 directories 18.00.00_60 (5/24/2024) and 19.00.00_60 (1/28/2026)
- **Fetched URL:** https://www.3gpp.org/dynareport?code=35-series.htm (directory: https://www.etsi.org/deliver/etsi_ts/135200_135299/135246/)
- **Location:** 35-series spec list, entry TS 35.246
- **Quote:** "Specification of the ZUC based 256-bits algorithm set: Specification of the 256-NEA6 encryption, the 256-NIA6 integrity, and the 256-NCA6 authenticated encryption algorithm for 5G; Document 1: algorithm specification"
- **Figure(s):** 256-NEA6 / 256-NIA6 / 256-NCA6. Test data are in TS 35.247 and 35.248.
- **Condition:** as SEC-03e
- **Use in paper:** as SEC-03d
- **Status:** VERIFIED

### SEC-03g
- **Citation:** S. Orkopoulos (SA WG3 Delegate, Nokia), "Post Quantum Cryptography in 3GPP," 3GPP Highlights Issue 12, published June 2026.
- **Fetched URL:** https://www.3gpp.org/technologies/pqc-sa3
- **Location:** Article body (256-bit algorithms paragraph)
- **Quote:** "To address this, 3GPP SA3 has decided to introduce 256-bit algorithm specifications in TS 35.240 through TS 35.248 as part of 3GPP Release 20, aiming to enhance long-term security resilience: …"
- **Figure(s):** TS 35.240–35.248; "Release 20"
- **Condition:** Official 3GPP web article (dated June 2026). **Release labels disagree:** this article says "Release 20", while the ETSI cover pages say TS 35.240 V18.0.0 is "Release 18" and V19.0.0 is "Release 19" (SEC-03d). Quote both; do not reconcile.
- **Use in paper:** Status statement for 256-bit algorithms.
- **Status:** VERIFIED

### SEC-03h
- **Citation:** 3GPP TR 33.771, "Study on supporting AEAD algorithms" (3GPP portal); described in the 3GPP article of SEC-03g.
- **Fetched URL:** https://www.3gpp.org/technologies/pqc-sa3 and https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4461
- **Location:** Article body; portal specification page
- **Quote:** "Additionally, there is an ongoing 6G Rel-20 study on supporting 256-bit AEAD algorithms for Access Stratum (AS) and Non-Access Stratum (NAS) security, documented in TR 33.771, which examines the integration of those algorithms into the overall security architecture."
- **Figure(s):** Portal: Status "Under change control"; Initial planned Release "Release 20"; versions include 1.0.0 (SA#112), 2.0.0 (SA#113, listed 2026-09-04) and 20.0.0 (no date shown); WI FS_AEAD.
- **Condition:** 6G study. Integrating 256-bit AS/NAS algorithms into the security architecture is still a study item.
- **Use in paper:** "256-bit AS/NAS algorithms are specified but still under study for integration (6G, Rel-20)."
- **Status:** VERIFIED

### SEC-03i
- **Citation:** 3GPP TR 33.841, "Study on the support of 256-bit algorithms for 5G" (portal: Technical report, "Under change control", Initial planned Release 15; versions 16.0.0 of 2018-12-18 and 16.1.0 of 2019-03-28; WI FS_256_Algo)
- **Fetched URL:** https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3422 (metadata); https://www.tech-invite.com/3m33/toc/tinv-3gpp-33-841_a.html (scope text, V16.1.0)
- **Location:** Clause 1 "Scope" (last bullet); Introduction
- **Quote:** "Recommendations for suitable requirements for the needed algorithms for use with 256-bit keys and ask ETSI SAGE to provide those algorithms." / Introduction: "Quantum computing poses a long-term threat to information security."
- **Figure(s):** V16.1.0 (2019-03-28)
- **Condition:** 2018–2019 study (Rel-15/16). Its conclusions clause was not reachable.
- **Use in paper:** Origin of the 256-bit work.
- **Status:** VERIFIED for the portal metadata; SECONDARY (via tech-invite.com rendering of TR 33.841 V16.1.0) for the quoted text

---

## SEC-04 — 3GPP SA3 study on post-quantum cryptography: TR 33.703

### SEC-04a
- **Citation:** 3GPP TR 33.703, "Study on transitioning to Post Quantum Cryptography (PQC) in 3GPP"
- **Fetched URL:** https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4422 (redirected from https://www.3gpp.org/dynareport/33703.htm)
- **Location:** 3GPP portal specification page (General / Versions / Related WI)
- **Quote:** Title "Study on transitioning to Post Quantum Cryptography (PQC) in 3GPP"; Type "Technical report (TR)"; Status "Under change control"; Initial planned Release "Release 20"
- **Figure(s):** Versions: 20.0.0 (SA#112, uploaded 2026-06-25); 20.0.1 (SA#112, uploaded 2026-07-03); 20.1.0 (SA#113, no upload date shown). Earlier drafts 0.0.0/0.1.0 date from 2025-09-30. Related WI: FS_CryptoPQC (UID 1080045), "Study on Transitioning to Post Quantum Cryptography in 3GPP", group S3. The radio technologies ticked are 2G, 3G, LTE, 5G and 6G.
- **Condition:** Status as of 2026-09-27. The study is approved and under change control; it is not a normative specification.
- **Use in paper:** PQC status statement for 3GPP.
- **Status:** VERIFIED

### SEC-04b
- **Citation:** 3GPP TR 33.703 V20.0.1 (2026-07), Release 20
- **Fetched URL:** https://whatthespec.net/friendlyspec/spec/33.703/20.0.1
- **Location:** Clause 1 "Scope" (opening)
- **Quote:** "The present document studies the complexities involved with the introduction of standalone and/or hybrid Post Quantum Cryptography (PQC) algorithms in existing security protocols used by 5G specifications. These security protocols and their associated algorithms have been listed in TR 33.938 \"3GPP Cryptographic Inventory.\""
- **Figure(s):** —
- **Condition:** Scope of the study. The scope ends: "The present document is Generation agnostic."
- **Use in paper:** Quote of the scope paragraph.
- **Status:** SECONDARY (via whatthespec.net rendering of 3GPP TR 33.703 V20.0.1; the 3GPP zip was not readable)

### SEC-04c
- **Citation / Fetched URL:** as SEC-04b
- **Location:** Clause 1 "Scope", bullet 6
- **Quote:** "Identifies the protocols with asymmetric cryptography listed in TR 33.938 that are not expected to be updated by other Standards Development Organizations (SDOs) in a near future to use PQC, e.g. MIKEY-SAKKE and SUCI calculation"
- **Figure(s):** —
- **Condition:** Study scope. The last scope bullet adds: "Studies solutions to update 3GPP defined security protocols (for example SUCI calculation) to use the appropriate PQC algorithm, if those protocols are not expected to be updated by other SDOs to use PQC algorithms."
- **Use in paper:** SUCI (SEC-02) is named as the 3GPP-owned asymmetric protocol that needs a PQC update.
- **Status:** SECONDARY (via whatthespec.net)

### SEC-04d
- **Citation / Fetched URL:** as SEC-04b
- **Location:** Clause 1 "Scope", bullets 3–4
- **Quote:** "Impact to 3GPP procedures due to larger length of PQC key, signature, and message compared to the length of those in traditional cryptography. … Determines security levels (I-V) required to align with existing 3GPP procedures level of assurance."
- **Figure(s):** NIST security levels I–V
- **Condition:** Study scope.
- **Use in paper:** Motivates the size and latency budget.
- **Status:** SECONDARY (via whatthespec.net)

### SEC-04e
- **Citation:** S. Orkopoulos, "Post Quantum Cryptography in 3GPP," 3GPP Highlights Issue 12, June 2026 (byline: "By Stawros Orkopoulos, SA WG3 Delegate, Nokia"; "Published June 2026, in Highlights Issue 12")
- **Fetched URL:** https://www.3gpp.org/technologies/pqc-sa3
- **Location:** Article body
- **Quote:** "To counteract this, 3GPP SA3 has started a study, documented in TR 33.703, for analysing the transition to PQC-enablement. … The ongoing SID is progressing according to a defined schedule, with a target date for finalization set for June 2026."
- **Figure(s):** target finalization June 2026
- **Condition:** Official 3GPP article. SEC-04a is consistent with it: V20.0.0 appeared at SA#112 in June 2026.
- **Use in paper:** Timeline.
- **Status:** VERIFIED

### SEC-04f
- **Citation / Fetched URL:** as SEC-04e
- **Location:** Article body (timeline)
- **Quote:** "Overall, it is expected that the 3GPP specifications for Rel-20 will be frozen by mid-2027 and the specifications for Rel-21 will be completed not before early 2029 (SP-260360)."
- **Figure(s):** Rel-20 freeze mid-2027; Rel-21 not before early 2029
- **Condition:** Expectation, not a decision. The source cited is SP-260360 (TSG SA#111, Fukuoka, 2026-03).
- **Use in paper:** Earliest dates for normative PQC in 3GPP.
- **Status:** VERIFIED

### SEC-04g
- **Citation / Fetched URL:** as SEC-04e
- **Location:** Article body
- **Quote:** "3GPP defines several protocols within the 3GPP specifications, for example the 5G-SUCI calculation, which is specified in TS 33.501, and MIKEY-SAKKE, which refers to Mission Critical (MCX) and is specified in TS 33.180. 3GPP SA3 Security standards extensively integrate widely used protocols and framework defined by IETF. For example, TLS, IPsec, PKI, JOSE."
- **Figure(s):** —
- **Condition:** Official 3GPP article, June 2026.
- **Use in paper:** Names the asymmetric protocols in 3GPP systems (also supports SEC-05 and SEC-08).
- **Status:** VERIFIED

### SEC-04h
- **Citation:** 3GPP TR 33.938, "3GPP Cryptographic Inventory"
- **Fetched URL:** https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=4380
- **Location:** 3GPP portal specification page
- **Quote:** Title "3GPP Cryptographic Inventory"; Type "Technical report (TR)"; Status "Under change control"; Initial planned Release "Release 19"
- **Figure(s):** 19.0.0 (2025-06-20, SA#108); 19.1.0 (2025-09-26, SA#109); 19.2.0 (2026-01-16, SA#110); 19.3.0 (SA#113, no date shown); WI FS_CryptoInv "Study on 3GPP Cryptographic Inventory"
- **Condition:** Inventory study referenced by the TR 33.703 scope.
- **Use in paper:** Citation for "which primitives exist in 3GPP systems".
- **Status:** VERIFIED (metadata only; the TR text was not fetched)

---

## SEC-05 — GSMA Post-Quantum Telco Network (PQTN) Task Force documents

### SEC-05a
- **Citation:** GSMA, "Post-Quantum Cryptography Documents" (listing page)
- **Fetched URL:** https://www.gsma.com/solutions-and-impact/technologies/security/post-quantum-cryptography-documents/
- **Location:** Document list
- **Quote:** "PQ.07 Post Quantum Cryptography for Non-Terrestrial Networks … PQ.06 Official Document Implementation and Prototype Verification of Post-Quantum Use Case: Hybrid Key Exchange … PQ.05 Quantum-safe Cryptography for 4G and 5G Roaming"
- **Figure(s):** Further titles from the same listing, as returned: "PQ.04 Post Quantum Cryptography in IoT Ecosystem"; "PQ.03 Guidelines for Telecom Use Cases"; "PQ.02 Guidelines for Quantum Risk Management for Telco"; "PQ.01 Post Quantum Telco Network – Impact Assessment – Whitepaper". Listed dates: PQ.07 Feb 2026; PQ.06 May 2026; PQ.05 Jul 2025; PQ.04 Feb 2025; PQ.03 Oct 2024; PQ.02 Sep 2023; PQ.01 Feb 2023.
- **Condition:** Titles and dates are as the fetch tool returned them from the listing. Printed document dates can differ: PQ.05 is "26 June 2025", PQ.04 "25/11/2024", PQ.07 "04 February 2026", PQ.02 "22 September 2023". The URLs found are:
  - PQ.02 v1.0: https://www.gsma.com/get-involved/working-groups/wp-content/uploads/2023/09/Guidelines-for-Quantum-Risk-Management-for-Telco-v1.0.pdf
  - PQ.03 v2.0 news page ("PQ.03 Post Quantum Cryptography – Guidelines for Telecom Use Cases v2.0", "Friday October 4, 2024"): https://www.gsma.com/newsroom/gsma_resources/pq-03-post-quantum-cryptography-guidelines-for-telecom-use-cases/
  - PQ.03 Executive Summary ("Version 2.0 | September 2024"): https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2024/09/Post-Quantum-Cryptography-Use-cases-final.pdf
  - PQ.04 v1.0: https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2025/02/PQ.04-Post-Quantum-Cryptography-in-IoT-Ecosystem-v1.0.pdf
  - PQ.05 v1.0: https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2019/03/PQ.05-Post-Quantum-Cryptography-for-5G-Roaming-use-case-1.pdf
  - PQ.07 V1.0 (resource page dated "Friday February 6, 2026"): https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2026/02/PQ.07-Post-Quantum-Cryptography-for-Non-Terrestrial-Networks.pdf
  - PQ.01: resource page returned 403. Its publication is confirmed by IETF liaison 1817 (SEC-05h).
- **Use in paper:** Related-work and industry-status citations.
- **Status:** VERIFIED (listing page); full-text URL NOT-FOUND for PQ.01 and PQ.06

### SEC-05b
- **Citation:** GSMA PQ.05, "Quantum-safe Cryptography for 4G and 5G Roaming," Version 1.0, 26 June 2025.
- **Fetched URL:** https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2019/03/PQ.05-Post-Quantum-Cryptography-for-5G-Roaming-use-case-1.pdf
- **Location:** p. 17 (Section 5.3 per the tool)
- **Quote:** "The key establishment process on the n32 interface using TLS 1.2 / 1.3 relies on either ECDHE or DHE, and therefore the N32-c and N32-f interfaces are highly susceptible to HNDL type of attacks …"
- **Figure(s):** TLS 1.2 / 1.3 with ECDHE or DHE on N32 (SEPP-to-SEPP)
- **Condition:** 5G roaming interconnect (inter-PLMN SBA). One fetch returned "key exchange process"; a check fetch confirmed "key establishment process".
- **Use in paper:** Names a quantum-vulnerable primitive in the 5G SBA.
- **Status:** VERIFIED

### SEC-05c
- **Citation / Fetched URL:** as SEC-05b
- **Location:** p. 18
- **Quote:** "JSON web tokens (JWT), that are authenticated using JSON web signatures based on ECDSA can be spoofed by IPX intermediaries."
- **Figure(s):** ECDSA-based JWS
- **Condition:** Roaming (N32 / IPX), with a CRQC-capable adversary assumed by the document.
- **Use in paper:** Signature-side vulnerability in the SBA.
- **Status:** VERIFIED

### SEC-05d
- **Citation / Fetched URL:** as SEC-05b
- **Location:** p. 20, Section 6.1.3
- **Quote:** "The Internet Key Exchange (IKE) protocol enables communicating parties (e.g. mobile operator and IPX providers) to establish an IPSec channel by using X.509 certificates for mutual authentication. The key exchange protocol is based on Diffie-Hellman (DH)."
- **Figure(s):** IKE/IPsec with X.509 certificates and DH
- **Condition:** Roaming and IPX context.
- **Use in paper:** IPsec/IKEv2 as a quantum-vulnerable primitive.
- **Status:** VERIFIED

### SEC-05e
- **Citation:** GSMA PQ.02, "Guidelines for Quantum Risk Management for Telco," V1.0, 22 September 2023.
- **Fetched URL:** https://www.gsma.com/get-involved/working-groups/wp-content/uploads/2023/09/Guidelines-for-Quantum-Risk-Management-for-Telco-v1.0.pdf
- **Location:** p. 18
- **Quote:** "Some of the asymmetric protocols used are TLS, IKE, and PKI. All of these are quantum vulnerable."
- **Figure(s):** —
- **Condition:** Telco-wide risk-management guidance.
- **Use in paper:** Short citation for "TLS, IKE and PKI are quantum-vulnerable".
- **Status:** VERIFIED

### SEC-05f
- **Citation:** GSMA PQ.07, "Post Quantum Cryptography for Non-Terrestrial Networks," V1.0, 04 February 2026.
- **Fetched URL:** https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2026/02/PQ.07-Post-Quantum-Cryptography-for-Non-Terrestrial-Networks.pdf
- **Location:** Section 3.6 "Legacy Impact", p. 18
- **Quote:** "Protocols such as IPsec and TLS can support PQC; early versions rely on cryptographic algorithms (e.g., RSA, DH, ECDH) that are not quantum-safe."
- **Figure(s):** RSA, DH, ECDH (named as not quantum-safe)
- **Condition:** NTN / satellite context. The document does not mention SUCI or ECIES (the tool checked).
- **Use in paper:** NTN section: PQC migration for satellite links.
- **Status:** VERIFIED

### SEC-05g
- **Citation:** GSMA PQ.03, "Post Quantum Cryptography – Guidelines for Telecom Use Cases," Executive Summary, Version 2.0, September 2024.
- **Fetched URL:** https://www.gsma.com/solutions-and-impact/technologies/security/wp-content/uploads/2024/09/Post-Quantum-Cryptography-Use-cases-final.pdf
- **Location:** p. 4
- **Quote:** "The evolution of quantum computing capabilities poses a threat as they have the potential to render obsolete the most used cryptographic algorithms, such as public key cryptography, which underpin the cyber security solutions we rely on today."
- **Figure(s):** —
- **Condition:** Executive summary only; the full PQ.03 v2.0 was not reachable.
- **Use in paper:** General motivation.
- **Status:** VERIFIED

### SEC-05h
- **Citation:** IETF liaison statements from GSMA: #1817, "LS to inform about the Post Quantum Telco Network Impact Assessment Whitepaper Publication" (GSMA → pquip, submitted 2023-03-07); #1894, "LS regarding the publication of the Post Quantum Cryptography – Guidelines for Telecom Use Cases document in Feb 24" (GSMA → SEC area, submitted 2024-02-07).
- **Fetched URL:** https://datatracker.ietf.org/liaison/1817/ and https://datatracker.ietf.org/liaison/1894/
- **Location:** Liaison body (#1894)
- **Quote:** "This is the first detailed, telco sector-specific, analysis of the implications of the transition to Post Quantum Cryptography for the telecom industry."
- **Figure(s):** 2023-03-07; 2024-02-07
- **Condition:** The liaison dates bracket the publications. #1817 (2023-03-07) informs pquip that the PQ.01 whitepaper has been published. #1894 (2024-02-07) announces that PQ.03 (v1) is to be published in "Feb 24".
- **Use in paper:** Dating the PQTN documents.
- **Status:** VERIFIED

### SEC-05i
- **Citation:** GSMA, "Post-Quantum Cryptography | Security" web page (undated)
- **Fetched URL:** https://www.gsma.com/solutions-and-impact/technologies/security/post-quantum/
- **Location:** Page body
- **Quote:** "Data transits from a base station to a network security gateway may be secured with IPSec, typically using asymmetric (quantum vulnerable) methods for key exchange."
- **Figure(s):** —
- **Condition:** RAN backhaul (base station to SEG). Undated web page.
- **Use in paper:** Backhaul IPsec as a quantum-vulnerable link (compare with SEC-08d, N2).
- **Status:** VERIFIED

---

## SEC-06 — IETF hybrid key exchange for TLS 1.3: X25519MLKEM768

### SEC-06a
- **Citation:** K. Kwiatkowski, P. Kampanakis, B. E. Westerbaan, D. Stebila, "Post-quantum hybrid ECDHE-MLKEM Key Agreement for TLSv1.3," IETF Internet-Draft draft-ietf-tls-ecdhe-mlkem-05 (tls WG), 26 May 2026, Intended status: Standards Track. The authors and date were read from https://www.ietf.org/archive/id/draft-ietf-tls-ecdhe-mlkem-05.html.
- **Fetched URL:** https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/
- **Location:** Datatracker document metadata
- **Quote:** Status "Active Internet-Draft (tls WG)"; IESG state "Approved-announcement sent"; RFC Editor state "In Progress"; Intended RFC status "Proposed Standard"; Last updated "2026-08-09 (Latest revision 2026-05-26)"
- **Figure(s):** No RFC number as of 2026-09-27 (IESG-approved and in the RFC Editor queue)
- **Condition:** Status on the access date. The RFC Editor queue page itself was not readable (JavaScript).
- **Use in paper:** Cite as an Internet-Draft approved for Proposed Standard, not as an RFC.
- **Status:** VERIFIED

### SEC-06b
- **Citation:** draft-ietf-tls-ecdhe-mlkem-05 (26 May 2026)
- **Fetched URL:** https://www.ietf.org/archive/id/draft-ietf-tls-ecdhe-mlkem-05.html
- **Location:** Section 4.1 "Client share"
- **Quote:** "The size of the client share is 1216 bytes (1184 bytes for the ML-KEM part and 32 bytes for X25519)."
- **Figure(s):** X25519MLKEM768 client key_exchange = 1216 bytes (1184 ML-KEM + 32 X25519)
- **Condition:** TLS 1.3 ClientHello key_share, group X25519MLKEM768 (codepoint 4588 = 0x11EC per §7.1, from the tool).
- **Use in paper:** Per-handshake uplink bytes.
- **Status:** VERIFIED

### SEC-06c
- **Citation / Fetched URL:** as SEC-06b
- **Location:** Section 4.2 "Server share"
- **Quote:** "The size of the server share is 1120 bytes (1088 bytes for the ML-KEM part and 32 bytes for X25519)."
- **Figure(s):** X25519MLKEM768 server key_exchange = 1120 bytes (1088 ML-KEM + 32 X25519)
- **Condition:** TLS 1.3 ServerHello key_share.
- **Use in paper:** Per-handshake downlink bytes.
- **Status:** VERIFIED

### SEC-06d
- **Citation / Fetched URL:** as SEC-06b
- **Location:** Sections 4.1 and 4.2 (the other two groups)
- **Quote:** "The size of the client share is 1249 bytes (65 bytes for the secp256r1 part and 1184 bytes for ML-KEM). … The size of the server share is 1153 bytes (1088 bytes for the ML-KEM part and 65 bytes for secp256r1)."
- **Figure(s):** SecP256r1MLKEM768: client 1249 bytes, server 1153 bytes. SecP384r1MLKEM1024 from the same sections: client "1665 bytes (97 bytes for the secp384r1 part and 1568 for ML-KEM)", server "1665 bytes (1568 bytes for the ML-KEM part and 97 bytes for secp384r1)".
- **Condition:** TLS 1.3 hybrid groups.
- **Use in paper:** Profile alternatives, e.g. P-256-based hybrids for the 5GC TLS profile (SEC-08).
- **Status:** VERIFIED

### SEC-06e
- **Citation / Fetched URL:** as SEC-06b
- **Location:** Section 4.3 (shared secret)
- **Quote:** "The shared secret is 64 bytes (32 bytes for each part)."
- **Figure(s):** 64-byte shared secret (X25519MLKEM768)
- **Condition:** From a single fetch. The tool also reported the concatenation order "ML-KEM shared secret followed by X25519 shared secret", but that is not quoted here.
- **Use in paper:** Key-schedule input size (minor).
- **Status:** VERIFIED

---

## SEC-07 — Share of TLS traffic using post-quantum key agreement (Cloudflare)

### SEC-07a
- **Citation:** D. Belson, "The 2025 Cloudflare Radar Year in Review: The rise of AI, post-quantum, and record-breaking DDoS attacks," Cloudflare Blog, 15 Dec 2025.
- **Fetched URL:** https://blog.cloudflare.com/radar-2025-year-in-review/
- **Location:** Section headed "The share of human-generated Web traffic that is post-quantum encrypted has grown to 52%"
- **Quote:** "After seeing significant growth in 2024, the global share of post-quantum encrypted traffic nearly doubled throughout 2025, from 29% at the start of the year to 52% in early December."
- **Figure(s):** 29% (start of 2025) → 52% (early December 2025)
- **Condition:** Only traffic seen by Cloudflare, human-generated Web traffic; "data spanning the period from January 1 to December 2, 2025". The post does not name the key-agreement group. The Radar chart is titled "Post-quantum encrypted share of HTTPS request traffic" and "shows the percentage of HTTPS requests using post-quantum key exchange over time" (chart text only; values not rendered).
- **Use in paper:** Deployment status of hybrid PQ key agreement in TLS.
- **Status:** VERIFIED

### SEC-07b
- **Citation:** B. Westerbaan, "State of the post-quantum Internet in 2025," Cloudflare Blog, 28 Oct 2025.
- **Fetched URL:** https://blog.cloudflare.com/pq-2025/
- **Location:** Opening
- **Quote:** "This week, the last week of October 2025, we reached a major milestone for Internet security: the majority of human-initiated traffic with Cloudflare is using post-quantum encryption mitigating the threat of harvest-now/decrypt-later."
- **Figure(s):** "majority" (>50%, no exact number), last week of October 2025
- **Condition:** Cloudflare vantage point; human-initiated traffic.
- **Use in paper:** Dated milestone.
- **Status:** VERIFIED

### SEC-07c
- **Citation:** B. Westerbaan, "Cloudflare targets 2029 for full post-quantum security," Cloudflare Blog, 7 Apr 2026 (the tool reported a last-modified date of 15 Jul 2026).
- **Fetched URL:** https://blog.cloudflare.com/post-quantum-roadmap/
- **Location:** Section "Cloudflare is accelerating its post-quantum roadmap"
- **Quote:** "While we're excited by the fact that over 65% of human traffic to Cloudflare is post-quantum encrypted, our work is not done until authentication is also upgraded."
- **Figure(s):** over 65% of human traffic
- **Condition:** Cloudflare vantage point. The sentence gives no measurement date; the post is dated 7 Apr 2026. Key agreement only; the post stresses that authentication is not yet PQ.
- **Use in paper:** Most recent dated figure (2026).
- **Status:** VERIFIED

---

## SEC-08 — TLS and IPsec/IKEv2 between 5G core network functions

### SEC-08a
- **Citation:** 3GPP TS 33.501 clause 13.1.0 "General" under 13.1 "Protection at the network or transport layer" (itecspec "Rel-20")
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/13.1.0
- **Location:** Clause 13.1.0
- **Quote:** "All network functions shall support mutually authenticated TLS and HTTPS as specified in RFC 9113 [47] and RFC 9110 [113]. … TLS shall be used for transport protection within a PLMN unless network security is provided by other means."
- **Figure(s):** —
- **Condition:** Service-based interfaces (SBA) inside a PLMN; normative.
- **Use in paper:** Classical public-key primitives in the 5GC are those of TLS (ECDHE + certificates).
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-08b
- **Citation / Fetched URL:** as SEC-08a
- **Location:** Clause 13.1.0
- **Quote:** "The TLS profile shall follow the profile given in clause 6.2 of TS 33.210 [3] with the restriction that it shall be compliant with the profile given by HTTP/2. … TLS client and server certificates shall be compliant with the SBA certificate profile specified in clause 6.1.3c of TS 33.310 [5]."
- **Figure(s):** —
- **Condition:** as SEC-08a
- **Use in paper:** Links the 5GC TLS profile to TS 33.210 §6.2 (SEC-08g–i).
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-08c
- **Citation / Fetched URL:** as SEC-08a
- **Location:** Clause 13.1.0
- **Quote:** "Regardless of whether TLS is used or not, NDS/IP as specified in TS 33.210 [3] and TS 33.310 [5] can be used for network layer protection."
- **Figure(s):** —
- **Condition:** Optional network-layer protection (IPsec) for SBA.
- **Use in paper:** IPsec/IKEv2 as the second 5GC primitive family.
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-08d
- **Citation:** 3GPP TS 33.501 clause 9.2 "Security mechanisms for the N2 interface" (itecspec "Rel-20")
- **Fetched URL:** https://itecspec.com/3gpp/33.501/s/9.2
- **Location:** Clause 9.2
- **Quote:** "IPsec is mandatory to implement on the gNB and the ng-eNB. … Mutual authentication shall be supported over the N2 interface between the AMF and the 5G-AN using DTLS and/or IKEv2."
- **Figure(s):** — (the clause also refers to "IPsec ESP and IKEv2 certificates-based authentication as specified in sub-clause 9.1.2")
- **Condition:** N2 (gNB to AMF, non-SBA). The tool's summary (not a quote) says the clause leaves use of the cryptographic solutions to the operator. Check before relying on this.
- **Use in paper:** RAN-to-core control-plane link: IKEv2/DTLS public-key handshakes.
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-08e
- **Citation / Fetched URL:** as SEC-08d
- **Location:** Clause 9.2
- **Quote:** "DTLS shall be supported as specified in RFC 6083 [58] to provide mutual authentication, integrity protection, replay protection and confidentiality protection."
- **Figure(s):** —
- **Condition:** N2. The tool reported that the DTLS profile follows TS 33.210 clause 6.2 and TS 33.310 clause 6.1.3a (paraphrase, not quoted).
- **Use in paper:** as SEC-08d
- **Status:** SECONDARY (itecspec Rel-20)

### SEC-08f
- **Citation:** ETSI TS 133 210 V19.3.0 (2026-02), "Digital cellular telecommunications system (Phase 2+) (GSM); Universal Mobile Telecommunications System (UMTS); LTE; 5G; Network Domain Security (NDS); IP network layer security (3GPP TS 33.210 version 19.3.0 Release 19)" (cover page). The latest ETSI directory on 2026-09-27 was 19.03.00_60 (2/26/2026).
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/133200_133299/133210/19.03.00_60/ts_133210v190300p.pdf
- **Location:** Clause 5.4.2 "Profiling of IKEv2", under "For IKE_SA_INIT exchange:"
- **Quote:** "Following algorithms shall be supported: … Diffie-Hellman group 19 (256-bit random ECP group) … Following algorithms should be supported: … Diffie-Hellman group 20 (384-bit random ECP group). Diffie-Hellman group 31 (Curve25519). … For security reasons, the use of Diffie-Hellman MODP groups less than 2048-bit shall not be supported."
- **Figure(s):** DH group 19 "(256-bit random ECP group)" shall; group 20 "(384-bit random ECP group)" and group 31 "(Curve25519)" should; MODP groups "less than 2048-bit shall not be supported"
- **Condition:** NDS/IP IKEv2 profile. TS 33.501 points to it for N2 (SEC-08d, via sub-clause 9.1.2) and as optional network-layer protection for the SBA (SEC-08c); other interfaces were not checked. The only IKE_AUTH line the tool found was "Authentication method 2 - Shared Key Message Integrity Code shall be supported." The tool reported no certificate or digital-signature method in 5.4. SEC-08d refers to "certificates-based authentication"; TS 33.310 was not fetched.
- **Use in paper:** Classical key exchange in 5GC/RAN IPsec.
- **Status:** VERIFIED

### SEC-08g
- **Citation / Fetched URL:** as SEC-08f
- **Location:** Clause 6.2.1 (TLS profile)
- **Quote:** "TLS 1.2 as specified in RFC 5246 [50] shall be supported. TLS 1.3 as specified in RFC 8446 [66] shall be supported."
- **Figure(s):** TLS 1.2 and 1.3 both mandatory to support
- **Condition:** Profile referenced by TS 33.501 §13.1.0 (SEC-08b).
- **Use in paper:** Base TLS versions in the 5GC.
- **Status:** VERIFIED

### SEC-08h
- **Citation / Fetched URL:** as SEC-08f
- **Location:** Clause 6.2.3 (TLS 1.2 profile, per the tool)
- **Quote:** "For ECDHE, the curve secp256r1 (P-256) as defined in RFC 8422 [71] shall be supported, secp384r1 (P-384) as defined in RFC 8422 [71] should be supported. … Except x25519, elliptic curve groups of less than 256 bits shall not be supported. … Finite field Diffie-Hellman (i.e. DHE) shall not be supported."
- **Figure(s):** secp256r1 shall; secp384r1 should; DHE shall not
- **Condition:** TLS 1.2 profile.
- **Use in paper:** Classical ECDHE in the 5GC.
- **Status:** VERIFIED

### SEC-08i
- **Citation / Fetched URL:** as SEC-08f
- **Location:** Clause 6.2.2 (TLS 1.3 profile, per the tool)
- **Quote:** "The requirements given in section 9.1 of TLS 1.3 RFC 8446 [66] shall be followed. … Key exchange with secp384r1 should be supported. … ecdsa_secp384r1_sha384 should be supported."
- **Figure(s):** RFC 8446 §9.1 mandatory-to-implement set, plus secp384r1 (should) and ecdsa_secp384r1_sha384 (should). The tool also reported "Ffdhe2048 shall not be supported" and "TLS_SHA256_SHA256 and TLS_SHA384_SHA384 shall not be supported."
- **Condition:** TLS 1.3 profile. RFC 8446 §9.1 itself could not be fetched (truncated), so the mandatory-to-implement group and signature list is **not** in this ledger. The tool found no mention of "quantum", "ML-KEM", "hybrid" or "post-quantum" in the TS 33.210 V19.3.0 text it received. Treat this as indicative only, since the text may have been truncated.
- **Use in paper:** Indicates, but does not confirm, that the Rel-19 5GC TLS profile names no PQ hybrid group. Check TS 33.210 V19.3.0 §6.2 by hand before claiming this. Pair with SEC-06 and SEC-04.
- **Status:** VERIFIED (quotes); NOT-FOUND (RFC 8446 §9.1 text)
