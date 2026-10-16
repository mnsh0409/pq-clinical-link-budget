# clinical-streams.md — physiological stream rates and acquisition parameters

Cluster file under `README.md`. All entries were collected on **2026-09-27** using WebSearch/WebFetch only.
Quotes are verbatim as returned by the fetched page. Each quote is at most 60 words, and "…" marks a trimmed sentence.
Table rows are shown with cells separated by ` | `. This ledger does no arithmetic: stream rates derived from
acquisition parameters are computed in the model scripts and reference these ids.

Where a quote was read only once, it is marked *(single read)*. Every other quote was read twice with the same wording, either in
two fetches or in two copies of the document. Spot-check the single-read quotes against the PDF before submission.

## Mapping from the previous uncited assumptions to ledger ids (no arithmetic)

| Previous assumption (uncited) | Published basis now in ledger | Gap |
|---|---|---|
| ICU monitor "8 channels × 250 Hz × 16-bit" | STR-04 (MIMIC-III: up to eight signals, 125 Hz, 8-/10-/(occasionally) 12-bit); STR-04c (VitalDB: 62.5–500 Hz waveforms, up to 12 waveform tracks) | No source found for 250 Hz / 16-bit as an ICU-monitor norm |
| EEG "32 ch × 256 Hz × 16-bit" | STR-02b (≥256 samples/s, ≥16 bits/sample, 512 Hz preferable, 24-bit typical); STR-02 (≥16 channels, 21 electrodes); STR-08 (typical equipment 32 or more channels; 12 GB/day video+EEG example) | — |
| ECG (resting / monitoring) | STR-03 (500 samples/s needed for 150-Hz cutoff; ≈10 kB per 10 s single lead); STR-01 (ECG 3 Kbps); STR-01b (6-lead 71 kbps, 12-lead 288 kbps, 12 bits) | No bit-depth statement in STR-03 |
| Haptic "1 kHz × 64-byte" packets | STR-05, STR-05b, STR-05c (1 kHz; 1000 packets/s; 16 bit per DoF; 6-byte 3-DoF payload; IPv4/IPv6 header 20/40 bytes) | No source for a 64-byte packet |
| Surgical video "15 Mbit/s" | STR-06 (1080p25 H264 VBR 1.5–2 Mbps, 5G telesurgery demo); STR-06b (4K video "Basic needs" 36 Mbps) | No source for 15 Mbit/s |
| Ambulance video "4 Mbit/s" | STR-07 (5G ambulance field test: video stream 12 Mbps, ultrasound ≈4 Mbps measured) | — |

## Access problems encountered (for re-trying from an institutional network)

- **Europe PMC REST full text** (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10489199/fullTextXML`): the WebFetch proxy rejected it
  with HTTP 429 (rate limited) and said not to refetch. It was not retried.
- **pmc.ncbi.nlm.nih.gov** and **pubmed.ncbi.nlm.nih.gov**: served only a reCAPTCHA page (PMC9178032, PMC10489199, PubMed 25626777).
- **ieeexplore.ieee.org**: `/document/6155061` returned an empty page and `/abstract/document/6155061/` returned HTTP 418.
- **ahajournals.org**, **jacc.org**, **heartrhythmjournal.com**: HTTP 403. **bjssjournals.onlinelibrary.wiley.com**: 403. **journals.lww.com** (Current Urology): 402.
- **nature.com** table sub-page (`/articles/s41597-022-01411-5/tables/2`) and **repository.uantwerpen.be**: disallowed by robots.txt.
- **mentor.ieee.org** document listing: HTTP 418. **api.semanticscholar.org**: 429. The Semantic Scholar paper page is rendered by JavaScript and came back empty.

---

### STR-01  WBAN application data rates — Movassaghi et al. survey (Table II)
- **Citation:** S. Movassaghi, M. Abolhasan, J. Lipman, D. Smith, A. Jamalipour, "Wireless Body Area Networks: A Survey," IEEE Communications Surveys & Tutorials, 16(3):1658–1686, 2014. DOI 10.1109/SURV.2013.121313.00064 (bibliographic data from the Crossref API).
- **Fetched URL:** https://www.academia.edu/56127432/Wireless_Body_Area_Networks_A_Survey. This is the accepted-version text, with page header "IEEE COMMUNICATIONS SURVEYS & TUTORIALS, ACCEPTED FOR PUBLICATION" and DOI 10.1109/SURV.2013.121313.00064. It was cross-checked against https://www.academia.edu/5452276/Body_Area_Networks_A_Survey (manuscript COMST-00064-2013.R1), which has identical Data Rate cells.
- **Location:** Table II, "Characteristics of In/On-Body Applications". The table cites reference [15] in the accepted version and [10] in the R1 manuscript. The reference list was truncated on the host, so that entry was not seen. Column headers are Application Type | Sensor Node | Data Rate | Duty Cycle (per device) % | Power Consumption | QoS (Sensitive to Latency) | Privacy.
- **Quote:** Data Rate cells, read twice:
  - "Glucose sensor" → "Few Kbps"
  - "Pacemaker" → "Few Kbps"
  - "Endoscope Capsule" → "> 2 Mbps"
  - "ECG" → "3 Kbps"
  - "SpO2" → "32 Kbps"
  - "Blood Pressure" → "< 10 bps"
  - "Music for Headsets" → "1.4 Mbps"
  - Section "Data Rates and Power Requirements": "The sensors in WBANs are capable of transmitting data in a wide range of data rates from 1 Kbit/s to 10 Mbit/s [57]." *(single read)*
- **Figure(s):** ECG 3 Kbps; SpO2 32 Kbps; Blood Pressure < 10 bps; Glucose sensor Few Kbps; Endoscope Capsule > 2 Mbps; Music for Headsets 1.4 Mbps; WBAN sensor range 1 Kbit/s to 10 Mbit/s.
- **Condition:** These are nominal per-application rates for WBAN sensor nodes from a survey table. They are not link measurements. The ECG row gives no lead count, sampling rate or resolution. Table II has **no** rows for 6-/12-lead ECG, EEG, EMG, temperature or video (see STR-01b). The survey's own source for the table was not visible.
- **Use in paper:** Clinical-stream rate table giving low-rate WBAN classes (ECG, SpO2, BP, glucose) and the capsule-endoscope upper class in the key-supply budget.
- **Status:** VERIFIED. The text is the accepted version of the survey, hosted on academia.edu. The final IEEE Xplore version could not be fetched (empty page / 418), so re-check the table number and cells against Xplore before submission.

### STR-01b  WBAN application data rates with lead counts — Latré et al. survey (Table 1)
- **Citation:** B. Latré, B. Braem, I. Moerman, C. Blondia, P. Demeester, "A survey on wireless body area networks," Wireless Networks, 17(1):1–18, 2011. DOI 10.1007/s11276-010-0252-4 (bibliographic data from the Springer landing page).
- **Fetched URL:** https://backoffice.biblio.ugent.be/download/3234782/3234793. This is the Ghent University Biblio author manuscript, with header "Wireless Networks manuscript No. (will be inserted by the editor)".
- **Location:** Table 1, "Examples of medical WBAN applications [21, 25–27]". Columns: Application | Data Rate | Bandwidth | Accuracy.
- **Quote:** Rows as extracted. The Data Rate and Accuracy cells were read twice.
  - "ECG (12 leads) | 288 kbps | 100-1000 Hz | 12 bits"
  - "ECG (6 leads) | 71 kbps | 100-500 Hz | 12 bits"
  - "EMG | 320 kbps | 0-10,000 Hz | 16 bits"
  - "EEG (12 leads) | 43.2 kbps | 0-150 Hz | 12 bits"
  - "Blood saturation | 16 bps | 0-1 Hz | 8 bits"
  - "Glucose monitoring | 1600 bps | 0-50 Hz | 16 bits"
  - "Temperature | 120 bps | 0-1 Hz | 8 bits"
  - "Motion sensor | 35 kbps | 0-500 Hz | 12 bits"
  - "Cochlear implant | 100 kbps | – | –"; "Artificial retina | 50-700 kbps | – | –"; "Audio | 1 Mbps | – | –"; "Voice | 50-100 kbps | – | –"
  - Section 3: "…ranging from simple data at a few kbit/s to video streams of several Mbit/s." *(single read, partial sentence)*
- **Figure(s):** ECG 12 leads 288 kbps (12 bits); ECG 6 leads 71 kbps (12 bits); EMG 320 kbps (16 bits); EEG 12 leads 43.2 kbps (12 bits); blood saturation 16 bps (8 bits); glucose 1600 bps (16 bits); temperature 120 bps (8 bits); motion 35 kbps; audio 1 Mbps; voice 50-100 kbps.
- **Condition:** This is a survey table compiled from refs [21] (Theogarajan et al., ISSCC 2006), [25] (Penzel et al., IEEE EMB Mag. 20(3):25–32, 2001), [26] (Arnon et al., IEEE Wireless Commun. 10(1):56–61, 2003) and [27] (Gyselinckx et al., J. Electrocardiol. 40(6):S165–S168), as listed in the manuscript. The rates are nominal raw rates. "Bandwidth" means signal bandwidth in Hz, not radio bandwidth, and "Accuracy" means bits per sample. There is no capsule-endoscope or video row; "several Mbit/s" video is text only.
- **Use in paper:** Supplies the lead-specific ECG/EEG/EMG and temperature rows missing from STR-01, together with published resolution (bits).
- **Status:** VERIFIED (author manuscript). The Springer version is paywalled and the UAntwerp repository copy is robots-blocked.

### STR-01c  IEEE 802.15 TG6 application matrix / technical requirements (original)
- **Citation:** IEEE P802.15 TG6 application matrix / TRD (e.g., IEEE 802.15-08-0407). The exact document was not identified.
- **Fetched URL:** —
- **Location:** —
- **Quote:** —
- **Figure(s):** —
- **Condition:** —
- **Use in paper:** Would be the original source behind survey tables. It is not needed while STR-01/01b hold.
- **Status:** NOT-FOUND. Tried: WebSearch for "15-08-0407" 802.15 TG6, "TG6 Applications Matrix", and "TG6 technical requirements document" (including a search restricted to mentor.ieee.org / ieee802.org). None returned the document. The mentor.ieee.org TG6 document listing returned HTTP 418. Neither survey table's visible citations point to an IEEE 802.15 document.

### STR-02  ACNS Guideline 1 — minimum technical requirements for clinical EEG
- **Citation:** S. R. Sinha, L. Sullivan, D. Sabau, D. San-Juan, K. E. Dombrowski, J. J. Halford, A. J. Hani, F. W. Drislane, M. M. Stecker, "American Clinical Neurophysiology Society Guideline 1: Minimum Technical Requirements for Performing Clinical Electroencephalography," J. Clin. Neurophysiol., 33(4):303–307, 2016. DOI 10.1097/WNP.0000000000000308 (Crossref).
- **Fetched URL:** https://www.acns.org/UserFiles/file/Guideline1-MinimumTechnicalRequirementsforPerofrmingClinicalEEG_v1.pdf
- **Location:** §1.1 (p. 303); §1.5 (p. 303); §2.3 (p. 304)
- **Quote:**
  - §1.1: "Sixteen channels of simultaneous recording are considered the minimum number required to show the areas producing most normal and abnormal EEG patterns."
  - §2.3: "All 21 electrodes and placements recommended by the IFCN3 should be used." (the "3" is a reference superscript)
  - §1.5: "Digital equipment should conform to the recommendations in Guideline 4: Recording Clinical EEG on Digital Media." *(single read)*
- **Figure(s):** minimum 16 channels of simultaneous recording; 21 electrodes (IFCN 10-20 placements). **Sampling rate and amplitude resolution are not stated in Guideline 1**, which defers to Guideline 4 (STR-02b).
- **Condition:** Minimum requirement for routine clinical scalp EEG. The guideline is not specific to ICU continuous EEG.
- **Use in paper:** EEG channel-count basis for the EEG stream (replaces the assumed "32 ch").
- **Status:** VERIFIED

### STR-02b  ACNS Guideline 4 — recording clinical EEG on digital media (sampling rate, bits)
- **Citation:** J. J. Halford, D. Sabau, F. W. Drislane, T. N. Tsuchida, S. R. Sinha, "American Clinical Neurophysiology Society Guideline 4: Recording Clinical EEG on Digital Media," J. Clin. Neurophysiol., 33(4):317–319, 2016. DOI 10.1097/WNP.0000000000000318 (Crossref).
- **Fetched URL:** https://www.acns.org/UserFiles/file/Guideline4-RecordingClinicalEEGonDigitalMedia_v1.pdf (published version). It was cross-checked against https://www.acns.org/UserFiles/file/Guideline4-RecordingClinicalEEGonDigitalMedia.pdf ("Publish Ahead of Print" copy), which has identical wording for the sentences below.
- **Location:** Section "Recording", pp. 317–318. The 256 samples/s sentence is on p. 317 and the 512 Hz sentence on p. 318.
- **Quote:**
  - "Acquisition of EEG data onto a digital storage medium should occur at a minimum sampling rate of 256 samples per second."
  - "Higher rates, such as 512 Hz, are preferable to prevent aliasing on modern high-resolution computer screens."
  - "Digitization should use a resolution of at least 16 bits per sample including any sign bit."
  - "Most modern clinical EEG amplifiers record with a bit depth of 24."
- **Figure(s):** minimum 256 samples per second; 512 Hz preferable; at least 16 bits per sample; 24-bit typical of modern amplifiers.
- **Condition:** Minimum acquisition specification for clinical EEG stored on digital media. This is the recorded (stored) rate, not a display rate. Not used: the follow-on sentence giving an amplitude step renders "0.05 µV" in the preprint copy but "0.05 mV" in the text layer of the published copy, so the unit is unresolved.
- **Use in paper:** EEG per-channel sampling rate and word length (replaces the assumed "256 Hz × 16-bit"). The rate is derived in the model.
- **Status:** VERIFIED

### STR-03  AHA/ACCF/HRS ECG standardization, Part I — digital ECG sampling
- **Citation:** P. Kligfield, L. S. Gettes, J. J. Bailey, R. Childers, B. J. Deal, et al. (13 authors), "Recommendations for the Standardization and Interpretation of the Electrocardiogram: Part I: The Electrocardiogram and Its Technology…," Circulation, 115(10):1306–1324, 2007, DOI 10.1161/CIRCULATIONAHA.106.180200 (Crossref). The quoted text is from the simultaneous co-publication in J. Am. Coll. Cardiol., 49(10):1109–1127, 2007, DOI 10.1016/j.jacc.2007.01.024.
- **Fetched URL:** https://www.sciencedirect.com/science/article/pii/S073510970700232X
- **Location:** "The ECG Signal and Its Processing" → subsections "High-Frequency Filtering" (Technology; Clinical Implications), "Data Compression for Transmission, Storage, and Retrieval of ECGs" (Technology), "The ECG Signal", and "Sampling of the ECG Signal" (Technology; Recommendations)
- **Quote:**
  - High-Frequency Filtering / Technology: "A series of studies have now indicated that data at 500 samples per second are needed to allow the 150-Hz high-frequency digital filter cutoff that is required to reduce amplitude error measurements to ≈1% in adults."
  - Data Compression / Technology: "Digitized at 500 samples per second, 10 seconds of a single lead of ECG record requires ≈10 kB of memory." *(single read)*
  - Sampling / Technology: "Front-end sampling has been performed at rates from 1000 to 2000 per second, but newer converters can routinely sample at 10 000 to 15 000 per second or even higher; other converters are adaptive in sampling rate, with output that is proportional to the energy detected."
  - High-Frequency Filtering / Clinical Implications: "To measure routine durations and amplitudes accurately in adults, adolescents, and children, an upper-frequency cutoff of at least 150 Hz is required; an upper-frequency cutoff of 250 Hz is more appropriate for infants." *(single read)*
  - The ECG Signal: "Because digital ECGs have a temporal resolution in milliseconds and an amplitude resolution in microvolts, recommendations for the high-frequency response of ECGs have evolved over the years."
  - Data Compression / Technology: "The 1990 AHA report recommended that the fidelity of retrieved compressed data should be within 10 μV for corresponding samples." *(single read)*
  - Sampling / Recommendations: "Oversampling by a significant multiple of the upper-frequency cutoff is recommended to provide recommended bandwidth in the digitized signal." *(single read)*
- **Figure(s):** 500 samples per second (needed for a 150-Hz cutoff in adults); ≈10 kB per 10 s of a single lead at 500 samples/s; front-end 1000–2000 per second (earlier) and 10 000–15 000 per second (newer converters); ≥150 Hz upper cutoff (250 Hz for infants); compressed-data fidelity within 10 μV. **No explicit amplitude quantisation (bits or µV per LSB) was found.** The searched terms "resolution", "µV/μV", "bit(s)" and "analog-to-digital" return only the sentences above.
- **Condition:** Standard resting 12-lead diagnostic ECG from digital electrocardiographs, not bedside or ambulatory monitoring. 500 samples/s is the processing/storage rate needed for the 150-Hz cutoff. It is not the front-end A/D rate.
- **Use in paper:** Per-lead ECG sampling basis for 12-lead / diagnostic ECG streams. The published ≈10 kB per 10 s single-lead figure serves as a cross-check.
- **Status:** VERIFIED, from the JACC co-publication of the same statement. The Circulation page (ahajournals.org), jacc.org and heartrhythmjournal.com all returned 403.

### STR-04  ICU multiparameter monitor waveforms — MIMIC-III Waveform Database
- **Citation:** B. Moody, G. Moody, M. Villarroel, G. D. Clifford, I. Silva, "MIMIC-III Waveform Database" (version 1.0), PhysioNet, published April 7, 2020 (as shown on page). DOI 10.13026/c2607m.
- **Fetched URL:** https://physionet.org/content/mimic3wdb/1.0/
- **Location:** Project page sections "Data Description", "Methods", "Technical Limitations" and "Abstract" (section headings confirmed in a separate read)
- **Quote:**
  - Data Description: "Physiologic waveform records in this database contain up to eight simultaneously recorded signals digitized at 125 Hz with 8-, 10-, or (occasionally) 12-bit resolution."
  - Methods: "Waveforms almost always include one or more ECG signals, and often include continuous arterial blood pressure (ABP) waveforms, fingertip photoplethysmogram (PPG) signals, and respiration, with additional waveforms (up to 8 simultaneously) as available."
  - Data Description: "Numerics records typically contain 10 or more time series of vital signs sampled once per second or once per minute."
  - Technical Limitations (ECG): "The scaling reduced the effective amplitude resolution from 12 bits to 9 or 10 bits in typical cases, and as little as 7 bits in some cases."
  - Abstract: "The MIMIC-III Waveform Database contains 67,830 record sets for approximately 30,000 ICU patients."
- **Figure(s):** up to eight simultaneous signals; 125 Hz; 8-, 10-, or (occasionally) 12-bit resolution; numerics sampled once per second or once per minute; effective ECG resolution 9 or 10 bits typical (as little as 7).
- **Condition:** Archived ICU bedside-monitor waveforms as stored in the database. Per Technical Limitations, the ECG was "originally sampled with 12-bit precision at a high sampling rate" *(single read)*, so 125 Hz is the stored rate and not the monitor's front-end rate.
- **Use in paper:** ICU multiparameter-monitor stream (replaces the assumed "8 channels × 250 Hz × 16-bit"). The rate is derived in the model.
- **Status:** VERIFIED

### STR-04b  ICU waveforms — MIMIC-IV Waveform Database (signal list only)
- **Citation:** B. Moody, S. Hao, B. Gow, T. Pollard, W. Zong, R. Mark, "MIMIC-IV Waveform Database" (version 0.1.0), PhysioNet, July 10, 2022. DOI 10.13026/a2mw-f949. The "latest version" DOI 10.13026/6269-ws81 redirects to this 0.1.0 page.
- **Fetched URL:** https://physionet.org/content/mimic4wdb/0.1.0/
- **Location:** Abstract; Release Notes
- **Quote:**
  - Abstract: "The MIMIC-IV Waveform Database is a large collection of physiological signals and measurements from patients in intensive care units, including electrocardiograms, photoplethysmograms, respiration, invasive and non-invasive blood pressure, and more." *(single read)*
  - Release Notes: "This release contains just 200 records from 198 patients, and is intended as a technical preview…" *(single read)*
- **Figure(s):** Signal list only. **The project page states no sampling frequency and no resolution.** Both the 0.1.0 page and the version-less page were checked.
- **Condition:** Technical-preview release of 200 records.
- **Use in paper:** Supporting signal list only. Use STR-04 for rates.
- **Status:** VERIFIED for the signal list. The sampling frequency is NOT-FOUND on the project page.

### STR-04c  High-resolution vital-sign dataset — VitalDB (second basis)
- **Citation:** H.-C. Lee, Y. Park, S. B. Yoon, et al., "VitalDB, a high-fidelity multi-parameter vital signs database in surgical patients," Scientific Data, 9:279, 2022. DOI 10.1038/s41597-022-01411-5. Dataset: H.-C. Lee, C.-W. Jung, "VitalDB…" (version 1.0.0), PhysioNet, September 21, 2022, DOI 10.13026/czw8-9p62.
- **Fetched URL:** https://www.nature.com/articles/s41597-022-01411-5 ; https://physionet.org/content/vitaldb/1.0.0/
- **Location:** Sci. Data section "Data Records" (the sentence refers to Table 2); PhysioNet sections "Data Description" and "Abstract"
- **Quote:**
  - Sci. Data, Data Records: "Vital signs data have various time intervals according to the anesthesia devices, with a time resolution of 1–7 seconds for numeric data and 62.5–500 Hz for waveform data (Table 2)." The same sentence appears on the PhysioNet page, without "(Table 2)".
  - PhysioNet, Data Description: "Vital signs data includes up to 12 waveform and 184 numeric data tracks acquired from multiple anesthesia devices applied to patients during surgery." *(single read)*
  - PhysioNet, Abstract: "This dataset contains high-resolution multi-parameter data from 6,388 cases, including 486,451 waveform and numeric data tracks." *(single read)*
- **Figure(s):** waveform tracks 62.5–500 Hz; numeric data 1–7 s; up to 12 waveform and 184 numeric tracks per case.
- **Condition:** Intra-operative (anaesthesia) recordings in surgical patients, not ICU. Per the PhysioNet page, patient-monitor data came from a GE Solar 8000M. **Per-track sampling rates (Table 2) were not obtained**: the nature.com table page is robots-disallowed, PMC9178032 served a reCAPTCHA, and the PhysioNet page does not reproduce Table 2. eICU was not checked.
- **Use in paper:** Second basis giving the upper and lower waveform-rate bounds for a multiparameter monitor stream.
- **Status:** VERIFIED (the range only; per-track rates NOT-FOUND)

### STR-05  Haptic control-loop / packet rate — Steinbach et al., "Haptic Communications" (2012)
- **Citation:** E. Steinbach, S. Hirche, M. Ernst, F. Brandi, R. Chaudhari, J. Kammerl, I. Vittorias, "Haptic Communications," Proceedings of the IEEE, 100(4):937–956, 2012. DOI 10.1109/JPROC.2011.2182100. Crossref gives the volume, pages and DOI. The full author list is taken from the manuscript.
- **Fetched URL:** https://mediatum.ub.tum.de/doc/1155653/document.pdf. This is the TUM mediaTUM author manuscript, with header "PROCEEDINGS OF THE IEEE, FRONTIERS OF AUDIOVISUAL COMMUNICATIONS: CONVERGENCES OF BROADBAND, COMPUTING AND RICH MEDIA". Its page numbers 1–16 are manuscript pages, not journal pages.
- **Location:** §IV "Perceptual Coding of Haptic Data", opening paragraph, manuscript p. 6. The three sentences are consecutive in this order. The RTP/UDP sentence is in §V "Haptic Communication Protocols".
- **Quote:**
  - "Haptic systems typically use a local 1kHz control loop to overcome device dynamics and display high-frequency haptic effects to the user."
  - "Ideally this update rate should be maintained also across the communication channel."
  - "At a packet rate of 1 kHz, this can become a critical factor and overhead can even dominate compared to the actual payload data."
  - §V: "In an IP-based packet-switched network scenario, the requirements for the haptic stream transport match to the widely applied RTP/UDP protocol." *(single read)*
- **Figure(s):** local control loop 1 kHz; packet rate 1 kHz. **No bytes-per-packet figure** is given; header overhead is discussed only qualitatively.
- **Condition:** Generic kinesthetic bilateral teleoperation (master–slave), not specific to medicine.
- **Use in paper:** Haptic/telesurgery control-loop packet rate (1 kHz) for the per-packet handshake and authentication cost budget.
- **Status:** VERIFIED (author manuscript). IEEE Xplore returned an empty page for /document/ and HTTP 418 for /abstract/.

### STR-05b  Haptic packet rate — Antonakoglou et al., COMST 2018
- **Citation:** K. Antonakoglou, X. Xu, E. Steinbach, T. Mahmoodi, M. Dohler, "Toward Haptic Communications Over the 5G Tactile Internet," IEEE Communications Surveys & Tutorials, 20(4):3034–3059, 2018. DOI 10.1109/COMST.2018.2851452 (Crossref).
- **Fetched URL:** https://scispace.com/pdf/toward-haptic-communications-over-the-5g-tactile-internet-1ye12g467d.pdf. The cover page reads "Peer reviewed version (Author Accepted Manuscript…)".
- **Location:** §II-C "Challenges of teleoperation systems"
- **Quote:**
  - "Haptic sensor readings from kinesthetic devices are typically sampled, packetized and transmitted at a rate of 1 kHz or even higher [6], [22], [23] to maintain stability and transparency of the system…"
  - "Communication of kinesthetic information for teleoperation systems, hence, requires a thousand or more haptic data packets per second to be transmitted between the master and the slave devices."
  - "…a haptic communication system device usually needs to transmit and receive a packet every millisecond, otherwise stability cannot be guaranteed."
- **Figure(s):** 1 kHz or higher; a thousand or more haptic data packets per second; one packet every millisecond.
- **Condition:** Generic kinesthetic teleoperation. No packet size is stated.
- **Use in paper:** Corroborates STR-05 in a 5G / Tactile Internet context.
- **Status:** VERIFIED (author accepted manuscript)

### STR-05c  Haptic packet payload size — Aijaz et al., IEEE Wireless Communications 2017
- **Citation:** A. Aijaz, M. Dohler, A. H. Aghvami, V. Friderikos, M. Frodigh, "Realizing the Tactile Internet: Haptic Communications over Next Generation 5G Cellular Networks," IEEE Wireless Communications, 24(2):82–89, 2017. DOI 10.1109/MWC.2016.1500157RP (Crossref). The arXiv version is 1510.02826v2 (30 Dec 2015), with Comments: "IEEE Wireless Communications - Accepted for Publication".
- **Fetched URL:** https://arxiv.org/pdf/1510.02826 (version details from https://arxiv.org/abs/1510.02826)
- **Location:** Section "B. Haptic Codecs"; Section "E. Ultra-Reliability"
- **Quote:**
  - B: "As part of digitizing the haptic information, the haptic signals are typically sampled at 1 kHz leading to a fairly high packet generation rate of 1000 packets per second."
  - E: "Haptic data is typically sampled at a constant rate with a resolution of 16 bit per DoF. Therefore, the payload of one packet for a 3-DoF haptic stream is only 6 bytes."
  - E: "With the ongoing transition towards IPv6, the issue becomes particularly challenging as the header size doubles from 20 bytes (in IPv4) to 40 bytes." *(single read)*
- **Figure(s):** 1 kHz; 1000 packets per second; 16 bit per DoF; 6-byte payload for a 3-DoF stream; IP header 20 bytes (IPv4) and 40 bytes (IPv6).
- **Condition:** Generic kinesthetic haptic stream (3-DoF example). The payload is given before transport and lower-layer headers other than the IP figure quoted.
- **Use in paper:** Published payload and header basis for the haptic packet size. It replaces the uncited "64-byte" packet. The total packet size is derived in the model.
- **Status:** VERIFIED (arXiv version of the peer-reviewed paper)

### STR-06  Surgical video bitrate in a 5G telesurgery demonstration — Moustris et al. 2023
- **Citation:** G. Moustris, C. Tzafestas, K. Konstantinidis, "A long distance telesurgical demonstration on robotic surgery phantoms over 5G," International Journal of Computer Assisted Radiology and Surgery, 18(9):1577–1587, 2023. DOI 10.1007/s11548-023-02913-2 (Crossref; CC BY 4.0).
- **Fetched URL:** https://link.springer.com/article/10.1007/s11548-023-02913-2
- **Location:** Materials and methods, subsections "Video pipeline" and "Location and networking"; Results
- **Quote:**
  - Video pipeline: "The camera used was a SONY NX5R, producing a 1080i50 10bit 4:2:2 uncompressed video feed…"
  - Video pipeline: "This was captured by a video grabber card (Blackmagic DeckLink DUO 2 mini) on a local workstation and was compressed to 1080p25 using the H264 codec, with a variable bitrate of 1.5–2 Mbps."
  - Video pipeline: "The feed was then streamed over the internet to the surgeon's site using a commercial video streaming service (Zoom)." *(single read)*
  - Materials and methods: "Speed tests measured its download (DL) throughput to 800 Mbps–1.4 Gbps and its upload (UL) throughput to 60–70 Mbps." The antecedent of "its" was not captured.
  - Results: "…the measured round-trip time (i.e., ping) from the surgeon's controllers to the robot at the remote site, and back, was 18 ms."
  - Results: "Video transmission from the remote site to the network end on the surgeon's site was 250 ms." / "…thus resulting in 350 ms latency for the entire video pipeline"
  - Location and networking: "A portable 5 G antenna was transferred to the demo area, providing local 5 G coverage." *(single read)*
  - Location and networking: "This was routed to the Internet via Vodafone's Fixed Network, enabling communication with the Trikala site via a UDP connection." *(single read)*
- **Figure(s):** video 1080p25, H264, variable bitrate 1.5–2 Mbps (configured); source 1080i50 10-bit 4:2:2 uncompressed; speed test DL 800 Mbps–1.4 Gbps and UL 60–70 Mbps; control RTT 18 ms; video transmission 250 ms and whole video pipeline 350 ms; distance "some 300 km".
- **Condition:** Demonstration on robotic-surgery **phantoms**, with no patients. 5G access was used **only at the surgeon's site**, through a portable antenna giving local coverage and a Huawei 5G CPE Pro. The robot (hospital) side used wired Gigabit Ethernet and the Vodafone fixed network. Video was sent through Zoom. The bitrate is an encoder setting (VBR), not a measured link throughput. The collaboration included Vodafone Greece, and the surgeon was in Trikala with the robot at Athens Medical Centre.
- **Use in paper:** Published surgical-video stream rate for the telesurgery budget, replacing the uncited "15 Mbit/s".
- **Status:** VERIFIED

### STR-06b  4K clinical video requirement and measured 5G SA rates — Chen et al., JMIR 2024
- **Citation:** B. Chen, X. Shi, T. Feng, S. Jiang, Y. Zhai, M. Ren, D. Liu, C. Wang, J. Gao, "Construction and Application of a Private 5G Standalone Medical Network in a Smart Health Environment: Exploratory Practice From China," J. Med. Internet Res., 26:e52404, 2024. DOI 10.2196/52404.
- **Fetched URL:** https://www.jmir.org/2024/1/e52404/PDF
- **Location:** Table 3, "The feasibility of the 5G-enabled robot-assisted mobile ward rounds." Columns: Items and requirements of typical applications | Indicators | Basic needs | 4G | 5G SA. Also Results (ward rounds; remote ultrasound).
- **Quote:**
  - Table 3: "High-definition lossless transmission of patient's 4K video | Uplink | 36 Mbps | 20 Mbps | 91 Mbps"
  - Table 3: "High-definition lossless transmission of doctor's 4K video | Downlink | 36 Mbps | 20 Mbps | 91 Mbps"
  - Table 3: "No-sense real-time transmission of control information | Latency | 10 ms | 20-30 ms | 1 ms"
  - Results: "The field test results showed a peak 5G download rate of 918 Mbps and an average download rate of 790 Mbps. The peak upload rate was 94.15 Mbps, with an average upload rate of 91 Mbps."
  - Results: "For remote ultrasound, the average downlink rate of the 5G network is 4.82 Mbps, and the average uplink rate is 2 Mbps, with an average fluctuation of approximately 8 ms."
- **Figure(s):** 4K video "Basic needs" 36 Mbps (uplink and downlink); control latency need 10 ms; field-test 5G SA average download 790 Mbps and upload 91 Mbps; remote ultrasound average downlink 4.82 Mbps and uplink 2 Mbps.
- **Condition:** Private 5G SA hospital network in China. The 36 Mbps figure is a **requirement ("Basic needs") for robot-assisted mobile ward rounds, not surgery**. The 4G and 5G SA columns are network rates, not the video's own bitrate. The remote-ultrasound rates are measured service averages. An earlier read garbled the "4.82" sentence, and a later read resolved it to the wording above.
- **Use in paper:** Upper-bound 4K clinical video rate (requirement), set against STR-06's configured 1080p rate.
- **Status:** VERIFIED

### STR-06c  Clinical 5G telerobotic surgery — Tian et al., Neurospine 2020 (latency only)
- **Citation:** W. Tian, M. Fan, C. Zeng, Y. Liu, D. He, Q. Zhang, "Telerobotic Spinal Surgery Based on 5G Network: The First 12 Cases," Neurospine, 17(1):114–120, 2020. DOI 10.14245/ns.1938454.227.
- **Fetched URL:** https://www.e-neurospine.org/journal/view.php?doi=10.14245%2Fns.1938454.227
- **Location:** Methods ("Equipment and Personnel Arrangement of 5G Telerobotic Spinal Surgery"); Results
- **Quote:**
  - Results: "The mean network latency of all these operations was 28 ms, reported by China Telecom."
  - Methods: "The 5G network: telecommunication network and equipment were provided and established by China Telecom (Beijing, China) and Huawei Technologies Co., Ltd."
- **Figure(s):** mean network latency 28 ms. **No video bitrate or resolution is stated.**
- **Condition:** Live clinical telerobotic spinal surgery on 12 patients over an operator 5G network, in multiple cities in China, in 2019.
- **Use in paper:** Clinical 5G latency reference only. It gives no stream rate.
- **Status:** VERIFIED (latency). The video bitrate is NOT-FOUND in this paper.
- **Other STR-06 candidates tried and NOT-FOUND:**
  - Lacy et al., BJS 106(12):1576–1579, 2019 (DOI 10.1002/bjs.11364): the OUP page shows only the abstract and the Wiley PDF returned 403.
  - Hara et al., IJCARS 2026 (DOI 10.1007/s11548-026-03738-5): paywalled, and the abstract gives latency only.
  - Li et al., Surg. Endosc. 38:1592–1599, 2024 (DOI 10.1007/s00464-023-10585-x): paywalled.
  - Current Urology 2023 5G wireless endoscopy review: LWW returned 402, PMC10489199 served a reCAPTCHA, and Europe PMC was rejected with 429.
  - Morohashi et al., Surg. Today 52:705–714, 2022: fetched, but it used a commercial wired/VPN network rather than 5G and states no video bitrate.

### STR-07  5G-connected ambulance field test — Berlet et al., JMIR Formative Research 2022
- **Citation:** M. Berlet, T. Vogel, M. Gharba, J. Eichinger, E. Schulz, H. Friess, D. Wilhelm, D. Ostler, M. Kranzfelder, "Emergency Telemedicine Mobile Ultrasounds Using a 5G-Enabled Application: Development and Usability Study," JMIR Formative Research, 6(5):e36824, 2022. DOI 10.2196/36824.
- **Fetched URL:** https://formative.jmir.org/2022/5/e36824/PDF. The HTML page at https://formative.jmir.org/2022/5/e36824 rendered empty.
- **Location:** Section "The 5G Field Test" (Methods and Results); Abstract
- **Quote:**
  - Results: "The measured average throughput for the ultrasound image traffic is approximately 4 Mbps and for the video stream 12 Mbps."
  - Results: "The measured average E2E round trip latency, including RAN and core for the data traffic of the two applications is approximately 10 milliseconds."
  - The 5G Field Test: "…first, a mobile ultrasound application providing imaging of the patient with average uplink required service throughput of 5 Mbps, and second, a camera video stream application showing the inside of the ambulance car (patient and doctor) as well as the remote hospital site with average uplink of 10 Mbps and downlink required service throughput of 5 Mbps."
  - Results: "Without core slicing, the throughput for the video application was reduced to 8 Mbps after the additional uplink traffic was added."
  - The 5G Field Test: "Additionally, the latency increased up to 400 milliseconds (Figures 3 and 4)."
  - Methods: "The ambulance car was parked in a position of line of sight with the gNB antenna with small buildings located in between as well as cars and pedestrians passing by during the test."
- **Figure(s):** measured ultrasound ≈4 Mbps and video stream 12 Mbps; required uplink 5 Mbps (ultrasound) and 10 Mbps (video), plus 5 Mbps video downlink; E2E RTT ≈10 ms; without core slicing, video fell to 8 Mbps and latency rose up to 400 ms.
- **Condition:** 5G field test in Munich, Germany, with the ambulance **parked (stationary)** in line of sight of the gNB, so this is not a moving transport. The core network was in a cloud data centre at the remote hospital site, and core network slicing was used. Per Methods, the carrier was 3.41 GHz. The channel-bandwidth figure in the same sentence renders as "40 Hz" in the text layer and is not used. It is a usability study, and the collected quotes do not establish whether real patients were transported.
- **Use in paper:** Published ambulance video and ultrasound stream rates, replacing the uncited "4 Mbit/s". Also gives a measured 5G RTT for prehospital links.
- **Status:** VERIFIED

### STR-07b  Prehospital "remote first aid" over private 5G SA — Chen et al., JMIR 2024 (qualitative only)
- **Citation:** as STR-06b (J. Med. Internet Res., 26:e52404, 2024; DOI 10.2196/52404).
- **Fetched URL:** https://www.jmir.org/2024/1/e52404/PDF
- **Location:** Results, "Remote Prehospital First Aid"; Figure 8 caption
- **Quote:**
  - "The upstream bandwidth of 4G was clearly insufficient compared with 5G, exhibiting poor delay stability and a significant range of fluctuations, especially during regional boundary switches." *(single read)*
  - Figure 8 caption: "Comparison of uplink and downlink average service bandwidth of the 4G/5G-enabled remote first aid service at static/dynamic status." *(single read)*
- **Figure(s):** None in the text. The numeric values appear only in Figure 8 (graphic), which was not read.
- **Condition:** Private 5G SA network in China; ambulance/first-aid service, static and moving.
- **Use in paper:** Qualitative support only. It is not usable as a rate.
- **Status:** VERIFIED (qualitative). Numeric figure NOT-FOUND in text.

### STR-08  Continuous EEG in the ICU — Herman et al. 2015 consensus, Part II (technical specifications)
- **Citation:** S. T. Herman, N. S. Abend, T. P. Bleck, K. E. Chapman, F. W. Drislane, R. G. Emerson, E. E. Gerard, C. D. Hahn, A. M. Husain, P. W. Kaplan, S. M. LaRoche, M. R. Nuwer, M. Quigg, J. J. Riviello, S. E. Schmitt, L. A. Simmons, T. N. Tsuchida, L. J. Hirsch, "Consensus Statement on Continuous EEG in Critically Ill Adults and Children, Part II: Personnel, Technical Specifications, and Clinical Practice," J. Clin. Neurophysiol., 32(2):96–108, 2015. DOI 10.1097/WNP.0000000000000165.
- **Fetched URL:** https://escholarship.org/content/qt0747z73t/qt0747z73t.pdf. It was cross-checked against the second eScholarship copy, https://escholarship.org/content/qt1x0769kc/qt1x0769kc.pdf.
- **Location:**
  - "Critical Care Continuous EEG Acquisition Machines" (p. 99)
  - "Networking, Remote Access, and Data Storage Equipment" (p. 101)
  - "Initiation of Critical Care Continuous EEG" (p. 103; one read gave p. 102)
  - Table 1 (p. 102)
- **Quote:**
  - p. 103: "Standard CCEEG requires a minimum of 16 electrodes placed according to the 10-20 International System, with placement designed to optimize brain regions sampled (e.g., Fp1, Fp2, C3, C4, O1, O2, T3, T4)."
  - p. 103: "Fewer than 16 EEG channels may be used for rapid screening of EEG in emergency situations, but adequate EEG recording (i.e., >16 electrodes) should be instituted as soon as possible."
  - p. 99: "Typical equipment can record and locally store 5 to 7 days of 32 or more channels of EEG plus digital video."
  - p. 99: "Hard drive capacity should be sufficient for storage of at least 24 hours of continuous video and EEG data."
  - p. 99: "All machines should have network connectivity and network interface card with 100 megabits per second minimum."
  - p. 99: "Rapid EEG and video review will usually require at least 1 gigabit per second."
  - p. 101: "Example: 12 GB/day (video 1 EEG) · 8 machines · 30 days ¼ 2880 GB or w3 TB." This is exactly as rendered by the PDF text layer. In LWW PDFs, "¼" and "w" are glyph substitutions (read by the fetch tool as "=" and "≈"). The "1" between "video" and "EEG" is presumably "+", which is **not verified**.
  - Table 1 (p. 102): "Suspected NCS: discontinue after 24–48 hours if no seizures occur" (partial cell)
- **Figure(s):** minimum 16 electrodes (10-20 system); >16 electrodes for adequate recording; typical equipment 32 or more channels of EEG plus video for 5–7 days; ≥24 h local storage; NIC ≥100 Mbit/s; ≥1 Gbit/s for rapid review; 12 GB/day (video and EEG) per-machine example. **No sampling rate or bit depth is stated.** The searched terms "Hz", "bits" and "digitization" gave no hits. **"21 electrodes" / "full montage" is not stated** here; see STR-02 for 21 electrodes.
- **Condition:** ICU continuous EEG with synchronized video (CCEEG), adults and children. The 12 GB/day figure is a storage-sizing example that includes video.
- **Use in paper:** ICU cEEG channel count and data-volume basis. The 12 GB/day figure is a published per-bed volume that includes video.
- **Status:** VERIFIED

### STR-08b  Continuous EEG duration — Herman et al. 2015 consensus, Part I (indications)
- **Citation:** S. T. Herman et al. (same author group as STR-08), "Consensus Statement on Continuous EEG in Critically Ill Adults and Children, Part I: Indications," J. Clin. Neurophysiol., 32(2):87–95, 2015. DOI 10.1097/WNP.0000000000000166 (Crossref).
- **Fetched URL:** https://www.acns.org/UserFiles/file/Consensus_Statement_on_Continuous_EEG_in.1.pdf
- **Location:** "Diagnosis of Nonconvulsive Seizures…" (timing and duration), p. 90. The general "minimum of 24 hours" sentence was located inconsistently: one read gave the "Indications for Critical Care Continuous EEG" section, p. 88, and another gave the "Introduction", p. 90.
- **Quote:**
  - p. 90: "Recording for at least 24 hours is recommended, but there may be situations in which shorter or longer periods of recording are necessary."
  - p. 90: "About 80% to 95% of patients with NCS can be identified within 24 to 48 hours."
  - p. 90: "In specific populations, such as patients who are comatose, have periodic discharges, or are pharmacologically sedated, NCS may occur later and more prolonged monitoring (48 hours or more) may be needed."
  - General statement (p. 88 or 90): "For most indications, recording for a minimum of 24 hours is recommended, but shorter or longer recording may be needed for selected populations."
- **Figure(s):** at least 24 hours (minimum for most indications); 80%–95% of NCS identified within 24 to 48 hours; 48 hours or more in selected populations.
- **Condition:** Recommended cEEG duration for detecting nonconvulsive seizures in critically ill adults and children.
- **Use in paper:** Session duration for the cEEG key-consumption budget (per-session versus per-day volume).
- **Status:** VERIFIED
