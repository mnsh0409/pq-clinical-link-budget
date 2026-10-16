# NTN cluster — 3GPP NTN reference parameters + deployment scenarios

Ledger file per `README.md`. Access date for every entry: **2026-09-27**.
Collection method: WebSearch + WebFetch only (no other HTTP clients).

## Read first — source, version and tool notes

- **TR 38.821.** ETSI does not publish a TR 138 821 (`https://www.etsi.org/deliver/etsi_tr/138800_138899/138821/` → 404; the
  parent directory lists only `13881702` and `138854`). Fetched the official 3GPP Organizational-Partner transposition
  **ATIS.3GPP.38.821.V1600 = 3GPP TR 38.821 V16.0.0 (2019-12)**. The 3GPP portal (specificationId=3525) lists newer
  **V16.1.0 (upload 2021-06-30)** and **V16.2.0 (upload 2023-04-03, latest; no Rel-17+ version)**. The Table 4.2-2 rows were
  cross-checked against iTecSpec's Rel-16 rendering (version not labelled) and matched.
- **TR 38.811.** ETSI TR 138 811 directory → 404. Fetched **ATIS.3GPP.38.811.V1530 (V15.3.0; portal upload 2020-07-22)**.
  The cover page was not in the extracted text (the version comes from the ATIS file name; one extraction returned an
  unrelated title, "Study on channel model for frequencies from 0.5 to 100 GHz", in error). Title confirmed from the 3GPP portal and from an NCU-hosted copy of V15.1.0. Latest version:
  **V15.4.0 (portal upload 2020-10-08)**.
- **TR 38.913.** Fetched **ETSI TR 138 913 V19.0.0 (2025-10)**, which is the latest (portal: 19.0.0, 2025-10-14, SA#109).
- **TS 38.300.** Fetched ETSI TS 138 300 **V19.3.0 (2026-08), V18.10.0 (2026-08) and V17.17.0 (2026-08)**. WebFetch's text
  window ends inside the table of contents, so only the §16.14 clause *headings* are verified from the primary. The clause
  *bodies* come from iTecSpec's per-clause rendering, labelled "Rel-19" with no exact version → **SECONDARY**. Newer 3GPP
  versions exist: **V19.4.0 and V18.11.0 (both uploaded 2026-09-25, RAN#113)**. No Rel-20 version is listed.
- **Tool limits.** (i) The WebFetch text window ends around §6.1.4.2 of the ATIS TR 38.821 PDF, around §5.3.3 of ATIS
  TR 38.811, at §5.3.2.3 of the NCU TR 38.811 copy, and inside the TOC of every TS 38.300 PDF. Later clauses were
  reached only via the iTecSpec mirror (SECONDARY). (ii) WebFetch caps quotes at about 125 characters, so long sentences
  came back in consecutive fragments. They are joined here with one space, with no words added or removed. (iii) In quotes, ` | ` separates table cells as
  rendered by the extraction, and ` / ` separates excerpts that were extracted separately and may not be adjacent.
- **Blocked:** tech-invite.com (WebFetch: robots.txt disallowed). It was not used, per the rules.
- **iTecSpec** (itecspec.com) is a third-party web rendering of 3GPP text. Every entry quoted from it is **SECONDARY** and
  names both the mirror and the primary.

---

## NTN-01 — TR 38.821 reference-scenario parameters (Table 4.2-2)

### NTN-01a  (altitudes)
- **Citation:** 3GPP, "Solutions for NR to support non-terrestrial networks (NTN)," TR 38.821 V16.0.0 (Release 16), Dec. 2019; published as ATIS.3GPP.38.821.V1600. https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2 "Reference scenario parameters", header row + "Altitude" row (pp. 19–20 per extraction)
- **Quote:** "Scenarios | GEO based non-terrestrial access network (Scenario A and B) | LEO based non-terrestrial access network (Scenario C & D)" / "Altitude | 35,786 km | 600 km, 1,200 km"
- **Figure(s):** 35,786 km (GEO); 600 km and 1,200 km (LEO)
- **Condition:** TR 38.821 V16.0.0 (Rel-16) reference scenarios. §4.2: "Six scenarios are considered as depicted in Table 4.2-1 and are detailed in Table 4.2-2." (A = GEO transparent, B = GEO regenerative, C1/C2 = LEO transparent, D1/D2 = LEO regenerative; see NTN-01b)
- **Use in paper:** NTN latency/geometry model (NTN budget section); inputs for the model scripts.
- **Status:** VERIFIED (ATIS OP transposition of V16.0.0; latest is V16.2.0, and iTecSpec's Rel-16 rendering shows the same values)

### NTN-01b  (payload type per scenario)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2, "Payload" row
- **Quote:** "Payload | Scenario A: Transparent (including radio frequency function only) Scenario B: regenerative (including all or part of RAN functions) | Scenario C: Transparent (including radio frequency function only) Scenario D: Regenerative (including all or part of RAN functions)"
- **Figure(s):** — (defines the transparent/regenerative label for each scenario)
- **Condition:** TR 38.821 V16.0.0; applies to all Table 4.2-2 delay rows
- **Use in paper:** labels transparent vs regenerative in every NTN delay figure
- **Status:** VERIFIED

### NTN-01c  (minimum elevation angle)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2, minimum-elevation row
- **Quote:** "Min Elevation angle for both satgateway and user equipment | 10° for service link and 10° for feeder link | 10° for service link and 10° for feeder link"
- **Figure(s):** 10° (service link), 10° (feeder link), for both GEO and LEO
- **Condition:** TR 38.821 V16.0.0. The ATIS extraction shows "satgateway"; iTecSpec's Rel-16 rendering of the same row shows "sat-gateway".
- **Use in paper:** elevation assumption behind every Table 4.2-2 delay; input for the pass-geometry script
- **Status:** VERIFIED

### NTN-01d  (max slant range at min elevation)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2
- **Quote:** "Max distance between satellite and user equipment at min elevation angle | 40,581 km | 1,932 km (600 km altitude) 3,131 km (1,200 km altitude)"
- **Figure(s):** 40,581 km (GEO); 1,932 km (LEO 600 km); 3,131 km (LEO 1,200 km)
- **Condition:** at the 10° minimum elevation (NTN-01c); TR 38.821 V16.0.0
- **Use in paper:** geometry cross-check for the pass-duration and delay scripts
- **Status:** VERIFIED

### NTN-01e  (max round-trip delay, transparent vs regenerative)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2, RTD row
- **Quote:** "Max Round Trip Delay (propagation delay only) | Scenario A: 541.46 ms (service and feeder links) Scenario B: 270.73 ms (service link only) | Scenario C: (transparent payload: service and feeder links) 25.77 ms (600km) 41.77 ms (1200km) Scenario D: (regenerative payload: service link only) 12.89 ms (600km) 20.89 ms (1200km)"
- **Figure(s):** GEO transparent (A) 541.46 ms; GEO regenerative (B) 270.73 ms; LEO transparent (C) 25.77 ms @600 km, 41.77 ms @1200 km; LEO regenerative (D) 12.89 ms @600 km, 20.89 ms @1200 km
- **Condition:** propagation delay only (no processing). Transparent = service + feeder links; regenerative = service link only. The table's minimum elevation is 10° for both links (NTN-01c), but this row does not restate it. TR 38.821 V16.0.0.
- **Use in paper:** per-round-trip cost of (PQ-)TLS/DTLS handshakes and key updates over NTN (NTN budget section)
- **Status:** VERIFIED (Scenario A/B text also matches iTecSpec's rendering)

### NTN-01f  (max differential delay within a cell)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2 + NOTE 6
- **Quote:** "Max differential delay within a cell (Note 6) | 10.3 ms | 3.12 ms and 3.18 ms for respectively 600km and 1200km"
- **Figure(s):** 10.3 ms (GEO); 3.12 ms (LEO 600 km); 3.18 ms (LEO 1200 km)
- **Condition:** cell level. NOTE 6: "The maximum differential delay at cell level has been computed considering the one at beam level for largest beam size." Largest beam: NTN-01h. TR 38.821 V16.0.0.
- **Use in paper:** timing/jitter margin in the NTN budget (e.g., replay-window and timeout sizing)
- **Status:** VERIFIED

### NTN-01g  (speed of light used)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2, NOTE 4
- **Quote:** "Speed of light used for delay calculation is 299792458 m/s."
- **Figure(s):** 299792458 m/s
- **Condition:** constant behind the Table 4.2-2 delays
- **Use in paper:** model scripts must use the same constant to reproduce NTN-01e
- **Status:** VERIFIED

### NTN-01h  (max beam footprint)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2
- **Quote:** "Max beam foot print size (edge to edge) regardless of the elevation angle | 3500 km (Note 5) | 1000 km"
- **Figure(s):** 3500 km (GEO); 1000 km (LEO)
- **Condition:** edge to edge, regardless of elevation. NOTE 5 says the GEO value is "based on current state of the art GEO High Throughput systems". TR 38.821 V16.0.0.
- **Use in paper:** cell-size bound for the handover-rate model
- **Status:** VERIFIED

### NTN-01i  (satellite speed, TR 38.821)
- **Citation:** 3GPP TR 38.821 (Rel-16), §7.3.2.1.4, Table 7.3.2.1.4-1 "Time to HO for min/max cell diameter and varying UE speed"; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.821/s/7.3.2.1.4 (accessed 2026-09-27)
- **Location:** §7.3.2.1.4, Table 7.3.2.1.4-1, header, one row and NOTE 1
- **Quote:** "Cell Diameter Size (km) | UE Speed (km/hr) | Satellite Speed (km/s) | Time to HO (s)" / "50 (lower bound) | Neglected | 7.56 (NOTE 1) | 6.61" / "This value may need to be updated further pending clarification from satellite companies (e.g. if this is the ground speed, and what altitude this value corresponds to)."
- **Figure(s):** 7.56 km/s
- **Condition:** LEO. **No altitude is stated**, and NOTE 1 leaves open whether this is ground speed and which altitude it applies to. Rel-16 (exact version not shown).
- **Use in paper:** handover-rate model (flag the caveat)
- **Status:** SECONDARY (via iTecSpec rendering of 3GPP TR 38.821 §7.3.2.1.4). The primary ATIS V16.0.0 PDF was fetched, but the WebFetch window ends around §6.1.4.2, and a search of the reachable text found no km/s value.

### NTN-01j  (satellite speed at 600 km, TR 38.811)
- **Citation:** 3GPP, "Study on New Radio (NR) to support non-terrestrial networks," TR 38.811 (Rel-15), §5.3.4.3; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.811/s/5.3.4.3 (accessed 2026-09-27)
- **Location:** §5.3.4.3 "Doppler Shift and variation rate"
- **Quote:** "For all Non GSO cases, the satellite speeds are the following" / "At 600 km : V =7.5622 km.s-1" / "At 1500 km : V =7.1172 km.s-1" / "At 10000 km : V =4.9301 km.s-1"
- **Figure(s):** 7.5622 km/s (600 km); 7.1172 km/s (1500 km); 4.9301 km/s (10000 km)
- **Condition:** non-GSO circular orbits at the stated altitudes; TR 38.811 Rel-15 (exact version not shown)
- **Use in paper:** satellite velocity for the pass-duration and Doppler scripts
- **Status:** SECONDARY (via iTecSpec rendering of 3GPP TR 38.811 §5.3.4.3). The primary ATIS V15.3.0 and the NCU-hosted V15.1.0 PDFs were fetched, but their windows end at §5.3.3 and §5.3.2.3.

### NTN-01k  (generic non-GEO orbital speed, TR 38.811)
- **Citation:** 3GPP, "Study on New Radio (NR) to support non-terrestrial networks," TR 38.811 V15.3.0 (Release 15); published as ATIS.3GPP.38.811.V1530. https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §5.3.1.3 (Doppler shift/variation methodology)
- **Quote:** "For a relative speed of Non-Geo satellite of 7.5 km/s (orbital speed): the ratio is 0.000025"
- **Figure(s):** 7.5 km/s (orbital speed); ratio 0.000025
- **Condition:** illustrative non-GEO value in the Doppler methodology; no altitude stated; TR 38.811 V15.3.0
- **Use in paper:** Doppler sanity check only (prefer NTN-01j for 600 km)
- **Status:** VERIFIED

### NTN-01l  (maximum one-way delay in TR 38.821)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** Table 4.2-2 and the reachable text (to about §6.1.4.2)
- **Quote:** none. Table 4.2-2 has no one-way-delay row. The only "one-way" hit was the §3.1 definition of "One-way latency" ("time required to propagate through a telecommunication system from a terminal to the public data network or from the public data network to the terminal."), which gives no figure.
- **Figure(s):** —
- **Condition:** —
- **Use in paper:** use the TR 38.811 one-way delays instead: NTN-03j (GEO, VERIFIED) and NTN-03k/NTN-03l (LEO 600 km, SECONDARY)
- **Status:** NOT-FOUND in TR 38.821 (searched Table 4.2-2 and the reachable ATIS text)

---

## NTN-02 — Doppler / UE-speed assumptions; service-link switch, feeder-link switch, CHO, service continuity

### NTN-02a  (UE speed, aircraft / HST)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2
- **Quote:** "User equipment motion on the earth | 1200 km/h (e.g. aircraft) | 500 km/h (e.g. high speed train)Possibly 1200 km/h (e.g. aircraft)"
- **Figure(s):** GEO: 1200 km/h (aircraft); LEO: 500 km/h (high-speed train), possibly 1200 km/h (aircraft)
- **Condition:** reference-scenario UE mobility; TR 38.821 V16.0.0 (same text in iTecSpec's Rel-16 rendering)
- **Use in paper:** mobility cases (air ambulance, train) in the NTN budget
- **Status:** VERIFIED

### NTN-02b  (max Doppler shift)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2
- **Quote:** "Max Doppler shift (earth fixed user equipment) | 0.93 ppm | 24 ppm (600km)21ppm(1200km)"
- **Figure(s):** 0.93 ppm (GEO); 24 ppm (LEO 600 km); 21 ppm (LEO 1200 km)
- **Condition:** earth-fixed UE, so UE motion is excluded; TR 38.821 V16.0.0
- **Use in paper:** NTN link-condition background (Doppler)
- **Status:** VERIFIED

### NTN-02c  (max Doppler shift variation)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2
- **Quote:** "Max Doppler shift variation (earth fixed user equipment) | 0.000 045 ppm/s | 0.27ppm/s (600km)0.13ppm/s(1200km)"
- **Figure(s):** 0.000 045 ppm/s (GEO); 0.27 ppm/s (LEO 600 km); 0.13 ppm/s (LEO 1200 km)
- **Condition:** earth-fixed UE; TR 38.821 V16.0.0
- **Use in paper:** NTN link-condition background
- **Status:** VERIFIED

### NTN-02d  (GNSS/ephemeris prerequisite; UE Doppler pre-compensation)
- **Citation:** 3GPP, "NR; NR and NG-RAN Overall description; Stage-2," TS 38.300 Rel-19, §16.14.2.2 "Timing Advance and Frequency Pre-compensation" (p. 237 in ETSI TS 138 300 V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.2.2 (accessed 2026-09-27)
- **Location:** §16.14.2.2
- **Quote:** "The UE shall have valid GNSS position as well as ephemeris and Common TA before connecting to an NTN cell." / "The UE shall compute the frequency Doppler shift of the service link, and autonomously pre-compensate for it in the uplink transmissions."
- **Figure(s):** — (qualitative)
- **Condition:** TS 38.300 Rel-19 (mirror; exact version not shown); applies to NR NTN UEs
- **Use in paper:** threat/assumption note (GNSS and ephemeris dependence of NTN access)
- **Status:** SECONDARY (via iTecSpec rendering of 3GPP TS 38.300 §16.14.2.2). The primary ETSI TS 138 300 V19.3.0 PDF was fetched, but the WebFetch window ends in the TOC; the clause heading is confirmed there.

### NTN-02e  (definitions: feeder-link switchover, service-link switch)
- **Citation:** 3GPP TS 38.300 Rel-19, §16.14.4.1 "Definitions" (p. 240 in the V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.4.1 (accessed 2026-09-27)
- **Location:** §16.14.4.1
- **Quote:** "A feeder link switchover is the procedure where the feeder link is changed from a source NTN Gateway to a target NTN Gateway for an NTN payload." / "Service link switch refers to a change of the serving NTN payload." / "Both hard and soft feeder link switchover are supported in NTN payloads."
- **Figure(s):** —
- **Condition:** TS 38.300 Rel-19 (mirror)
- **Use in paper:** taxonomy of NTN mobility events that may trigger re-authentication or re-keying
- **Status:** SECONDARY (via iTecSpec; primary V19.3.0 TOC confirms the clause at p. 240)

### NTN-02f  (feeder-link switch over: UE transfer between gNBs; soft switch)
- **Citation:** 3GPP TS 38.300 Rel-19, §16.14.4.2 "Assumptions" (p. 240 in the V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.4.2 (accessed 2026-09-27)
- **Location:** §16.14.4.2
- **Quote:** "A feeder link switch over may result in transferring the established connection for the affected UEs between two gNBs." / "For soft feeder link switch over, an NTN payload is able to connect to more than one NTN Gateway during a given period, i.e. a temporary overlap can be ensured during the transition between the feeder links."
- **Figure(s):** —
- **Condition:** TS 38.300 Rel-19 (mirror); soft feeder-link switch over
- **Use in paper:** whether a feeder-link switch forces a gNB change, and hence a new AS security context
- **Status:** SECONDARY (via iTecSpec; primary TOC confirms the clause)

### NTN-02g  (hard feeder-link switch over: interruption)
- **Citation:** as NTN-02f
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.4.2 (accessed 2026-09-27)
- **Location:** §16.14.4.2
- **Quote:** "For hard feeder link switch over, an NTN payload connects to only one NTN Gateway at any given time, i.e. a radio link interruption may occur during the transition between the feeder links."
- **Figure(s):** — (no interruption duration stated)
- **Condition:** TS 38.300 Rel-19 (mirror); hard feeder-link switch over
- **Use in paper:** interruption event in the NTN mobility-security budget (duration not specified by 3GPP)
- **Status:** SECONDARY (via iTecSpec; primary TOC confirms the clause)

### NTN-02h  (CHO in NTN: time- and location-based triggers)
- **Citation:** 3GPP TS 38.300 Rel-19, §16.14.3.2.2 "Conditional Handover" (p. 238 in the V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.2 (accessed 2026-09-27)
- **Location:** §16.14.3.2.2
- **Quote:** "Time-based or location-based trigger conditions may be configured independently from the RRM measurement-based trigger conditions for CHO in NTN in some scenarios" / "It is up to UE implementation how the UE evaluates the time- or location-based trigger condition together with the RRM measurement-based event." / "Time-based CHO can be performed via RACH-less."
- **Figure(s):** — (the trigger types listed are "The RRM measurement-based event A4", "A time-based trigger condition", "A location-based trigger condition")
- **Condition:** TS 38.300 Rel-19 (mirror). The CHO clause appears in the Rel-17 TOC too (V17.17.0, p. 180).
- **Use in paper:** CHO allows the target to be prepared in advance, so security can be pre-established before the switch (mobility-security section)
- **Status:** SECONDARY (via iTecSpec; primary TOCs confirm the clause in V17.17.0, V18.10.0 and V19.3.0)

### NTN-02i  (CHO triggers, 3GPP overview page)
- **Citation:** J. Krause (3GPP MCC), "Non-Terrestrial Networks (NTN)," 3GPP website (no date shown). https://www.3gpp.org/technologies/ntn-overview
- **Fetched URL:** https://www.3gpp.org/technologies/ntn-overview (accessed 2026-09-27)
- **Location:** Release 17 section
- **Quote:** "Triggering conditions upon which a UE may execute Conditional Hand-Over (CHO) to a candidate cell, have been introduced: event A4, time-based trigger condition, location-based trigger condition."
- **Figure(s):** —
- **Condition:** Rel-17 NR NTN; 3GPP-authored overview (not normative)
- **Use in paper:** release attribution for NTN CHO triggers
- **Status:** VERIFIED (3GPP-authored web overview, not a specification)

### NTN-02j  (service continuity TN↔NTN, 3GPP overview page)
- **Citation:** as NTN-02i
- **Fetched URL:** https://www.3gpp.org/technologies/ntn-overview (accessed 2026-09-27)
- **Location:** Release 17 section
- **Quote:** "The 5G system shall support service continuity between 5G terrestrial access network and 5G satellite access networks owned by the same operator or owned by different operators having an agreement."
- **Figure(s):** —
- **Condition:** Rel-17 section of the page, which states it as a requirement but gives no normative spec reference (no normative source was fetched). The page also lists "NTN-TN and NTN-NTN mobility and service continuity enhancements" under Rel-18 NR_NTN_enh.
- **Use in paper:** motivation for TN↔NTN handover security in clinical continuity
- **Status:** VERIFIED (3GPP-authored web overview; normative source not fetched)

### NTN-02k  (NTN handover properties: no dual connection, no DAPS, RACH-less)
- **Citation:** 3GPP TS 38.300 Rel-19, §16.14.3.2.1 "Handover" (p. 238 in the V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.1 (accessed 2026-09-27)
- **Location:** §16.14.3.2.1
- **Quote:** "During mobility between NTN and TN, a UE is not required to connect to both NTN and TN at the same time." / "DAPS handover is not supported for NTN in this release of the specification." / "RACH-less handover as specified in 9.2.3.6, in TS 38.321 [6] and in TS 38.331 [12] is supported in NTNs."
- **Figure(s):** —
- **Condition:** TS 38.300 Rel-19 (mirror)
- **Use in paper:** handover model. Implication to argue: without DAPS in NTN there is no dual-active overlap to hide re-keying latency.
- **Status:** SECONDARY (via iTecSpec; primary TOC confirms the clause)

### NTN-02l  (why LEO handover is frequent)
- **Citation:** 3GPP TR 38.821 (Rel-16), §7.3.2.1.4 "Frequent and unavoidable handover"; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.821/s/7.3.2.1.4 (accessed 2026-09-27)
- **Location:** §7.3.2.1.4
- **Quote:** "Satellites in non-GEO orbits move with high speed relative to a fixed position on earth, leading to frequent and unavoidable handover for both stationary and moving UEs." / "It is not anticipated that frequent HO will occur in GEO due to large cell size limiting the impact of UE speed."
- **Figure(s):** — (see NTN-05c for the times)
- **Condition:** LEO vs GEO; TR 38.821 Rel-16 (mirror)
- **Use in paper:** handover-rate model (NTN)
- **Status:** SECONDARY (via iTecSpec; the primary ATIS V16.0.0 window ends before §7)

### NTN-02m  (service continuity as a benefit of time-based CHO)
- **Citation:** 3GPP TR 38.821 (Rel-16), §7.3.2.2.2 "Conditional Handover", Table 7.3.2.2.2-1; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.821/s/7.3.2.2.2 (accessed 2026-09-27)
- **Location:** Table 7.3.2.2.2-1, "Time/Timer-based" row, "Advantages" cell
- **Quote:** "●Can be useful to maintain service continuity if UE loses terrestrial coverage; ●Can enable mandatory HO based on timing;"
- **Figure(s):** —
- **Condition:** Rel-16 study-phase assessment (not normative)
- **Use in paper:** CHO and service-continuity argument
- **Status:** SECONDARY (via iTecSpec)

---

## NTN-03 — TR 38.811 (Rel-15 study): use cases and platform parameters

### NTN-03a  (eHealth vertical)
- **Citation:** as NTN-01k (TR 38.811 V15.3.0, ATIS.3GPP.38.811.V1530)
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.1 "Roles for Non-Terrestrial Networks in 5G system"
- **Quote:** "A role for Non-Terrestrial Network components in the 5G system is expected for the following verticals: transport, Public Safety, Media and Entertainment, eHealth, Energy, Agriculture, Finance, Automotive."
- **Figure(s):** — (names eHealth and Public Safety as NTN verticals)
- **Condition:** Rel-15 study (TR 38.811 V15.3.0)
- **Use in paper:** Introduction/motivation: 3GPP names eHealth as an NTN vertical
- **Status:** VERIFIED

### NTN-03b  (use case: wide-area public safety, satellite)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.2.1, Table 4.2.1-1 "5G use cases for Satellite access networks", row "Wide area public safety"
- **Quote:** "Emergency responders, such as police, fire brigade and medical personnel can exchange messaging and voice services in outdoor conditions anywhere they are and achieve continuity of service whatever mobility scenarios."
- **Figure(s):** —
- **Condition:** Rel-15 study; eMBB use case taken from TR 22.862 (per extraction)
- **Use in paper:** emergency-medical NTN use case
- **Status:** VERIFIED

### NTN-03c  (use case: local-area public safety, satellite)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.2.1, Table 4.2.1-1, row "Local area public safety"
- **Quote:** "Emergency responders, such as police, fire brigade, and medical personnel can set up a tactical cell wherever they need to operate."
- **Figure(s):** —
- **Condition:** Rel-15 study
- **Use in paper:** disaster/field-hospital NTN use case
- **Status:** VERIFIED

### NTN-03d  (use case: regional-area public safety, aerial/HAPS)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.2.1, Table 4.2.1-2 "5G use cases for Aerial access networks", row "Regional area public safety"
- **Quote:** "Emergency responders, such as police, fire brigades, and medical personnel can exchange messaging, voice and video services in indoor/outdoor conditions anywhere they are and whatever mobility scenarios."
- **Figure(s):** —
- **Condition:** Rel-15 study; aerial (HAPS/UAS) access
- **Use in paper:** emergency-medical use case (aerial)
- **Status:** VERIFIED. No row in the reachable text mentions "remote monitoring" or "ambulance". The only health mentions are eHealth (NTN-03a) and "medical personnel" (NTN-03b–d).

### NTN-03e  (platform altitudes)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.5, Table 4.5-1 "Typical characteristics of Airborne or Space-borne vehicles", header + "Altitude" row
- **Quote:** "Characteristics | Geostationary satellites | Non-Geostationary satellites | Airborne platforms" / "Altitude | 35 786 km | Low Earth Orbiting satellites: From 600 km up to 1500 km; Medium Earth Orbiting satellites: From 7000 up to 20000 km | Typically from 8 to 50 km"
- **Figure(s):** GEO 35 786 km; LEO 600–1500 km; MEO 7000–20000 km; airborne 8–50 km
- **Condition:** Rel-15 study, "typical" characteristics
- **Use in paper:** platform classes in the NTN section
- **Status:** VERIFIED

### NTN-03f  (typical elevation, Table 4.5-1)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.5, Table 4.5-1, "Elevation angle (NOTE 1)" row (same text in all three columns)
- **Quote:** "Elevation angle (NOTE 1) | Typically more than 10° for user terminal and more than 5° for gateways"
- **Figure(s):** >10° (user terminal); >5° (gateway)
- **Condition:** Rel-15 study; GEO, non-GEO and airborne. This differs from TR 38.821, which uses 10° for both links (NTN-01c).
- **Use in paper:** elevation assumption; label TR 38.811 delay figures with it, since it differs from TR 38.821's
- **Status:** VERIFIED

### NTN-03g  (typical minimum elevation by system)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.5, Table 4.5-2 "Typical elevation angles in aerial and satellite based systems" (column "Typical minimum Elevation Angle for terminals")
- **Quote:** "Regional GEO | 10 degrees | Addressing regions in lower and medium latitude" / "Aeronautical | 20 degrees | Taking into account aero-dynamic constraints prevents operation at lower angles" / "Vehicles | 15 degrees | Taking into account road conditions, terrain, and vehicle mechanics" / "Non GSO | 10 to 30 degrees | Ensuring service continuity optimising the number of satellites"
- **Figure(s):** Regional GEO 10°; Aeronautical 20°; Vehicles 15°; Non GSO 10–30°. The other rows are International GEO (Trunking) 5°, International (GEO) Maritime 5° and Aerial "In the range of 10 degrees".
- **Condition:** Rel-15 study; terminal minimum elevation
- **Use in paper:** elevation sensitivity for the pass-duration script (vehicle/aeronautical terminals)
- **Status:** VERIFIED

### NTN-03h  (typical beam footprint)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §4.6, Table 4.6-1 "Typical beam foot print size"
- **Quote:** "Attributes | GEO | Non-GEO | Aerial" / "Beam foot print size in diameter | 200 – 1000 km | 100 – 500 km | 5 - 200 km"
- **Figure(s):** GEO 200–1000 km; Non-GEO 100–500 km; Aerial 5–200 km (diameter)
- **Condition:** Rel-15 study, "typical". TR 38.821 later uses a 1000 km LEO maximum (NTN-01h).
- **Use in paper:** cell/beam-size range for the handover-rate model
- **Status:** VERIFIED

### NTN-03i  (reference deployment scenarios D1–D5)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §5.1, Table 5.1-1 "Reference Non-Terrestrial Network Deployment scenarios to be considered" (platform/altitude cells)
- **Quote:** "GEO at 35 786 km" (Deployment-D1, D2) / "Non-GEO down to 600 km" (Deployment-D3, D4) / "UAS between 8 km and 50 km including HAPS" (Deployment-D5)
- **Figure(s):** GEO 35 786 km; non-GEO down to 600 km; UAS/HAPS 8–50 km
- **Condition:** Rel-15 study deployment scenarios. The row label was not captured by the extraction.
- **Use in paper:** scenario mapping to the Rel-15 study
- **Status:** VERIFIED

### NTN-03j  (GEO propagation delays, one-way and RTT)
- **Citation:** as NTN-03a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel15/ATIS.3GPP.38.811.V1530.pdf (accessed 2026-09-27)
- **Location:** §5.3.2.1, Table 5.3.2.1-1 "Propagation delays for GEO satellite at 35786 km" (columns: Elevation angle | Path | D (km) | Time (ms))
- **Quote:** "Bent Pipe satellite | One way delay Gateway-satellite_UE | 81712.6 | 272.375" / "Bent Pipe satellite | Round trip Time Twice | 163425.3 | 544.751" / "Regenerative Satellite | One way delay Satellite -UE | 40586 | 135.286" / "Regenerative Satellite | Round Trip Time Satellite-UE-Satellite | 81172 | 270.572"
- **Figure(s):** GEO bent-pipe one-way 272.375 ms, RTT 544.751 ms; GEO regenerative one-way 135.286 ms, RTT 270.572 ms
- **Condition:** the same table's elevation rows are "UE: 10°" and "GW: 5°" (so not the 10°/10° of TR 38.821, whose Scenario A RTD is 541.46 ms). TR 38.811 V15.3.0. Bent pipe = transparent.
- **Use in paper:** GEO one-way delay (not given in TR 38.821)
- **Status:** VERIFIED

### NTN-03k  (LEO 600 km propagation delays, one-way and RTT)
- **Citation:** 3GPP TR 38.811 (Rel-15), §5.3.4.1, Table 5.3.4.1-1 "Propagation delays for different NGSO satellites (altitude and payload types)"; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.811/s/5.3.4.1 (accessed 2026-09-27)
- **Location:** Table 5.3.4.1-1, "LEO at 600 km" columns (Distance D (km) | Delay (ms))
- **Quote:** "Bent pipe satellite | One way delay | 4261.2 | 14.204" / "Bent pipe satellite | Round Trip Delay | 8522.5 | 28.408" / "Regenerative satellite | One way delay | 1932.24 | 6.44" / "Regenerative satellite | Round Trip Delay | 3864.48 | 12.88"
- **Figure(s):** LEO 600 km bent-pipe one-way 14.204 ms, RTD 28.408 ms; regenerative one-way 6.44 ms, RTD 12.88 ms
- **Condition:** table rows "UE: 10°" and "GW: 5°". The clause text reads: "Gateway is set at 5° (TBC) elevation angle, and terminal can be set at various elevation angles, but we consider that the reference case is 10° elevation angle." The mirror renders the UE-leg delay as "6,440" (comma), next to "6.44" in the regenerative row. TR 38.811 Rel-15. The 1500 km and MEO 10000 km columns are also present.
- **Use in paper:** LEO one-way delay. Do not mix with TR 38.821's 25.77 ms transparent RTD (NTN-01e): the two documents state different elevation assumptions (GW 5°/UE 10° here, 10°/10° in TR 38.821).
- **Status:** SECONDARY (via iTecSpec rendering of 3GPP TR 38.811 §5.3.4.1; the primary ATIS V15.3.0 window ends around §5.3.3). Two extractions matched.

### NTN-03l  (synthesis table: max one-way delay and differential delay)
- **Citation:** 3GPP TR 38.811 (Rel-15), §5.3.5, Table 5.3.5-1 "Summary of Doppler shift, Doppler Shift variation and propagation delay for LEO at 600 km, GEO and HAPS"; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.811/s/5.3.5 (accessed 2026-09-27)
- **Location:** Table 5.3.5-1 (columns D1 | D2 | D3 | D4 | D5 | Cellular (10 km Radius))
- **Quote:** "Max One way Propagation delay (ms) | Bentpipe: 272.37 ms gNB on board: 135.28 ms | 272.37 ms | 14.204 ms | 14.204 ms | 1.526 ms | 0.03333 ms" / "Max Differential delay (ms) | … | 4.44 (between Edge of satellite coverage and Nadir)" [D3 cell]
- **Figure(s):** max one-way delay: GEO (D1, D2) 272.37 ms bent pipe / 135.28 ms gNB on board (D1); LEO 600 km (D3, D4) 14.204 ms; airborne (D5) 1.526 ms; terrestrial 10 km cell 0.03333 ms. Max differential delay at LEO 600 km: 4.44 ms (edge of coverage vs nadir).
- **Condition:** D3/D4 = "Non-GEO down to 600 km"; D5 = "Airborne vehicle up to 20 km"; TR 38.811 Rel-15. The "…" marks omitted D1/D2 cells, which read "16 (between Edge of satellite coverage and Nadir)".
- **Use in paper:** one-way-delay row of the NTN budget table
- **Status:** SECONDARY (via iTecSpec rendering of 3GPP TR 38.811 §5.3.5; the primary ATIS window ends around §5.3.3)

---

## NTN-04 — TR 38.913 deployment scenarios: ISD and UE speed (ETSI TR 138 913 V19.0.0, Rel-19)

Common citation: ETSI TR 138 913 V19.0.0 (2025-10), "5G; Study on scenarios and requirements for next generation access
technologies (3GPP TR 38.913 version 19.0.0 Release 19)." https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf
(latest per 3GPP portal: 19.0.0, 2025-10-14).

### NTN-04a  (Indoor hotspot)
- **Citation:** ETSI TR 138 913 V19.0.0 (2025-10) / 3GPP TR 38.913 V19.0.0 (Rel-19)
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.1 "Indoor hotspot", Table 6.1.1-1, ISD row and "User distribution and UE speed" row (p. 10)
- **Quote:** "20m (Equivalent to 12TRxPs per 120m x 50m)" / "100% Indoor, 3km/h, 10 users per TRxP"
- **Figure(s):** ISD 20 m; UE speed 3 km/h (100 % indoor)
- **Condition:** Indoor hotspot; carrier "Around 30 GHz or Around 70 GHz or Around 4 GHz"; layout "Single layer: - Indoor floor (Open office)"; Rel-19 V19.0.0
- **Use in paper:** in-hospital hotspot mobility baseline (terrestrial handover-rate model)
- **Status:** VERIFIED

### NTN-04b  (Dense urban)
- **Citation:** as NTN-04a
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.2 "Dense urban", Table 6.1.2-1, ISD row and "User distribution and UE speed" row (p. 11)
- **Quote:** "Macro layer: 200m / Micro layer: 3micro TRxPs per macro TRxP, All micro TRxPs are all outdoor" / "80% indoor (3km/h), 20% outdoor (30km/h)"
- **Figure(s):** macro ISD 200 m (3 micro TRxPs per macro TRxP); UE speed 3 km/h indoor (80 %), 30 km/h outdoor (20 %)
- **Condition:** Dense urban, two layers (carrier "Around 4GHz + Around 30GHz (two layers)"); Rel-19 V19.0.0. The speed text is part of a longer cell that begins "Step1: Uniform/macro TRxP, 10 users per TRxP / Step2: …".
- **Use in paper:** urban ambulance / pedestrian handover-rate model
- **Status:** VERIFIED

### NTN-04c  (Rural)
- **Citation:** as NTN-04a
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.3 "Rural", Table 6.1.3-1, ISD row and "User distribution and UE speed" row (p. 12)
- **Quote:** "ISD 1: 1732m / ISD 2: 5000m" / "50% outdoor vehicles (120km/h) and 50% indoor (3km/h), 10 users per TRxP"
- **Figure(s):** ISD 1732 m (ISD 1) or 5000 m (ISD 2); UE speed 120 km/h (50 % vehicles), 3 km/h (50 % indoor)
- **Condition:** Rural, single-layer hex grid; carrier per extraction "Around 700MHz or Around 4GHz (for ISD 1)" (the cell may continue); Rel-19 V19.0.0
- **Use in paper:** rural ambulance handover-rate model
- **Status:** VERIFIED

### NTN-04d  (Urban macro)
- **Citation:** as NTN-04a
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.4 "Urban macro", Table 6.1.4-1, ISD row and "User distribution and UE speed" row (p. 13)
- **Quote:** "500m" / "20% Outdoor in cars: 30km/h, 80% Indoor in houses: 3km/h / 10 users per TRxP"
- **Figure(s):** ISD 500 m; UE speed 30 km/h (20 % outdoor in cars), 3 km/h (80 % indoor)
- **Condition:** Urban macro, single-layer hex grid; carrier "Around 2 GHz or Around 4 GHz or Around 30 GHz"; Rel-19 V19.0.0
- **Use in paper:** urban macro handover-rate model
- **Status:** VERIFIED

### NTN-04e  (High speed — train)
- **Citation:** as NTN-04a
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.5 "High speed", Table 6.1.5-1, ISD row and "User distribution and UE speed" row (p. 14)
- **Quote:** "Around 4GHz: ISD 1732m between RRH sites, two TRxPs per RRH site." / "1732m between BBU sites, 3 RRH sites connected to 1 BBU, one TRxP per RRH site" [Around-30GHz part] / "100% of users in train" / "Maximum mobility speed: 500km/h"
- **Figure(s):** ISD 1732 m (between RRH sites at ~4 GHz; between BBU sites at ~30 GHz); max UE speed 500 km/h
- **Condition:** High-speed train; layout "Macro only: - Around 4GHz: Dedicated linear deployment along railway line"; Rel-19 V19.0.0
- **Use in paper:** high-speed-train handover-rate model (worst terrestrial case)
- **Status:** VERIFIED

### NTN-04f  (Highway — ISD and user distribution)
- **Citation:** as NTN-04a
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.8 "Highway Scenario", Table 6.1.8-1, "ISD" row and "User distribution and UE speed NOTE5" row (p. 17)
- **Quote:** "Macro cell: ISD = 1732m, 500m(Optional) / Inter-RSU distance = 50m or 100m" / "100% in vehicles" / "Average inter-vehicle distance (between two vehicles' center) in the same lane is 0.5sec or 1sec * average vehicle speed (average speed: 100-300km/h)"
- **Figure(s):** macro ISD 1732 m (500 m optional); inter-RSU distance 50 m or 100 m; average vehicle speed 100–300 km/h
- **Condition:** Highway (V2X-oriented scenario); Rel-19 V19.0.0
- **Use in paper:** highway ambulance handover-rate model
- **Status:** VERIFIED

### NTN-04g  (Highway — speeds in the traffic-model row)
- **Citation:** as NTN-04a
- **Fetched URL:** https://www.etsi.org/deliver/etsi_tr/138900_138999/138913/19.00.00_60/tr_138913v190000p.pdf (accessed 2026-09-27)
- **Location:** §6.1.8, Table 6.1.8-1, "Traffic model NOTE5" row (p. 17)
- **Quote:** "50 messagesNOTE6 per 1 second with absolute average speed of either - 100-250 km/h (relative speed: 200 – 500km/h), or - 30 km/h"
- **Figure(s):** absolute average speed 100–250 km/h (relative 200–500 km/h) or 30 km/h
- **Condition:** these speeds sit in the **traffic-model** row, not the UE-speed row (NTN-04f gives 100–300 km/h there); Rel-19 V19.0.0
- **Use in paper:** cite only with this row distinction
- **Status:** VERIFIED

---

## NTN-05 — LEO visibility time / pass duration

### NTN-05a  (satellite in view ≈ 20 min, 2-hour orbit)
- **Citation:** 3GPP TR 38.811 (Rel-15), §7.3.2.1.1 "Problem statement" (under §7.3.2.1 "Hand-Over and paging"); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.811/s/7.3.2.1.1 (accessed 2026-09-27)
- **Location:** §7.3.2.1.1
- **Quote:** "As an example, on a 2-hour orbit, a LEO satellite is in view of a stationary UE from horizon to horizon for about 20 minutes."
- **Figure(s):** about 20 minutes
- **Condition:** **2-hour orbital period, horizon to horizon, stationary UE; no altitude or elevation mask stated.** This is **not** a 600 km figure and not at a 10° mask.
- **Use in paper:** order-of-magnitude anchor only. The 600 km, 10°-mask pass duration must come from the geometry script, which can be sanity-checked against this entry.
- **Status:** SECONDARY (via iTecSpec rendering of 3GPP TR 38.811 §7.3.2.1.1). The primary ATIS V15.3.0 and NCU V15.1.0 PDFs were fetched, but their windows end before §7. An exact-phrase WebSearch found no other copy.

### NTN-05b  (time within a beam: a few minutes)
- **Citation:** as NTN-05a
- **Fetched URL:** https://itecspec.com/3gpp/38.811/s/7.3.2.1.1 (accessed 2026-09-27)
- **Location:** §7.3.2.1.1
- **Quote:** "Since each LEO satellite may have many beams, the time such a UE stays within a beam is typically for only a few minutes."
- **Figure(s):** "only a few minutes" (not quantified further)
- **Condition:** generic LEO, multi-beam; Rel-15
- **Use in paper:** beam-switch frequency (qualitative)
- **Status:** SECONDARY (via iTecSpec)

### NTN-05c  (max time a UE stays in a LEO cell: time to HO)
- **Citation:** 3GPP TR 38.821 (Rel-16), §7.3.2.1.4, Table 7.3.2.1.4-1; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.821/s/7.3.2.1.4 (accessed 2026-09-27)
- **Location:** §7.3.2.1.4, running text + Table 7.3.2.1.4-1
- **Quote:** "Neglecting UE movement, a UE served by an NTN LEO cell of diameter 50 km and 1000 km may remained connected for a maximum of 6.61 seconds and 132.38 seconds respectively due to satellite movement." / "1000 (upper bound) | Neglected | 7.56 (NOTE 1) | 132.28"
- **Figure(s):** 6.61 s (50 km cell); 132.38 s in the text but **132.28 s in the table cell** (1000 km cell). The table also gives 6.49/6.74/6.33/6.92 s (50 km; UE ±500, ±1200 km/h) and 129.89/134.75/126.69/138.38 s (1000 km; same UE speeds).
- **Condition:** cell dwell time, **not** a satellite pass/visibility time. It assumes satellite speed 7.56 km/s with the unresolved altitude caveat (NOTE 1, see NTN-01i). The source text calls it "Substituting reference values from 4.2-2 and 7.1-1 into the above equation". Rel-16 (mirror).
- **Use in paper:** upper bound on cell-level (L3) handover interval in LEO. The 132.28 vs 132.38 mismatch must be resolved against the primary before citing.
- **Status:** SECONDARY (via iTecSpec). The mismatch is present in the mirror's rendering and was not checked against the primary because its window ends before §7.

### NTN-05d  ("visibility time" named without a value)
- **Citation:** as NTN-01a
- **Fetched URL:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.38.821.V1600.pdf (accessed 2026-09-27)
- **Location:** §4.2, Table 4.2-2, NOTE 1 (attached to the "Earth-fixed beams" entry)
- **Quote:** "Each satellite has the capability to steer beams towards fixed points on earth using beamforming techniques. This is applicable for a period of time corresponding to the visibility time of the satellite"
- **Figure(s):** — (no value)
- **Condition:** LEO steerable (earth-fixed) beams, Scenarios C1/D1; TR 38.821 V16.0.0
- **Use in paper:** states that earth-fixed service is bounded by satellite visibility time
- **Status:** VERIFIED (qualitative; no figure)

### NTN-05e  (600 km-specific pass duration)
- **Citation:** —
- **Fetched URL:** —
- **Location:** —
- **Quote:** —
- **Figure(s):** —
- **Condition:** LEO 600 km, ground UE
- **Use in paper:** compute from geometry (NTN-01a/c/d, NTN-01j) in the model scripts
- **Status:** NOT-FOUND. No 3GPP statement giving the visibility/pass time of a **600 km** satellite was found. Searched:
  (1) TR 38.821 via the ATIS V16.0.0 PDF (Table 4.2-2 and all text to about §6.1.4.2; a targeted search for visibility time in minutes/seconds found none), plus iTecSpec clauses 4.2, 7.1, 7.3.1, 7.3.1.2, 7.3.2.1.4, 7.3.2.2.2, 7.3.2.3, 8.7.1, 8.7.2 and 8.7.2.1;
  (2) TR 38.811 via the ATIS V15.3.0 PDF (to about §5.3.3) and the NCU V15.1.0 PDF (to §5.3.2.3), plus iTecSpec clauses 5.3.4, 5.3.4.1, 5.3.4.3, 5.3.5, 7, 7.3.2.1, 7.3.2.1.1–7.3.2.1.3 and 7.3.3. Only the 2-hour-orbit statement exists (NTN-05a);
  (3) TS 38.300 §16.14 via the TOCs of ETSI V19.3.0, V18.10.0 and V17.17.0, plus iTecSpec clauses 16.14.1, 16.14.2.2, 16.14.3.1, 16.14.3.2.1–16.14.3.2.3 and 16.14.4.1–16.14.4.3;
  (4) the 3GPP NTN overview web page;
  (5) WebSearch with the phrases "visibility time", "visible … minutes", "few minutes".
  Clauses not reached: most of TR 38.821 §§5–6 and §7.3.1.x beyond 7.3.1.2, and TR 38.811 §7.3.2.2–7.3.2.4.

---

## NTN-06 — satellite switch with re-synchronisation (Rel-18+); feeder-link / satellite-switch interval

### NTN-06a  (release placement, primary TOC evidence)
- **Citation:** ETSI TS 138 300 V19.3.0 (2026-08), V18.10.0 (2026-08) and V17.17.0 (2026-08), "5G; NR; NR and NG-RAN Overall description; Stage-2 (3GPP TS 38.300 version 19.3.0 Release 19 / 18.10.0 Release 18 / 17.17.0 Release 17)."
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/19.03.00_60/ts_138300v190300p.pdf ; https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/18.10.00_60/ts_138300v181000p.pdf ; https://www.etsi.org/deliver/etsi_ts/138300_138399/138300/17.17.00_60/ts_138300v171700p.pdf (accessed 2026-09-27)
- **Location:** table of contents, clause 16.14
- **Quote:** V19.3.0: "16.14.3.2.3 Satellite switch with re-synchronization ... 239" / V18.10.0: "16.14.3.2.3 Satellite switch with re-synchronization" (p. 214) / V17.17.0: TOC goes "16.14.3.2.2 Conditional Handover — 180" → "16.14.3.3 Measurements — 181" (no 16.14.3.2.3)
- **Figure(s):** — (the clause exists in Rel-18 and Rel-19 and is absent in Rel-17)
- **Condition:** TS 38.300 Rel-17/18/19. Newer versions V19.4.0 and V18.11.0 (uploaded 2026-09-25) were not fetched.
- **Use in paper:** release attribution of satellite switch with re-sync (Rel-18)
- **Status:** VERIFIED (TOC headings only; clause bodies below are SECONDARY)

### NTN-06b  (scope of satellite switch with re-sync)
- **Citation:** 3GPP TS 38.300 Rel-19, §16.14.3.2.3 "Satellite switch with re-synchronization" (p. 239 in the V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.3 (accessed 2026-09-27)
- **Location:** §16.14.3.2.3, first sentence
- **Quote:** "For transparent payload, upon both hard and soft satellite switch over in the quasi-Earth fixed scenario with the same SSB frequency and the same gNB, the satellite switch with re-synchronization procedure is supported."
- **Figure(s):** —
- **Condition:** **transparent payload, quasi-Earth-fixed cells, same SSB frequency and same gNB**; Rel-18+ (mirror labelled Rel-19)
- **Use in paper:** mobility-security budget. Implication to check (not stated here): same gNB and no L3 handover may mean no AS re-keying; verify against TS 33.501 / TS 38.331.
- **Status:** SECONDARY (via iTecSpec; primary TOC confirms the clause, NTN-06a)

### NTN-06c  (same PCI, no L3 mobility)
- **Citation:** as NTN-06b
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.3 (accessed 2026-09-27)
- **Location:** §16.14.3.2.3, second sentence
- **Quote:** "The satellite switch with re-sync avoids a L3 mobility for UEs in the cell by maintaining the same PCI on the geographical area covered by quasi-Earth fixed beam."
- **Figure(s):** —
- **Condition:** as NTN-06b
- **Use in paper:** mobility-security budget: satellite switches that do not count as handovers
- **Status:** SECONDARY (via iTecSpec)

### NTN-06d  (soft satellite switch)
- **Citation:** as NTN-06b
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.3 (accessed 2026-09-27)
- **Location:** §16.14.3.2.3
- **Quote:** "For soft satellite switch over, the UE can start synchronizing with the target satellite before the source satellite ends to serve the cell. It is not required for the UE to be connected to source satellite when the UE switches to target satellite."
- **Figure(s):** —
- **Condition:** soft satellite switch; Rel-18+ (mirror)
- **Use in paper:** interruption model (soft case)
- **Status:** SECONDARY (via iTecSpec)

### NTN-06e  (hard satellite switch; coexistence with CHO)
- **Citation:** as NTN-06b
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.3 (accessed 2026-09-27)
- **Location:** §16.14.3.2.3
- **Quote:** "For hard satellite switch over, the UE can only start synchronizing with the target satellite after the source satellite ends to serve the cell. When both CHO and Satellite switch with re-synchronization are configured, it is up to UE implementation which procedure to initiate, if both of them are triggered simultaneously."
- **Figure(s):** — (no interruption duration stated)
- **Condition:** hard satellite switch; Rel-18+ (mirror)
- **Use in paper:** interruption model (hard case). Implication to check: when both are triggered, the UE picks CHO or re-sync, so whether a handover (and new keys) occurs may depend on the UE.
- **Status:** SECONDARY (via iTecSpec)

### NTN-06f  (re-sync access via PDCCH order)
- **Citation:** as NTN-06b
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.3.2.3 (accessed 2026-09-27)
- **Location:** §16.14.3.2.3, last sentence
- **Quote:** "For the re-synchronization to the target satellite, random access can be triggered by a PDCCH order via the target satellite."
- **Figure(s):** —
- **Condition:** Rel-18+ (mirror)
- **Use in paper:** signalling cost of a satellite switch (random access, no RRC reconfiguration)
- **Status:** SECONDARY (via iTecSpec)

### NTN-06g  (Rel-18 work item lists the feature)
- **Citation:** as NTN-02i (3GPP NTN overview page)
- **Fetched URL:** https://www.3gpp.org/technologies/ntn-overview (accessed 2026-09-27)
- **Location:** Release 18 section
- **Quote:** "The WG RAN2 led Release 18 WI "NR NTN (Non-Terrestrial Networks) enhancements" (NR_NTN_enh)" / "satellite switch with re-sync"
- **Figure(s):** —
- **Condition:** Rel-18 NR_NTN_enh; 3GPP-authored overview (not normative)
- **Use in paper:** release attribution (with NTN-06a)
- **Status:** VERIFIED (3GPP-authored web overview)

### NTN-06h  (timing of feeder-link switch over is a network decision)
- **Citation:** 3GPP TS 38.300 Rel-19, §16.14.4.3 "Procedures" (p. 240 in the V19.3.0 TOC); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.300/s/16.14.4.3 (accessed 2026-09-27)
- **Location:** §16.14.4.3
- **Quote:** "The NTN Control function (see Annex B.4) determines the point in time when the feeder link switch over is performed. The transfer of the affected UE(s)' at feeder link switch over is performed by means of handover or TNL functionality, and it depends on the gNBs' implementation and configuration information provided to the gNBs by the NTN Control function."
- **Figure(s):** — (no interval specified)
- **Condition:** TS 38.300 Rel-19 (mirror)
- **Use in paper:** the feeder-link switch interval is set by the deployment, not by 3GPP, so the paper must parameterise it
- **Status:** SECONDARY (via iTecSpec; primary TOC confirms the clause)

### NTN-06i  (why feeder-link switches occur)
- **Citation:** 3GPP TR 38.821 (Rel-16), §8.7.1 "Principles" (under §8.7 "Feeder link switch over"); rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.821/s/8.7.1 (accessed 2026-09-27)
- **Location:** §8.7.1
- **Quote:** "During NTN operation, it may become necessary to switch the feeder link (SRI) between different NTN GWs toward the same satellite." / "This may be due to e.g. maintenance, traffic offloading, or (for LEO) due to the satellite moving out of visibility with respect to the current NTN GW."
- **Figure(s):** — (no interval)
- **Condition:** Rel-16 study (mirror); LEO feeder links
- **Use in paper:** feeder-link switch as a recurring LEO event
- **Status:** SECONDARY (via iTecSpec; the primary ATIS window ends before §8. Its TOC lists "8.7 Feeder link switch over" at p. 122.)

### NTN-06j  (predictable switchover; soft vs hard)
- **Citation:** 3GPP TR 38.821 (Rel-16), §8.7.2.1 "Transparent payload case"; rendered by iTecSpec.
- **Fetched URL:** https://itecspec.com/3gpp/38.821/s/8.7.2.1 (accessed 2026-09-27)
- **Location:** §8.7.2.1
- **Quote:** "The switchover may be predictable (e.g. based on the LEO satellite ephemeris information and NTN GWs location) or event-triggered (e.g. for maintenance)." / "Alternatively, a hard switch procedure could be considered to allow for no simultaneous connectivity between satellite and the 2 NTN-GWs."
- **Figure(s):** —
- **Condition:** transparent payload; Rel-16 study (mirror)
- **Use in paper:** predictability means security material can be pre-provisioned before a feeder-link switch
- **Status:** SECONDARY (via iTecSpec)

### NTN-06k  (numeric feeder-link / satellite-switch interval)
- **Citation:** —
- **Fetched URL:** —
- **Location:** —
- **Quote:** —
- **Figure(s):** —
- **Condition:** —
- **Use in paper:** parameterise from geometry or deployment (see NTN-05e)
- **Status:** NOT-FOUND. No numeric interval between feeder-link switches or satellite switches was found in: TS 38.300 §16.14.3.2.3 and §16.14.4.1–16.14.4.3 (iTecSpec Rel-19; primary TOCs V17.17.0, V18.10.0, V19.3.0); TR 38.821 §§7.3.2.3, 8.7.1, 8.7.2 and 8.7.2.1 (iTecSpec; ATIS V16.0.0 TOC); and the 3GPP NTN overview page. TS 38.300 §16.14.4.3 leaves the timing to the NTN Control function (NTN-06h).
