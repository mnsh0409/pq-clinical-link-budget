# sources/: the parameter ledger

Every input number in the paper is a ledger entry: a value copied from a public primary source, with the
source's own words, its location and the condition it applies to. The model scripts read only
`ledger.json`; the `.md` files hold the evidence behind each entry.

## Rules

1. **Public primary sources only.** Standards (3GPP, ETSI, IEEE, IETF, NIST), peer-reviewed papers and their
   arXiv or ePrint versions, official project repositories (pqm4, liboqs). No lecture material.
2. **Quote, don't recall.** Each value is copied verbatim from a fetched page, with its section, table or page.
   A page that could not be fetched is marked `NOT-FOUND` and its value is not used.
3. **No arithmetic in the ledger.** The ledger holds what the source says, in the source's units. Every derived
   number is computed in `models/` and names the ledger ids it combines.
4. **Label the condition.** Lab or deployed, measured or simulated, board and clock, release, carrier.
5. **Status.** `VERIFIED`: quoted from the primary document. `SECONDARY`: quoted from a document that cites the
   primary; both are named.

Access date: 2026-09-27 unless an entry states otherwise.

## Files

| File | Ids | Covers |
|---|---|---|
| `constrained-pqc-links.md` | PQC, LNK, RFC, TB | FIPS 203/204 sizes, pqm4 cycle counts, PQ-TLS on Cortex-M4, link-layer rates and frame limits, TLS/DTLS/QUIC/TCP RFCs, testbed software versions |
| `medical-urllc.md` | MED | 3GPP TS 22.104 and TR 22.826 medical service requirements, tactile-Internet requirements |
| `clinical-streams.md` | STR | Physiological stream rates, clinical 5G measurements |
| `mobility-5g-security.md` | MOB, SEC | Handover measurements, TS 33.501 key handling, 3GPP PQC study status, hybrid TLS key shares |
| `ntn.md` | NTN | 3GPP non-terrestrial reference parameters (read by the scripts, not used in the paper's results) |
| `ledger.json` | all | 229 parameters and 55 citations, written by `models/build_ledger.py` |

## `ledger.json` format

```json
"tls_hs_bytes_dil3_kyb3": {
  "value": 20224,
  "unit": "byte",
  "id": "PQC-05",
  "status": "VERIFIED",
  "condition": "Dilithium3 + Kyber768 (pre-FIPS analogues of ML-DSA-65 + ML-KEM-768; ...)",
  "cite": "tasopoulos2022"
}
```

`models/common.py` loads it: `p("tls_hs_bytes_dil3_kyb3")` returns the value, `cid(...)` the ledger id.
`cites` maps each citation key to the full reference.

## Tracing a number back to its source

Example: the paper's 20,224-B fully post-quantum handshake.

1. `ledger.json` key `tls_hs_bytes_dil3_kyb3` gives the value, the id `PQC-05` and the citation `tasopoulos2022`.
2. `constrained-pqc-links.md`, section `### PQC-05`, gives the citation, the fetched URL, the location
   (Table 2 of the ISPEC 2022 paper) and the verbatim quote.
3. `grep -rn tls_hs_bytes_dil3_kyb3 ../models` shows every script that uses it.

## Entry template (`.md` files)

```
### <id>
- **Citation:** Authors, "Title," Venue, vol(issue):pages, year. DOI/URL.
- **Fetched URL:** <exact URL that returned the text>
- **Location:** <section / table / page / figure>
- **Quote:** "<verbatim, at most 60 words, with the figure inside it>"
- **Figure(s):** <value and unit, exactly as quoted>
- **Condition:** <what the figure applies to>
- **Use in paper:** <where it is used>
- **Status:** VERIFIED | SECONDARY (via ...) | NOT-FOUND (tried ...)
```
