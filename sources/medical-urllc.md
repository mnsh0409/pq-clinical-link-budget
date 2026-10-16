# medical-urllc.md — 3GPP / IEEE / ITU medical and tactile requirements

Cluster file for the source ledger.
Rules: `README.md`. All entries collected **2026-09-27** (access date) with
WebSearch/WebFetch only. Table rows are quoted cell-by-cell, cells joined with " | " in the
source's column order; column headers are listed in the Condition line.

**Mirror caveat (read before citing TR 22.826).** ETSI does not publish TR 22.826
(`etsi.org/deliver/etsi_tr/122800_122899/122826/` returns 404), and 3gpp.org only has zipped
.docx files that WebFetch cannot open. Every TR 22.826 quote below comes from the tech-invite.com
HTML reproduction of the TR. It is a verbatim mirror, not the 3GPP host, so those entries are
tagged SECONDARY. The central robotic-surgery and robotic-diagnosis KPIs were adopted
normatively into TS 22.104 Table 5.2-1, and those rows are VERIFIED from the ETSI PDF (MED-04a–c).
Cite TS 22.104 for those numbers.

## Status index

| id | what | status |
|---|---|---|
| MED-01a–o | TR 22.826 robotic aided surgery (local, 5.2.4) + remote telesurgery (5.3.3) + latency budget (5.2.1) | SECONDARY (tech-invite mirror) |
| MED-02a–e | TR 22.826 tele-ultrasound (5.3.2) + mobile specialist practice (5.3.4) | SECONDARY (tech-invite mirror) |
| MED-03a–h | TR 22.826 cardiac telemetry in/out of hospital (5.4.2, 5.5.3), ambulance (5.5.2) | SECONDARY (tech-invite mirror) |
| MED-04a–d | TS 22.104 V19.2.0 Table 5.2-1 medical rows | VERIFIED |
| MED-05a | TS 22.261 V19.14.0 end-to-end latency definition | VERIFIED |
| MED-05b | TS 22.261 Table 7.2.2-1 rows | NOT-FOUND |
| MED-05c | TS 22.261 Rel-20 clause 7.2.2 (no table; points to 22.104/22.186/22.289) | SECONDARY (itecspec mirror) |
| MED-05d–e | TS 22.261 Rel-20 Table 7.11-1 "Remote control robot" haptic row + NOTE 2 (IEEE 1918.1) | SECONDARY (itecspec mirror) |
| MED-06a | IEEE 1918.1-2024: year and scope | VERIFIED (no latency figure on the IEEE pages) |
| MED-06b–d | IEEE 1918.1 latency figures | SECONDARY (via Holland et al., Proc. IEEE 2019) |
| MED-07a–f | ITU-T Tech Watch "The Tactile Internet" (Aug 2014) | VERIFIED |
| MED-08a–f | ITU-R M.2160-0 (11/2023) | VERIFIED |
| MED-09a–d | 5G telesurgery clinical reports (Tian 2020; Ye 2026) | VERIFIED |

---

## MED-01 — TR 22.826 robotic-aided surgery / telesurgery

Common citation for MED-01/02/03: 3GPP, "Study on communication services for critical medical
applications," TR 22.826 V17.2.0 (Release 17). The 3GPP portal lists 17.2.0 as the latest version,
"uploaded 2021-04-02", status "Under change control". The metadata page
https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3546
was fetched 2026-09-27.

### MED-01a  (local robotic aided surgery: stereoscopic uncompressed 8K video row)
- **Citation:** 3GPP TR 22.826 V17.2.0 (Rel-17), 2021, clause 5.2.4. Accessed 2026-09-27.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html (page header "Word version: 17.2.0")
- **Location:** 5.2.4 "Robotic Aided Surgery" → 5.2.4.6 "Potential New Requirements needed to support the use case" (mirror page marker p. 27). The mirror shows no "Table x-y" caption for this KPI table.
- **Quote:** "Stereoscopic uncompressed 8K (7680x4320 pixels) 120 fps HDR 10bits real-time video stream | >99.99999 | >1 year | <2 ms | 240 Gbits/s | UE to Network; Network to UE | ~1500 - ~9000 (note 3) | ~8ms | stationary | 1 | 100"
- **Figure(s):** availability >99.99999 (%); MTBF >1 year; end-to-end latency max <2 ms; bit rate 240 Gbits/s; message ~1500 - ~9000 bytes; survival time ~8ms; # of active UEs 1; service area 100 (m2)
- **Condition:** Rel-17 study (not normative). Static-local operating room, the TR's "RAKT" surgery scenario ("Typical RAKT duration is close to four hours"). 5.2.4.3 states "the surgeon at his console sends commands through his hands and feet movements to the robot over the 5G non-public network". Columns in order: Communication service availability: target value in % | Communication service reliability: Mean Time Between Failure | End-to-end latency: maximum | Bit rate | Direction | Message Size [byte] | Survival time | UE speed | # of active UEs | Service Area [m2]. End-to-end latency is one-way (TR clause 3 definition, MED-01o). In the mirror's text the last two cells render as "1100" (UEs = 1, area = 100); one extraction split them this way.
- **Use in paper:** upper bound of the clinical video stream (per-byte AEAD/PQC overhead scale); 2 ms one-way budget per link.
- **Status:** SECONDARY (via tech-invite.com verbatim HTML mirror of 3GPP TR 22.826 V17.2.0; primary .zip on 3gpp.org not openable; ETSI TR 122 826 → 404)

### MED-01b  (local robotic aided surgery: stereoscopic 4K lossless-compressed video row)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html
- **Location:** 5.2.4.6 KPI table (p. 27 marker), second row; NOTE 1 and NOTE 2 under the table.
- **Quote:** "Stereoscopic 4K (3840x2160 pixels) 120 fps HDR 10bits real-time video stream with lossless compression (note 1) | >99.99999 | >1 year | <2 ms | 24 Gbits/s (note 2) | UE to Network; Network to UE | ~1500 - ~9000 (note 3) | ~8ms | stationary | 1 | 100"
- **Figure(s):** >99.99999 (%); >1 year; <2 ms; 24 Gbits/s; ~8ms survival time
- **Condition:** as MED-01a. NOTE 1: "This line provides alternative KPIs that are still acceptable". NOTE 2: "An average compression ratio of 2.5 has been considered when applying a lossless compression algorithm". NOTE 3 (MTU): "MTU size of 1500 bytes is not generally suitable to gigabits connections as it induces many interruptions and loads on CPUs."
- **Use in paper:** "acceptable alternative" video rate for the budget; packet-size range 1500–9000 B for per-packet overhead.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01c  (local robotic aided surgery: video to additional displays, Network to UEs)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html
- **Location:** 5.2.4.6 KPI table (p. 27 marker), third row.
- **Quote:** "Uncompressed 8K (7680x4320 pixels) 120 fps HDR 10bits real-time video stream | >99.99999 | >1 year | <50 ms | 120 Gbits/s | Network to UEs | ~1500 - ~9000 (note 3) | ~8ms | Stationary | <10 | 100"
- **Figure(s):** <50 ms; 120 Gbits/s; <10 active UEs
- **Condition:** as MED-01a. Downlink to up to 10 display UEs in the operating room. The mirror renders the last two cells as "<10100" (UEs <10, area 100). The 4K lossless alternative row for this stream reads "12 Gbits/s (note 2)" with <50 ms (not quoted separately).
- **Use in paper:** relaxed-latency display stream (contrast with the 2 ms surgeon-console stream).
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01d  (local robotic aided surgery: motion-control data stream rows)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html
- **Location:** 5.2.4.6 KPI table (p. 27 marker), rows 5–6.
- **Quote:** "Motion control data stream | >99.999999 | >10 year | <2 ms | 2 Mbits/s | UE to Network | ~250 | ~1 ms | Stationary | 1 | 100" / "Motion control data stream | >99.999999 | >10 year | <2 ms | 16 Mbits/s | Network to UE | ~2000 | ~1 ms | Stationary | 1 | 100"
- **Figure(s):** availability >99.999999 (%); MTBF >10 year; <2 ms; 2 Mbits/s UL with ~250-byte messages; 16 Mbits/s DL with ~2000-byte messages; survival time ~1 ms
- **Condition:** as MED-01a. This table has no transfer-interval column (confirmed by a second extraction). The TS 22.104 version of these rows gives the transfer interval as 1 ms (MED-04a).
- **Use in paper:** per-message authentication budget (250 B / 2000 B payloads at a 1 ms cadence); sets the 10^-8 unavailability target.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01e  (local robotic aided surgery: haptic feedback data stream rows)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html
- **Location:** 5.2.4.6 KPI table (p. 27 marker), rows 7–8.
- **Quote:** "Haptic feedback data stream | >99.999999 | >10 year | <2 ms | 16 Mbits/s | UE to Network | ~2000 | ~1 ms | Stationary | 1 | 100" / "Haptic feedback data stream | >99.999999 | >10 year | <2 ms | 2 Mbits/s | Network to UE | ~250 | ~1 ms | stationary | 1 | 100"
- **Figure(s):** >99.999999 (%); >10 year; <2 ms; 16 Mbits/s UL (~2000 B); 2 Mbits/s DL (~250 B); survival ~1 ms
- **Condition:** as MED-01a. Direction is from the 3GPP UE perspective (robot/console UEs).
- **Use in paper:** haptic channel data rate and message size for the security-overhead budget.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01f  (haptic update rate ~1000 Hz)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html
- **Location:** 5.2.4.1.1 "General" (under 5.2.4 Robotic Aided Surgery).
- **Quote:** "[…] tactile sensing has about 400 Hz bandwidth, where bandwidth refers to the frequency of which the stimuli can be sensed. […] This is why in general haptic feedback systems operate at frequencies around 1000 Hz."
- **Figure(s):** tactile sensing about 400 Hz bandwidth; haptic feedback systems around 1000 Hz
- **Condition:** Descriptive (general haptics), not a KPI-table value. The two sentences are not adjacent. A verification extraction shows the text between them: "This rate naturally applies to the update of all information used in the generation of the haptic feedback, e.g. instruments velocity, position …". The capitalisation at the start of the 400 Hz sentence varied between extractions, hence the leading "[…]".
- **Use in paper:** haptic packet rate, which sets the number of per-packet MAC/AEAD operations per second.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01g  (sensor return messages: 50 bytes at 1 kHz)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_c.html
- **Location:** 5.2.4.1.1 "General" (list item).
- **Quote:** "Sensors sampling velocity, forces, positions, … at the very same time and returning that information to the surgeon console, in 50 bytes messages at the rate of 1 kHz"
- **Figure(s):** 50 bytes messages; 1 kHz
- **Condition:** list item describing the robot-to-console feedback flow. The "…" is in the source text. A companion item reads "The surgeon console periodically sending a set of points to actuators in 50 bytes messages".
- **Use in paper:** smallest clinical packet, where the relative cost of per-packet tag/IV overhead is highest.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01h  (2 ms end-to-end constraint per radio link)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_b.html (header "Word version: 17.2.0")
- **Location:** 5.2.1 "Description of Modality" → "Latency aspects" → "Teleoperation Systems" (mirror p. 14; sub-clause numbers are truncated in the mirror rendering).
- **Quote:** "Also, note that surgeons may be able to adapt to the overall teleoperation system latency through training under a constant delay. This leaves us therefore with roughly 2 ms end-to-end latency constraint on each of the four radio links involved in the robotic sub-systems connectivity."
- **Figure(s):** roughly 2 ms end-to-end latency per radio link; four radio links
- **Condition:** static-local (in-hospital) teleoperation loop, derived by the TR.
- **Use in paper:** the per-link latency ceiling that any security processing (handshake excluded, per-packet crypto included) must fit inside.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01i  (outer control loop 50 ms; 300 ms tolerable teleoperation latency)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_b.html
- **Location:** 5.2.1 → "Latency aspects" → "Teleoperation Systems" (p. 14 marker).
- **Quote:** "The maximum tolerable teleoperation system latency, up to which surgeons can still improve their performance through repeating the same simple task over and over again has been found to be around 300 ms."
- **Figure(s):** around 300 ms
- **Condition:** literature-derived human-factors bound quoted by the TR. The same clause states "This allows to derive an overall outer control loop teleoperation system latency of 50 ms using principles and error targets explained in clause" (clause cross-reference missing in the mirror).
- **Use in paper:** context bound (human tolerance) vs. network KPI.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01j  (imaging: 2 ms transport budget at 120 fps)
- **Citation:** as MED-01a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_b.html
- **Location:** 5.2.1 → "Latency aspects" → "Imaging Systems" (p. 13 marker).
- **Quote:** "Under the same assumption as before (120fps), this leaves a budget of 2ms for the transport of packets through 5G System and 6ms for application processing."
- **Figure(s):** 2ms transport through 5G System; 6ms application processing; 120fps
- **Condition:** imaging chain at 120 fps. The same clause states "If we consider 120fps, latency contribution for generation plus display would be 8ms."
- **Use in paper:** splits the video latency budget into transport and processing (security processing competes with the 6 ms application share).
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01k  (remote robotic telesurgery: video rows)
- **Citation:** as MED-01a, clause 5.3.3 "Communication QoS requirement for robotic telesurgery".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_e.html (header "Word version: 17.2.0")
- **Location:** 5.3.3 → "Potential New Requirements needed to support the use case" (mirror p. 36 marker), rows 1–2.
- **Quote:** "Stereoscopic 4K 60 fps HDR 10bits frame packed real time video (loss less compressed) | 99.9999 | >1 year | < 250 ms | 6 Gbit/s | UE to Network; Network to UE | ~1500 - ~9000 (note 1) | ~16 ms | stationary | < 2 per 1000 km2 | <400"
- **Figure(s):** 99.9999 (%); >1 year; < 250 ms; 6 Gbit/s; ~16 ms survival time; < 2 per 1000 km2; <400
- **Condition:** Static-remote telesurgery; surgeon about 400 km away (MED-01m). Columns as MED-01a. The mirror renders the last header as "Service Area [m2]", but the note attached to it reads "Straight line distance between surgeon's console at the hospital and the remote robotic telesurgery system." (TS 22.104 gives "< 400 km (note 12)"). Second video row: "4K 60 fps 12 bits per pixel color coded (e.g. YUV 4:1:1) real time video (loss less compressed) | 99.999 | >>1 month (<1 year) | < 250 ms | 2 Gbit/s | Network to UEs".
- **Use in paper:** the wide-area (inter-hospital) video stream, where the latency budget is loose but the data rate is Gbit/s.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01l  (remote robotic telesurgery: haptic feedback rows)
- **Citation:** as MED-01k.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_e.html
- **Location:** 5.3.3 → "Potential New Requirements…" (p. 36 marker), rows 3–4.
- **Quote:** "Haptic Feedback | 99.9999 | >1 year | <20 ms | 2 Mbits/s | Network to UE | 250 | ~1 ms | stationary | < 2 per 1000 km2 | <400" / "Haptic Feedback | 99.9999 | >1 year | <20 ms | 16 Mbits/s | UE to Network | ~2000 | ~1 ms | stationary | < 2 per 1000 km2 | <400"
- **Figure(s):** 99.9999 (%); >1 year; <20 ms; 2 Mbits/s DL (250 B); 16 Mbits/s UL (~2000 B); ~1 ms survival
- **Condition:** as MED-01k. Clock-sync row in the same table: "Up to 10 UEs (note 2) | < 50 μs | 400 km".
- **Use in paper:** the remote-telesurgery haptic budget (20 ms vs 2 ms local); compare with TS 22.104 row MED-04b.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01m  (remote telesurgery distance)
- **Citation:** as MED-01k.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_e.html
- **Location:** 5.3.3 → "Pre-conditions" (p. 33 marker).
- **Quote:** "The level of expertise needed is not available at his local hospital but the hospital has managed to find a specialist in another hospital within the same country about 400km away but they cannot physically be present for the operation."
- **Figure(s):** about 400km
- **Condition:** narrative use-case assumption (same country, terrestrial).
- **Use in paper:** geographic scale for propagation delay (the model derives it; no arithmetic here).
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-01n  (telesurgery haptic force response, literature value cited by TR)
- **Citation:** as MED-01k. The TR attributes the figure to its reference [22] (not identified here).
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_e.html
- **Location:** 5.3.3 → "Service Flows" (p. 34 marker).
- **Quote:** "Haptic Feedback (considering human reaction) 3-10ms"
- **Figure(s):** 3-10ms
- **Condition:** The TR introduces these as "typical figures taken based on research [22]" (listed with 2D/3D camera, audio flows). It is a literature figure, not a 3GPP KPI.
- **Use in paper:** optional context only.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0; the underlying research ref [22] was not fetched)

### MED-01o  (TR 22.826 definition of end-to-end latency: one-way)
- **Citation:** 3GPP TR 22.826, clause 3 "Definitions, symbols and abbreviations".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_a.html (header shows "Word version: 17.1.0")
- **Location:** clause 3 (definitions).
- **Quote:** "end-to-end latency: the time that takes to transfer a given piece of information from a source to a destination, measured at the communication service interface, from the moment it is transmitted by the source to the moment it is successfully received at the destination."
- **Figure(s):** none (definition; establishes one-way latency)
- **Condition:** This mirror part is labelled 17.1.0, while parts b–g are labelled 17.2.0. The same clause defines communication service availability as a "percentage value of the amount of time the end-to-end communication service is delivered according to an agreed QoS, divided by the amount of time the system is expected to deliver the end-to-end service according to the specification in a specific area."
- **Use in paper:** labels every TR 22.826 latency as one-way, source to destination.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826)

---

## MED-02 — TR 22.826 robotic-aided diagnosis / tele-ultrasound

### MED-02a  (tele-ultrasound: below 20 ms one-way end-to-end)
- **Citation:** as MED-01a, clause 5.3.2 "Emergency care - Ultrasound examination and remote interventional support".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_d.html (header "Word version: 17.2.0")
- **Location:** 5.3.2 → "Description" (mirror p. 28 marker).
- **Quote:** "Along the same principles as depicted in clause, but considering there isn't any heavy processing at the application side, one ends up with a below 20 ms one way end-to-end latency from the echographer to the application at the remote expert site."
- **Figure(s):** below 20 ms one way end-to-end latency
- **Condition:** Ambulance-based ultrasound with a remote expert (static-remote modality). The service flow notes "As an option Marc may even control a robot in the ambulance for the ultrasound capture." The clause cross-reference number is missing in the mirror text.
- **Use in paper:** the tele-diagnosis latency ceiling, explicitly one-way.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-02b  (gesture tracking basis: 30 cm/s, 1 cm, 35 ms)
- **Citation:** as MED-02a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_d.html
- **Location:** 5.3.2 → "Description" (p. 28 marker).
- **Quote:** "In general, we consider here gestures executed at the speed of 30 cm/s and with an expected accuracy of 1cm which gives us a total imaging system latency of up to 35 ms."
- **Figure(s):** 30 cm/s; 1cm; up to 35 ms total imaging system latency
- **Condition:** derivation basis for MED-02a. The same clause assumes "a straight-line distance below < 50 km for the ambulance journey".
- **Use in paper:** shows where the 20 ms figure comes from (clinical kinematics), for the reviewer.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-02c  (tele-ultrasound: 4K video row)
- **Citation:** as MED-02a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_d.html
- **Location:** 5.3.2 → "Potential New Requirements needed to support the use case" (p. 32 marker), row 1.
- **Quote:** "Compressed 4K (3840x2160 pixels) 60 fps 12 bits per pixel color coded (e.g. YUV 4:1:1) real-time video stream | 99.99 | >1 month | <20 ms | 25 Mbits/s | UE to Network | ~1500 | ~100 ms | stationary | <20 per 100 km2 | <50"
- **Figure(s):** 99.99 (%); >1 month; <20 ms; 25 Mbits/s; ~1500 B; ~100 ms survival; <20 per 100 km2; <50
- **Condition:** Uplink from the ambulance. The mirror renders the last header as "Service Area [m2]", but the table's note reads "Straight line distance between an ambulance and the closest emergency room". The Description assumes "a straight-line distance below < 50 km for the ambulance journey".
- **Use in paper:** compressed-video stream rate for the tele-diagnosis budget.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-02d  (tele-ultrasound: uncompressed ultrasound-probe stream row)
- **Citation:** as MED-02a.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_d.html
- **Location:** 5.3.2 → "Potential New Requirements…" (p. 32 marker), row 2.
- **Quote:** "Uncompressed 512x512 pixels 32 bits 20 fps video stream from ultra-sound probe | 99.999 | >>1 month (<1 year) | <20 ms | 160 Mbits/s | UE to Network | ~1500 | ~50 ms | stationary | <20 per 100 km2 | <50"
- **Figure(s):** 99.999 (%); >>1 month (<1 year); <20 ms; 160 Mbits/s; ~50 ms survival
- **Condition:** as MED-02c. No haptic row appears in this 5.3.2 table.
- **Use in paper:** raw imaging stream rate for tele-ultrasound.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-02e  (mobile specialist practice: haptic feedback row, the robotic-diagnosis haptic figures)
- **Citation:** as MED-01a, clause 5.3.4 "Mobile Specialist Practice".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_f.html (header "Word version: 17.2.0")
- **Location:** 5.3.4 → "Potential New Requirements needed to support the use case" (p. 41 marker), haptic row.
- **Quote:** "Haptic feedback data stream | 99.999 | >> 1 month (< 1 year) | <20 ms | ~2 Mbit/s / 16 Mbit/s | UE to Network; Network to UE | ~80 | ~1 ms | stationary | <20 per 100 km2 | ~ 0.1 Regional"
- **Figure(s):** 99.999 (%); >> 1 month (< 1 year); <20 ms; ~2 Mbit/s / 16 Mbit/s; ~80 B; ~1 ms survival; <20 per 100 km2
- **Condition:** Mobile clinic (truck) connected to a remote specialist. Columns: … | Message Size [byte] | Survival time | UE speed | # of active UEs | Service Area [km2]. The final cell text "~ 0.1 Regional" is ambiguous in the mirror rendering. Table NOTE: "The mobile specialist practice has dimensions of ca. 15 m x 3 m x 3 m." Other rows in the same table: stereoscopic 4K video "2 Gbit/s" "< 250 ms"; compressed 4K "25 Mbit/s" "<100 ms"; ultrasound "160 Mbit/s" "<50 ms"; audio "128 kbit/s". These match the normative TS 22.104 "Robotic Aided Diagnosis (A.6.3)" row (MED-04c: 80-byte messages, 1 ms, 2–16 Mbit/s).
- **Use in paper:** haptic channel for robotic diagnosis.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

---

## MED-03 — TR 22.826 patient monitoring (inside/outside hospital), ambulance

### MED-03a  (cardiac telemetry inside hospital/care facility)
- **Citation:** as MED-01a, clause 5.4.2 "Cardiac telemetry inside hospital/care facility".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html (header "Word version: 17.2.0")
- **Location:** 5.4.2 → potential-requirements table (single row).
- **Quote:** "99,99999 % | > 1 year | < 100 ms | 0.5 Mbit/s | ≤ 1000 | 100ms | ≤ 5 km/h | ≤ 1000 per km2 | Hospital (incl. elevators)"
- **Figure(s):** availability 99,99999 %; MTBF > 1 year; < 100 ms; 0.5 Mbit/s; message ≤ 1000 bytes; survival time 100ms; UE speed ≤ 5 km/h; ≤ 1000 per km2
- **Condition:** Body-worn IoT device inside the hospital, moving at walking speed. Columns: Communication service availability: target value | Communication service reliability: mean time between failures | End-to-end latency: maximum | Service bit rate: user experienced data rate | Message size [byte] | Survival time | UE speed | # of active UEs | Service area | Remarks. Remarks: "Use case entails body-worn IoT device. Use case involves possible deployment using non-public network and/or multi-RAT technologies (incl. handover to PLMN)".
- **Use in paper:** in-hospital wearable stream plus device density (for key-management scale).
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03b  (cardiac telemetry outside the hospital: at home, in transit)
- **Citation:** as MED-01a, clause 5.5.3 "Cardiac telemetry outside the hospital".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.3 → "Potential New Requirements needed to support the use case" (p. 50 marker).
- **Quote:** "99,9999 % | below 1 year but >> 1 month | < 100 ms | 0.5 Mbit/s | ≤ 1000 | < 1s | ≤ 500 km/h | In area with hospital up to 1000 per km2; In suburban areas up to 10 per km2 | Country wide including rural areas and deep indoor"
- **Figure(s):** 99,9999 %; < 100 ms; 0.5 Mbit/s; ≤ 1000 B; survival < 1s; ≤ 500 km/h; up to 1000 per km2 (hospital area) / up to 10 per km2 (suburban)
- **Condition:** Wide-area body-worn device (car/train). Remarks: "Use case entails body-worn IoT device (see Note 2) User could be moving by car or by train." NOTE 1 on deep indoor: "elevators, building's basement, underground parking lot…".
- **Use in paper:** outside-hospital monitoring (the NTN-relevant "country wide including rural" service area).
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03c  (wearable energy constraint: 3.3 V, <1000 mAh, 1 month, <50 mA)
- **Citation:** as MED-03b.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.3, note under the potential-requirements table (numbered "Note 2" in one extraction and unnumbered in another).
- **Quote:** "These performance requirements are aimed to be achieved using a 3.3V battery powered device with battery capacity <1000 mAh without recharging for at least 1 month, and whereby the peak current for transmit operations stays below 50mA."
- **Figure(s):** 3.3V; <1000 mAh; at least 1 month; below 50mA peak transmit current
- **Condition:** applies to the MED-03b requirement set.
- **Use in paper:** the energy envelope in which PQC handshake/verify cost must fit on a wearable (constrained-PQC section).
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03d  (patient monitoring inside ambulances: 4K video row)
- **Citation:** as MED-01a, clause 5.5.2 "Patient monitoring inside ambulances".
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.2 KPI table (mirror p. 44 marker for the heading), row 1.
- **Quote:** "Compressed 4K (3840x2160 pixels) 12 bits per pixel (e.g. YUV4:1:1) 60 fps real time video stream | 99.99 | >1 month | < 100ms | 25 Mbits/s | UE to Network | ~1500 | ~100 ms | 150 | <20 per 100 km2 | <50"
- **Figure(s):** 99.99 (%); < 100ms; 25 Mbits/s; ~1500 B; ~100 ms survival; UE speed 150; <20 per 100 km2; <50
- **Condition:** Moving-remote (ambulance in transit). Columns: … | Survival time | UE speed | # of active UEs | Service Area [km] (note 3). NOTE 3: "Straight line distance between an ambulance and the closest emergency room". The UE-speed cell reads "150" with no unit in the cell.
- **Use in paper:** ambulance video uplink.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03e  (ambulance: uncompressed scan stream row)
- **Citation:** as MED-03d.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.2 KPI table, row 2.
- **Quote:** "Uncompressed 2048x2048 pixels 16 bits per pixel 10 fps real-time video scan stream | 99.999 | >>1 month (<1 year) | <100ms | 670 Mbits/s | UE to Network | ~1500 | ~100 ms | 150 | <20 per 100 km2 | <50"
- **Figure(s):** 99.999 (%); <100ms; 670 Mbits/s
- **Condition:** as MED-03d.
- **Use in paper:** peak ambulance uplink stream.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03f  (ambulance: vital-signs stream row)
- **Citation:** as MED-03d.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.2 KPI table, row 3.
- **Quote:** "Physical vital signs monitoring data stream | 99.999 | >>1 month (<1 year) | <100 ms | 1 Mbits/s | UE to Network | ~80 (note 1) | 150 | <20 per 100 km2 | <50"
- **Figure(s):** 99.999 (%); <100 ms; 1 Mbits/s; ~80 B messages
- **Condition:** as MED-03d. The survival-time cell is blank or absent in the mirror rendering (two extractions agree). NOTE 1 in MED-03g.
- **Use in paper:** small-packet physiological stream in the ambulance.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03g  (ambulance: ECG packet composition, 200 Hz)
- **Citation:** as MED-03d.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.2, NOTE 1 under the KPI table.
- **Quote:** "10 bytes digitized ECG signal sampled at 200Hz, plus 40 bytes IPv6 headers or 20 Bytes IPv4 headers + 22 bytes Ethernet + 4 bytes CRC"
- **Figure(s):** 10 bytes ECG payload; 200Hz; 40 B IPv6 / 20 B IPv4; 22 B Ethernet; 4 B CRC
- **Condition:** One extraction prefixed the note with "For example,". The audio row's NOTE 2 reads "12 bytes RTP + 8 bytes UDP + 20 bytes IPv4 + 22 bytes Ethernet + 4 bytes CRC + Audio Payload = 322 bytes every 16ms".
- **Use in paper:** header-vs-payload ratio baseline, before adding AEAD tag/PQ overhead.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

### MED-03h  (ambulance: audio stream row)
- **Citation:** as MED-03d.
- **Fetched URL:** https://www.tech-invite.com/3m22/toc/tinv-3gpp-22-826_g.html
- **Location:** 5.5.2 KPI table, row 4.
- **Quote:** "High quality audio stream | 99.99 | >1 month | <100 ms | 128 kbits/s | UE to Network; Network to UE | ~300 (note 2) | ~16 ms | 150 | <20 per 100 km2 | <50"
- **Figure(s):** 128 kbits/s; <100 ms; ~300 B; ~16 ms
- **Condition:** as MED-03d.
- **Use in paper:** voice channel in the stream mix.
- **Status:** SECONDARY (via tech-invite mirror of TR 22.826 V17.2.0)

---

## MED-04 — TS 22.104 (Rel-19) medical rows — normative

Medical rows **exist** in TS 22.104 V19.2.0 Table 5.2-1 "Periodic deterministic communication
service performance requirements": two rows labelled "Robotic Aided Surgery (A.6.2)" and one
labelled "Robotic Aided Diagnosis (A.6.3)". There are no medical rows in Tables 5.3-1, 5.4-1 or
5.5-1. Row index numbers could not be extracted reliably (one extraction gave 23–25, another
19–21, and a third said no indices were legible), so the rows are identified by their Remarks label.

Common: ETSI TS 122 104 V19.2.0 (2026-01) = 3GPP TS 22.104 version 19.2.0 Release 19, "Service
requirements for cyber-physical control applications in vertical domains". Table 5.2-1 columns,
in order: "Communication service availability: target value (note 1)" | "Communication service
reliability: mean time between failures" | "End-to-end latency: maximum (note 2) (note 12a)" |
"Service bit rate: user experienced data rate (note 12a)" | "Message size [byte] (note 12a)" |
"Transfer interval: target value (note 12a)" | "Survival time (note 12a)" | "UE speed (note 13)" |
"# of UEs" | "Service area (note 3)" | "Remarks". NOTE 1: "One or more retransmissions of network
layer packets may take place in order to satisfy the communication service availability
requirement." NOTE 12: "Maximum straight-line distance between UEs." NOTE 12a: "It applies to
both UL and DL unless stated otherwise." Clause 3.1 defines end-to-end latency "as defined in
TS 22.261 [2]" (see MED-05a).

### MED-04a  (TS 22.104 Table 5.2-1: Robotic Aided Surgery, local row)
- **Citation:** 3GPP TS 22.104 V19.2.0 (Rel-19) / ETSI TS 122 104 V19.2.0 (2026-01), Table 5.2-1. Accessed 2026-09-27.
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/122100_122199/122104/19.02.00_60/ts_122104v190200p.pdf
- **Location:** clause 5.2, Table 5.2-1, row with Remarks "Robotic Aided Surgery (A.6.2)" (first of two); ETSI pp. 18–19 as reported by the extraction.
- **Quote:** ">99.999 999 % | > 10 years | < 2 ms | 2 Mbit/s to 16 Mbit/s | 250 to 2,000 | 1 ms | transfer interval value | stationary | 1 | < 100 m2 | Robotic Aided Surgery (A.6.2)"
- **Figure(s):** availability >99.999 999 %; MTBF > 10 years; end-to-end latency < 2 ms; 2 Mbit/s to 16 Mbit/s; message 250 to 2,000 bytes; transfer interval 1 ms; survival time = transfer interval value; 1 UE; < 100 m2
- **Condition:** Rel-19 normative Stage-1 requirement. Periodic deterministic traffic, one wireless link, one-way end-to-end latency per TS 22.261 definition, stationary UE, operating-room area. Values reproduced identically in two independent extractions.
- **Use in paper:** the primary citable URLLC KPI for the local-surgery security budget (per-message crypto within <2 ms at a 1 ms interval, 250–2000 B).
- **Status:** VERIFIED

### MED-04b  (TS 22.104 Table 5.2-1: Robotic Aided Surgery, remote row)
- **Citation:** as MED-04a.
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/122100_122199/122104/19.02.00_60/ts_122104v190200p.pdf
- **Location:** Table 5.2-1, second row with Remarks "Robotic Aided Surgery (A.6.2)".
- **Quote:** ">99.999 9 % | > 1 year | < 20 ms | 2 Mbit/s to 16 Mbit/s | 250 to 2,000 | 1 ms | transfer interval value | stationary | 2 per 1,000 km2 | < 400 km (note 12) | Robotic Aided Surgery (A.6.2)"
- **Figure(s):** >99.999 9 %; > 1 year; < 20 ms; 2 Mbit/s to 16 Mbit/s; 250 to 2,000 B; 1 ms; 2 per 1,000 km2; < 400 km
- **Condition:** as MED-04a but wide-area (inter-hospital), max straight-line distance < 400 km between UEs (NOTE 12).
- **Use in paper:** remote-telesurgery budget (20 ms one-way over ≤ 400 km); a possible NTN comparison point.
- **Status:** VERIFIED

### MED-04c  (TS 22.104 Table 5.2-1: Robotic Aided Diagnosis)
- **Citation:** as MED-04a.
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/122100_122199/122104/19.02.00_60/ts_122104v190200p.pdf
- **Location:** Table 5.2-1, row with Remarks "Robotic Aided Diagnosis (A.6.3)".
- **Quote:** ">99.999 % | >> 1 month (< 1 year) | < 20 ms | 2 Mbit/s to 16 Mbit/s | 80 | 1 ms | transfer interval value | stationary | 20 per 100 km2 | < 50 km (note 12) | Robotic Aided Diagnosis (A.6.3)"
- **Figure(s):** >99.999 %; >> 1 month (< 1 year); < 20 ms; 2 Mbit/s to 16 Mbit/s; 80 bytes; 1 ms; 20 per 100 km2; < 50 km
- **Condition:** as MED-04a; tele-diagnosis (tele-ultrasound-type) with max straight-line distance < 50 km.
- **Use in paper:** robotic-diagnosis budget (80-byte messages every 1 ms), the smallest normative clinical message.
- **Status:** VERIFIED

### MED-04d  (TS 22.104 Table 5.2-1 NOTE 2: one wireless link)
- **Citation:** as MED-04a.
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/122100_122199/122104/19.02.00_60/ts_122104v190200p.pdf
- **Location:** Table 5.2-1, NOTE 2 (attached to the end-to-end latency column header).
- **Quote:** "Unless otherwise specified, all communication includes 1 wireless link (UE to network node or network node to UE) rather than two wireless links (UE to UE)."
- **Figure(s):** 1 wireless link
- **Condition:** scopes every latency in Table 5.2-1 (MED-04a–c).
- **Use in paper:** establishes that the <2 ms / <20 ms budgets are per single radio hop, not console-to-robot over two radio links.
- **Status:** VERIFIED

---

## MED-05 — TS 22.261 low-latency / high-reliability KPIs

### MED-05a  (TS 22.261 definition of end-to-end latency)
- **Citation:** 3GPP TS 22.261 V19.14.0 (Rel-19) / ETSI TS 122 261 V19.14.0 (2026-07), "Service requirements for the 5G system", clause 3.1. Accessed 2026-09-27.
- **Fetched URL:** https://www.etsi.org/deliver/etsi_ts/122200_122299/122261/19.14.00_60/ts_122261v191400p.pdf
- **Location:** clause 3.1 Definitions (ETSI pp. 14–17 as reported).
- **Quote:** "end-to-end latency: the time that it takes to transfer a given piece of information from a source to a destination, measured at the communication interface, from the moment it is transmitted by the source to the moment it is successfully received at the destination."
- **Figure(s):** none (definition; one-way)
- **Condition:** The same clause defines reliability as "in the context of network layer packet transmissions, percentage value of the packets successfully delivered to a given system entity within the time constraint required by the targeted service out of all the packets transmitted." It defines communication service availability as a "percentage value of the amount of time the end-to-end communication service is delivered according to a specified QoS, divided by the amount of time the system is expected to deliver the end-to-end service." TS 22.104 imports this definition (MED-04).
- **Use in paper:** labels all 3GPP latency KPIs in the paper as one-way.
- **Status:** VERIFIED

### MED-05b  (TS 22.261 Table 7.2.2-1 rows: tactile interaction, discrete automation/motion control, remote control, ITS, eHealth)
- **Citation:** 3GPP TS 22.261, clause 7.2.2 "Scenarios and KPIs", Table 7.2.2-1.
- **Fetched URL:** none returned the table.
- **Location:** n/a
- **Quote:** n/a
- **Figure(s):** n/a
- **Condition:** ETSI table-of-contents page numbers (fetched): V15.5.0: 7.2.2 p. 30, 7.2.3 p. 33. V16.18.0: 7.2.2 p. 41, 7.2.3 p. 42. V17.16.0: 7.2.2 p. 48, 7.2.3 p. 49. V18.19.0: 7.2.2 p. 72, 7.2.3 p. 72. V19.14.0: 7.2.2 p. 88, 7.2.3 p. 89. The shrinking span, together with MED-05c, suggests the table was cut down or removed after Rel-15. This is an inference and is UNVERIFIED.
- **Use in paper:** would have given the classic "tactile interaction" and "remote control" rows. Use TS 22.104 (MED-04) and Table 7.11-1 (MED-05d) instead.
- **Status:** NOT-FOUND. Tried: (1) ETSI PDFs V19.14.0, V18.19.0, V17.16.0, V16.18.0, V15.9.0, V15.5.0. WebFetch's extracted text stops before the body of clause 7.2.2 in every version (only the TOC entry is visible, and search for "99,9999", "Tactile" and "Table 7.2.2-1" in the body found nothing). (2) tech-invite.com TS 22.261 part `_p` (clause 7.1–7.3). WebFetch failed repeatedly ("Failed to fetch or parse robots.txt" / "SSL: CERTIFICATE_VERIFY_FAILED … Hostname mismatch"), so per the rules no other means were tried. (3) Secondary papers checked, none of which reproduce the table: Kim et al. arXiv 1907.04474; Ji et al. arXiv 1704.05565; Fehrenbach et al. arXiv 1808.07034; Sharma et al. arXiv 1908.07337; Jun et al. ETRI J. 42(5) 2020; Varga et al. Sensors 20(3):828; Thabet et al. Future Internet 17(11):494. Lead only, not usable: a 3GPP MCC web article (A. Sultan, 3gpp.org/technologies/urlcc-2022) says "For instance, for remote control of process automation, a reliability of 99.9999% is expected, with a user experienced data rate up to 100 Mbps and an end-to-end latency of 50 ms." It does not name TS 22.261, so it cannot stand in for the table.

### MED-05c  (TS 22.261 Rel-20 clause 7.2.2 contains no table and points to TS 22.104/22.186/22.289)
- **Citation:** 3GPP TS 22.261 (Rel-20, as labelled by the mirror), clause 7.2.2 "Scenarios and KPIs".
- **Fetched URL:** https://itecspec.com/3gpp/22.261/s/7.2.2 (also https://itecspec.com/spec/3gpp-22-261-7-2-2-scenarios-and-kpis/)
- **Location:** clause 7.2.2, last sentence.
- **Quote:** "Cyber-physical control applications in vertical domains can be found in 22.104 [21]." … "For specific requirements, refer to the specifications noted above [21], [9], [23]."
- **Figure(s):** none
- **Condition:** The mirror labels the text "Rel-20". The extraction reports no table and no mention of "Table 7.2.2-1" in the clause. The clause also says "V2X can be found in 22.186 [9]." and "Rail communications can be found in 22.289 [23]."
- **Use in paper:** justifies citing TS 22.104 (MED-04) rather than TS 22.261 Table 7.2.2-1 for current-release URLLC KPIs.
- **Status:** SECONDARY (via itecspec.com verbatim HTML mirror of 3GPP TS 22.261 Rel-20; not confirmed on ETSI because the PDF extraction is truncated, see MED-05b)

### MED-05d  (TS 22.261 Table 7.11-1: "Remote control robot" haptic row)
- **Citation:** 3GPP TS 22.261 (Rel-20 per mirror), clause 7.11 "KPIs for tactile and multi-modal communication service", Table 7.11-1 "Multi-modal communication service performance requirements".
- **Fetched URL:** https://itecspec.com/3gpp/22.261/s/7.11
- **Location:** Table 7.11-1, first "Remote control robot" row.
- **Quote:** "Remote control robot | 1-20ms | 16 kbit/s -2 Mbit/s (without haptic compression encoding); 0.8 - 200 kbit/s (with haptic compression encoding) | 99.999% [40] | 2-8 (1 DoF) | high-dynamic (≤ 50 km/h) | ≤ 1 km2 | Haptic feedback"
- **Figure(s):** max allowed end-to-end latency 1-20ms; 16 kbit/s -2 Mbit/s uncompressed / 0.8 - 200 kbit/s compressed; reliability 99.999%; message 2-8 bytes (1 DoF); ≤ 50 km/h; ≤ 1 km2
- **Condition:** Columns: Use Cases | Max allowed end-to-end latency | Service bit rate: user-experienced data rate | Reliability | Message size (byte) | UE Speed | Service Area | Remarks. The companion row reads "20-100ms … Stationary or Pedestrian … Haptic feedback". Video/audio rows for the same use case give "5 ms | 1-100 Mbit/s | 99.999% [40] | 1500" (video) and "5 ms | 5-512 kbit/s | 99.9% [40] | 50-100" (audio). This is a generic tactile use case, not medical.
- **Use in paper:** the haptic message size (2–8 B per DoF) makes the security-overhead ratio extreme.
- **Status:** SECONDARY (via itecspec mirror of TS 22.261 Rel-20)

### MED-05e  (TS 22.261 Table 7.11-1 NOTE 2, citing IEEE 1918.1)
- **Citation:** as MED-05d.
- **Fetched URL:** https://itecspec.com/3gpp/22.261/s/7.11
- **Location:** Table 7.11-1, NOTE 2.
- **Quote:** "According to IEEE 1918.1 [40] as for haptic feedback, the latency is less than 25 ms for accurately completing haptic operations."
- **Figure(s):** less than 25 ms
- **Condition:** 3GPP attributes this figure to IEEE 1918.1 [40]. A first extraction continued: "As rendering and hardware introduce some delay, the communication delay for haptic modality can be reasonably less than 5 ms, i.e. the packets related to one haptic feedback are transferred to the devices within 10 ms." That continuation came back in only one of two extractions, so it is not used.
- **Use in paper:** links the 3GPP haptic KPI to IEEE 1918.1 (see MED-06).
- **Status:** SECONDARY (via itecspec mirror of TS 22.261 Rel-20)

---

## MED-06 — IEEE Std 1918.1 (Tactile Internet)

### MED-06a  (IEEE 1918.1-2024: designation, dates, scope)
- **Citation:** IEEE, "IEEE Standard for Tactile Internet: Application Scenarios, Definitions and Terminology, Architecture, Functions, and Technical Assumptions," IEEE Std 1918.1-2024 (COM/MobiNet-SC). Board approval 2024-09-26; "Published: 2026-01-23" per the IEEE SA page. Accessed 2026-09-27.
- **Fetched URL:** https://standards.ieee.org/ieee/1918.1/6721/ (and https://standards.ieee.org/about/sasb/sba/26sep2024/)
- **Location:** IEEE SA standard page (Scope; status fields). The SASB 26 Sep 2024 approvals list has the entry "1918.1-2024 (COM/MobiNet-SC) IEEE Standard for Tactile Internet: Application Scenarios, Definitions and Terminology, Architecture, Functions, and Technical Assumptions".
- **Quote:** "A framework for the Tactile Internet, including descriptions of various application scenarios, definitions and terminology, functions, and technical assumptions, is defined by this standard."
- **Figure(s):** year 2024 (designation "IEEE 1918.1-2024"; "Board Approval: 2024-09-26"; "Published: 2026-01-23"; "Status: Active Standard")
- **Condition:** The IEEE SA page, WG page (grouper.ieee.org/groups/1918/1/) and PAR (approved 2016-03-03) give no numeric latency. The PAR "Need" only says "The Tactile Internet presents acutely challenging requirements, in terms of latency, reliability, security, and likely others". The IEEE Xplore pages (e.g., draft P1918.1/D3, doc 10053664) render client-side and returned no content to WebFetch.
- **Use in paper:** citation for the Tactile Internet framework and its year. Numeric latency comes via MED-06b–d or MED-05e.
- **Status:** VERIFIED (year/scope). Latency statement from the IEEE Xplore abstract/scope: NOT-FOUND (tried IEEE Xplore doc 10053664 [empty JS page], IEEE SA page, SASB page, WG page, PAR PDF).

### MED-06b  (Holland et al. on the 1918.1 WG: telesurgery haptic latency 10–100 ms)
- **Citation:** O. Holland, E. Steinbach, R. V. Prasad, Q. Liu, Z. Dawy, A. Aijaz, N. Pappas, K. Chandra, V. S. Rao, S. Oteafy, M. Eid, M. Luden, A. Bhardwaj, X. Liu, J. Sachs, J. Araújo, "The IEEE 1918.1 'Tactile Internet' Standards Working Group and its Standards," *Proc. IEEE*, 107(2):256–279, Feb. 2019. DOI 10.1109/JPROC.2018.2885541 (volume/issue/pages from Crossref).
- **Fetched URL:** https://www.st.ewi.tudelft.nl/vijay/pdfs/holland2019ieee1918.pdf (author-hosted file marked "IEEE Proof"); metadata from https://api.crossref.org/works/10.1109/JPROC.2018.2885541
- **Location:** Sec. IV "Use Cases and Requirements", Teleoperation (proof p. 7).
- **Quote:** "For teleoperation in a medium-dynamic environment (e.g., telesurgery and telerehabilitation), the teleoperator can react and move with reduced speed or copes with deformable objects. As a result, the latency requirement of haptic data exchange in this scenario is extended to 10–100 ms."
- **Figure(s):** 10–100 ms (haptic data exchange, telesurgery-class teleoperation)
- **Condition:** WG members describing the P1918.1 use-case set (pre-publication, 2018/2019). Whether latency is one-way or round-trip is not stated in the quoted sentence.
- **Use in paper:** IEEE-side telesurgery haptic latency range.
- **Status:** SECONDARY (via Holland et al., Proc. IEEE 2019, which describes IEEE 1918.1)

### MED-06c  (Holland et al.: 1–10 ms for highly dynamic teleoperation)
- **Citation:** as MED-06b.
- **Fetched URL:** https://www.st.ewi.tudelft.nl/vijay/pdfs/holland2019ieee1918.pdf
- **Location:** Sec. IV, Teleoperation (proof p. 7).
- **Quote:** "When the environment is highly dynamic (e.g., tele-soccer, where the user remotely operates his robotic avatar in a soccer game), the exchange of haptic signals is extremely time critical, with a latency requirement of 1–10 ms, in order to interact with fast moving objects."
- **Figure(s):** 1–10 ms
- **Condition:** as MED-06b; non-medical high-dynamic case.
- **Use in paper:** upper-stringency comparison.
- **Status:** SECONDARY (via Holland et al., Proc. IEEE 2019)

### MED-06d  (Holland et al.: ~5 ms round-trip human-client vs 1 ms machine-client)
- **Citation:** as MED-06b.
- **Fetched URL:** https://www.st.ewi.tudelft.nl/vijay/pdfs/holland2019ieee1918.pdf
- **Location:** Sec. I "Introduction" (proof p. 2).
- **Quote:** "In the case of such machines using the TI, latency might be reduced from the requirement of around 5-ms round-trip for the most challenging human–client cases to as low as 1-ms round-trip for machine–client cases."
- **Figure(s):** around 5-ms round-trip (human–client); 1-ms round-trip (machine–client)
- **Condition:** explicitly round-trip.
- **Use in paper:** round-trip vs one-way labeling contrast with 3GPP's one-way KPIs.
- **Status:** SECONDARY (via Holland et al., Proc. IEEE 2019)

---

## MED-07 — ITU-T Technology Watch Report "The Tactile Internet" (August 2014)

Common citation: ITU-T, "The Tactile Internet," ITU-T Technology Watch Report, August 2014
(lead author G. Fettweis et al.). Accessed 2026-09-27.
Fetched URL (all MED-07): https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf

### MED-07a  (1 ms ideal round-trip for haptics at ~1000 Hz)
- **Citation:** ITU-T Technology Watch Report, "The Tactile Internet," Aug. 2014.
- **Fetched URL:** https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf
- **Location:** §3.3 "Virtual Reality", p. 6.
- **Quote:** "Typical update rates for the physical simulation and the display of haptic information are in the order of 1000 Hertz, which corresponds to an ideal round-trip communication latency of 1 millisecond."
- **Figure(s):** ~1000 Hertz; ideal round-trip communication latency of 1 millisecond
- **Condition:** explicitly round-trip; haptic VR/physical-simulation loop; 2014 vision document (non-normative).
- **Use in paper:** the canonical "1 ms round-trip" Tactile Internet figure.
- **Status:** VERIFIED

### MED-07b  (round-trip as little as 1 ms: access networks)
- **Citation:** as MED-07a.
- **Fetched URL:** https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf
- **Location:** §4.5 "Access Networks", p. 16.
- **Quote:** "The outlined use cases will require round-trip latencies of as little as 1 millisecond as well as high reliability and capacity (data rates)."
- **Figure(s):** round-trip latencies of as little as 1 millisecond
- **Condition:** round-trip; network-architecture discussion.
- **Use in paper:** as MED-07a.
- **Status:** VERIFIED

### MED-07c  (one-way 200 µs access-network share)
- **Citation:** as MED-07a.
- **Fetched URL:** https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf
- **Location:** §4.5 "Access Networks", p. 16 (refers to Figure 8, "Exemplary latency budget of a system of the Tactile Internet").
- **Quote:** "Future access networks need the ability to cope with one-way latencies of only 200 µs (Figure 8)."
- **Figure(s):** one-way latencies of only 200 µs
- **Condition:** one-way, access-network segment of an exemplary budget.
- **Use in paper:** example of a per-segment latency budget, analogous to our security-processing share.
- **Status:** VERIFIED

### MED-07d  (tele-medical: end-to-end latency 1-10 ms)
- **Citation:** as MED-07a.
- **Fetched URL:** https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf
- **Location:** §3.5 "Healthcare", p. 8.
- **Quote:** "To achieve the high fidelity required for tele-medical applications, it is necessary to achieve end-to-end latency of 1-10 milliseconds and highly reliable data transmission."
- **Figure(s):** end-to-end latency of 1-10 milliseconds
- **Condition:** Tele-diagnosis/tele-surgery/tele-rehabilitation vision; one-way vs round-trip not specified. The preceding sentence notes control approaches that remain stable "in the presence of packet loss and 100-millisecond latency, but the fidelity is significantly decreased."
- **Use in paper:** healthcare-specific Tactile Internet latency range.
- **Status:** VERIFIED

### MED-07e  (propagation: 300 km per ms → ≤150 km to control server)
- **Citation:** as MED-07a.
- **Fetched URL:** https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf
- **Location:** §4.6 "Mobile Edge-Cloud", p. 16.
- **Quote:** "Light travels 300 kilometers within 1 millisecond. The distance between a control server and the point of tactile interaction can thus be 150 kilometers, at most."
- **Figure(s):** 300 kilometers within 1 millisecond; 150 kilometers, at most
- **Condition:** idealised light-speed bound for a 1 ms round-trip.
- **Use in paper:** motivates edge placement of security termination for URLLC (no arithmetic here).
- **Status:** VERIFIED

### MED-07f  ("1-millisecond end-to-end latency is necessary")
- **Citation:** as MED-07a.
- **Fetched URL:** https://www.itu.int/dms_pub/itu-t/opb/gen/T-GEN-TWATCH-2014-1-PDF-E.pdf
- **Location:** p. 1 Executive Summary in two of three extractions; one extraction placed it in Section 1 "Vision Tactile Internet" (pp. 2–3). Possibly a highlighted pull-quote. Check the page before citing it.
- **Quote:** "1-millisecond end-to-end latency is necessary in Tactile Internet applications."
- **Figure(s):** 1-millisecond end-to-end latency
- **Condition:** The wording was identical in three extractions; only the location varies. One-way vs round-trip not stated. Prefer MED-07a/b, which say round-trip explicitly.
- **Use in paper:** headline statement (only with the location check).
- **Status:** VERIFIED (text); location needs a manual check

---

## MED-08 — ITU-R M.2160-0 (IMT-2030 framework, 11/2023)

Common citation: ITU-R, "Framework and overall objectives of the future development of IMT for
2030 and beyond," Recommendation ITU-R M.2160-0 (11/2023). Accessed 2026-09-27.
Fetched URL (all MED-08): https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf

### MED-08a  (latency over the air: 0.1 – 1 ms)
- **Citation:** Rec. ITU-R M.2160-0 (11/2023).
- **Fetched URL:** https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf
- **Location:** §4 "Capabilities of IMT-2030", item "7) Latency", p. 15 (runs to p. 16).
- **Quote:** "Latency over the air interface refers to the contribution by the radio network to the time from when the source sends a packet of a certain size to when the destination receives it. The research target of latency (over the air interface) could be 0.1 – 1 ms."
- **Figure(s):** 0.1 – 1 ms
- **Condition:** IMT-2030 (6G) research target. Over-the-air (radio) contribution only, one-way (source to destination), not end-to-end application latency.
- **Use in paper:** 6G radio-latency floor against which security processing is compared.
- **Status:** VERIFIED

### MED-08b  (reliability over the air: 1-10^-5 to 1-10^-7)
- **Citation:** as MED-08a.
- **Fetched URL:** https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf
- **Location:** §4, item "8) Reliability", p. 16.
- **Quote:** "Reliability over the air interface relates to the capability of transmitting successfully a predefined amount of data within a predetermined time duration with a given probability. The research target of reliability (over the air interface) could range from 1-10−5 to 1-10−7."
- **Figure(s):** 1-10−5 to 1-10−7
- **Condition:** IMT-2030 research target; over-the-air; probability of successful delivery within a time bound.
- **Use in paper:** reliability target, where security-induced drops or retries count against the budget.
- **Status:** VERIFIED

### MED-08c  (usage scenario "Ubiquitous connectivity")
- **Citation:** as MED-08a.
- **Fetched URL:** https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf
- **Location:** §3 "Usage scenarios of IMT-2030", "Ubiquitous connectivity", p. 13.
- **Quote:** "This usage scenario is intended to enhance connectivity with the aim to bridge the digital divide. Connectivity could be enhanced, inter alia, through interworking with other systems (see § 5.1.2). One focus of this usage scenario is to address presently uncovered or scarcely covered areas, particularly rural, remote and sparsely populated areas."
- **Figure(s):** none (qualitative)
- **Condition:** The paragraph continues "Typical use cases include, but not limited to, IoT and mobile broadband communication." § 9) Coverage in §4 gives no numeric target.
- **Use in paper:** NTN/rural-healthcare motivation.
- **Status:** VERIFIED

### MED-08d  (terrestrial–NTN interworking statement)
- **Citation:** as MED-08a.
- **Fetched URL:** https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf
- **Location:** §2.3.3 "Technology enablers to enhance the radio network", p. 10.
- **Quote:** "The interworking of IMT-2030 terrestrial network with its non-terrestrial networks (NTN), including satellite communications, high altitude platform stations as IMT base stations (HIBS), is expected to enhance achieving required connectivity objective."
- **Figure(s):** none (qualitative)
- **Condition:** §5.1.2 "Relationship between IMT-2030 and other access systems" (p. 18) adds that external SDOs have "ongoing standardization activities that facilitate IMT interworking with non-terrestrial networks of IMT (including satellite communication systems, HIBS and UASs)".
- **Use in paper:** grounds the NTN leg of the budget in the IMT-2030 framework.
- **Status:** VERIFIED

### MED-08e  (HRLLC usage scenario lists tele-medicine)
- **Citation:** as MED-08a.
- **Fetched URL:** https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf
- **Location:** §3 "Usage scenarios of IMT-2030", "Hyper reliable and low-latency communication", pp. 12–13.
- **Quote:** "Typical use cases include communications in an industrial environment for full automation, control and operation. These types of communications can help in realizing various applications such as machine interactions, emergency services, tele-medicine, and monitoring for electrical power transmission and distribution."
- **Figure(s):** none (qualitative)
- **Condition:** The scenario is introduced as extending "the Ultra-Reliable and Low-Latency Communication (URLLC) of IMT-2020 and covers specialized use cases that are expected to have more stringent requirements on reliability and latency."
- **Use in paper:** places tele-medicine within 6G HRLLC.
- **Status:** VERIFIED

### MED-08f  (digital health and well-being trend)
- **Citation:** as MED-08a.
- **Fetched URL:** https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2160-0-202311-I!!PDF-E.pdf
- **Location:** §2.2.6 "Digital health and well-being", p. 7.
- **Quote:** "[…] IMT-2030 is expected to facilitate the digital health services including interactive and remote monitoring, tele-diagnosis, remote tele-medical assistance (including tele-connected ambulances), tele-rehabilitation, digital clinical trials and telemedicine."
- **Figure(s):** none (qualitative)
- **Condition:** The same paragraph adds: "In some scenarios, these pervasive IoT devices are expected to function without battery as well."
- **Use in paper:** Healthcare 5.0 framing (ambulance and wearable streams), plus the batteryless-device constraint.
- **Status:** VERIFIED

---

## MED-09 — 5G telesurgery clinical reports (measured)

### MED-09a  (Tian et al. 2020: 12 telerobotic spinal surgeries over 5G, mean network latency 28 ms)
- **Citation:** W. Tian, M. Fan, C. Zeng, Y. Liu, D. He, Q. Zhang, "Telerobotic Spinal Surgery Based on 5G Network: The First 12 Cases," *Neurospine*, 17(1):114–120, 2020. DOI 10.14245/ns.1938454.227 (metadata confirmed via Crossref).
- **Fetched URL:** https://www.e-neurospine.org/journal/view.php?doi=10.14245%2Fns.1938454.227
- **Location:** Results. The sentence also appears in Materials and Methods, per one extraction.
- **Quote:** "The mean network latency of all these operations was 28 ms, reported by China Telecom."
- **Figure(s):** mean network latency 28 ms
- **Condition:** 12 actual patient procedures (June and August 2019; master console at Beijing Jishuitan Hospital, remote robots in Shandong, Zhejiang, Xinjiang, Hebei, Tianjin): "Images were transmitted to the master control room in Beijing Jishuitan Hospital remote surgery center via the 5G network system." The latency is operator-reported (China Telecom), and the paper does not say whether it is one-way or round-trip. No video bitrate is reported.
- **Use in paper:** measured clinical 5G latency, mean over real cases.
- **Status:** VERIFIED

### MED-09b  (Ye et al. 2026: 5G + wired telesurgery, average latency 220 ms, jitter <20 ms)
- **Citation:** Z. Ye, Y. Ding, W. Xu, Y. Xie, M. Qin, J. Fan, L. Cui, N. Li, X. Qiao, Y. Fang, Z. Ji, Y. Yang, J. Dong, "'5G wireless + wired network'-based multi-console robotic telesurgery: adaptability to complex surgical procedures and diverse network infrastructures—a case report," *Transl. Androl. Urol.*, 15(4):140, Apr. 2026. DOI 10.21037/tau-2026-1-0058 (confirmed via Crossref).
- **Fetched URL:** https://tau.amegroups.org/article/view/151205/html
- **Location:** "Surgical procedure" section.
- **Quote:** "Average network latency was 220 ms (with no data packet loss), and network jitter was less than 20 ms."
- **Figure(s):** average network latency 220 ms; jitter less than 20 ms; no packet loss
- **Condition:** One actual patient (robot-assisted radical nephrectomy, KangDuo KD-SR-01), Beijing consoles to Liaoyang patient cart, "an intercity distance of approximately 700 km". Network: "The surgical console in Liaoyang was connected to a stable wired network, whereas the surgical consoles in Beijing relied on a 5G wireless network" (public 5G, China Mobile, via CPE). Latency is defined by the authors as "the signal transmission time from the Beijing-based consoles to the patient cart"; the words "round-trip" and "one-way" do not appear. The paper states "The average latency of 220 ms remained well below the predefined safety threshold of 350 ms."
- **Use in paper:** measured end-to-end clinical latency on a 5G-plus-wired path, far above the 3GPP <20 ms remote KPI (MED-04b).
- **Status:** VERIFIED

### MED-09c  (Ye et al. 2026: video bitrate 40 Mbps)
- **Citation:** as MED-09b.
- **Fetched URL:** https://tau.amegroups.org/article/view/151205/html
- **Location:** "Surgical procedure" section.
- **Quote:** "Additionally, the real-time video transmission bit rate was maintained at 40 Mbps."
- **Figure(s):** 40 Mbps
- **Condition:** as MED-09b; measured during the procedure.
- **Use in paper:** real clinical surgical-video rate. Compare with TR 22.826 lossless Gbit/s KPIs (MED-01b/k).
- **Status:** VERIFIED

### MED-09d  (Ye et al. 2026: measured link throughput at each site)
- **Citation:** as MED-09b.
- **Fetched URL:** https://tau.amegroups.org/article/view/151205/html
- **Location:** "Surgical procedure" section.
- **Quote:** "the Beijing side achieved 177 Mbps (downstream) and 101 Mbps (upstream), while the Liaoyang side achieved 146 Mbps (downstream) and 112 Mbps (upstream)"
- **Figure(s):** Beijing 177 Mbps DL / 101 Mbps UL; Liaoyang 146 Mbps DL / 112 Mbps UL
- **Condition:** as MED-09b. Beijing is the 5G (CPE) side and Liaoyang the wired side.
- **Use in paper:** available-capacity headroom for security overhead on a real 5G telesurgery link.
- **Status:** VERIFIED

### MED-09: considered but not used
- Lacy et al., "5G-assisted telementored surgery," *BJS* 106(12):1576–1579, 2019, DOI 10.1002/bjs.11364. The OUP page shows no figures in the accessible abstract; the Wiley PDF returned 403; PubMed returned a reCAPTCHA page. NOT-FOUND.
- Li et al., "Telemedicine network latency management system in 5G telesurgery," *Surg Endosc* 38(3):1592–1599, 2024, DOI 10.1007/s00464-023-10585-x. The accessible content reports no latency or bitrate values.
- Pan et al., "Feasibility and Safety of Cross-Regional 5G-Enabled Remote Robot-Assisted Laparoscopic Surgery … 21 Patients," *IJMRCAS* 2026, DOI 10.1002/rcs.70214. Wiley returned 403 and Europe PMC returned 429 (proxy rate limit; not retried). NOT-FOUND.
- "A pilot study on the clinical feasibility of 5G remote robot-assisted gastrectomy," *World J Surg Oncol* 2025, DOI 10.1186/s12957-025-03780-8. Springer returned 429 (not retried) and the BMC URL redirects to the same page. NOT-FOUND.
- "Safety and reliability of telesurgery in China: a multicenter, single-arm, phase I clinical trial," *Int J Surg* 2025, DOI 10.1097/JS9.0000000000002792. LWW returned 402. NOT-FOUND.
- Aldousari et al., *J Robot Surg* 19:108, 2025, DOI 10.1007/s11701-025-02274-9. Fetched: "average RTL of 181.4 ms (minimum 176 ms, maximum 304 ms)" over 6935 km, but the paper says "For our study we used wired broadband network" (5G only as back-up). Excluded because it is not a 5G link. Possibly relevant as a long-haul round-trip reference.
