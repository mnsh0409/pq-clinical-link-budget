# Testbed: X1 (bytes per flight), X2 (time to first record), X3 (telemetry through handovers), X4 (QUIC)

Everything runs on one Linux machine as root, in three network namespaces:

```
cli (10.9.0.1) --veth-- [ rt: linkemu.py ] --veth-- srv (10.9.0.2)
```

`linkemu.py` is a user-space link emulator. It adds a one-way delay, a serialization rate per direction
(client to server = uplink) and outage windows (frames dropped), and it logs every frame. It exists because
the kernel used for the paper had no `netem`. With `netem`, `tc` would also work, but the byte log would then
have to come from `tcpdump`.

## Requirements

- Linux with root, `iproute2` (`ip`), `ethtool`, `gcc`, `cmake`, `git`, Python 3 with `numpy` and `pandas`.
  On Windows, use WSL2 (Ubuntu) and run everything with `sudo`.
- OpenSSL 3.5.4 in `/opt/ossl35` (ML-KEM-768, ML-DSA-65 and X25519MLKEM768 are built in):
  ```bash
  curl -LO https://github.com/openssl/openssl/releases/download/openssl-3.5.4/openssl-3.5.4.tar.gz
  sha256sum openssl-3.5.4.tar.gz   # 967311f84955316969bdb1d8d4b983718ef42338639c621ec4c34fddef355e99
  tar xzf openssl-3.5.4.tar.gz && cd openssl-3.5.4
  ./Configure --prefix=/opt/ossl35 --libdir=lib no-docs no-tests shared -O2 && make -j"$(nproc)" && sudo make install_sw
  sudo mkdir -p /opt/ossl35/ssl && sudo cp apps/openssl.cnf /opt/ossl35/ssl/
  ```
- Only for the Falcon-512 configurations (C3): liboqs 0.16.0 and oqs-provider 0.12.0, built against that OpenSSL.
  oqs-provider exposes the round-3 Falcon-512 (FN-DSA is not yet published as FIPS 206) under the experimental
  TLS code point 0xfed7.
  ```bash
  git clone https://github.com/open-quantum-safe/liboqs && git -C liboqs checkout 5a1a854b0dc9f2141bdc771c555ee60c37950183   # tag 0.16.0
  cmake -S liboqs -B liboqs/build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DOQS_BUILD_ONLY_LIB=ON \
        -DOQS_USE_OPENSSL=ON -DOPENSSL_ROOT_DIR=/opt/ossl35 -DCMAKE_INSTALL_PREFIX=/opt/oqs \
        "-DOQS_MINIMAL_BUILD=SIG_falcon_512;SIG_ml_dsa_44;SIG_ml_dsa_65;KEM_ml_kem_768"
  cmake --build liboqs/build -j"$(nproc)" && sudo cmake --install liboqs/build
  git clone https://github.com/open-quantum-safe/oqs-provider && git -C oqs-provider checkout 7e9d095aff7967fab9a8ce693e3da5357dc59d58   # tag 0.12.0
  cmake -S oqs-provider -B oqs-provider/build -DCMAKE_BUILD_TYPE=Release -DOPENSSL_ROOT_DIR=/opt/ossl35 \
        -Dliboqs_DIR=/opt/oqs/lib/cmake/liboqs
  cmake --build oqs-provider/build -j"$(nproc)"
  sudo cp oqs-provider/build/lib/oqsprovider.so /opt/ossl35/lib/ossl-modules/
  ```
  `oqs.cnf` loads the default and oqs providers; `run.py` sets `OPENSSL_CONF` to it for the Falcon
  configurations only, so the other configurations send the same ClientHello as without the provider.
- Layout: `testbed/` next to `models/` (for `common.p`, which reads `sources/ledger.json`) and `data/`
  (X3 reads the SIGCOMM'22 handover file from `data/sigcomm22-5g-mobility`; see `data/README.md`).

## One-time setup

```bash
cd testbed
(cd pki && bash mkpki.sh)                                          # P-256 and ML-DSA-65: root, intermediate, server and client leaves
(cd pki && OPENSSL_CONF=$PWD/../oqs.cnf FAMS=falcon bash mkpki.sh)  # Falcon-512 (needs oqs-provider)
(cd pki && MIXED=1 FAMS= bash mkpki.sh)                            # C3m: Falcon root/intermediate/server, ML-DSA-65 device (chains included)
for f in ec mldsa falcon; do
  cat pki/$f/srv.byint.crt pki/$f/int.crt > pki/$f/srv.chain3.pem
  cat pki/$f/cli.byint.crt pki/$f/int.crt > pki/$f/cli.chain3.pem
done
for b in hs tele quic; do gcc -O2 -o $b $b.c -I/opt/ossl35/include -L/opt/ossl35/lib -lssl -lcrypto -Wl,-rpath,/opt/ossl35/lib; done
sudo bash netns_up.sh        # x12.py, x3.py and x4.py also call this themselves
```

The keys and certificates are generated locally and are not part of the repository. All programs set
`SSL_MODE_NO_AUTO_CHAIN`: without it OpenSSL also sends the root CA certificate (about 5.5 kB more per side
with ML-DSA-65); `AUTOCHAIN=1 ./hs ...` reproduces that default.

Scratch files (emulator logs, X3 outage schedules and server output) go to `$TESTBED_TMP`
(default: `pqtb` under the system temporary directory). `cleanup.sh` kills emulator and endpoint processes
left over from an interrupted cell.

## Configurations (`run.py: CONFIGS`)

| Name | Key exchange | Certificates and signatures | Client authentication |
|---|---|---|---|
| C0 | secp256r1 ECDHE | ECDSA P-256 | mutual |
| C1 | X25519MLKEM768 | ECDSA P-256 | mutual |
| C2 | ML-KEM-768 | ML-DSA-65 | mutual |
| C2u | ML-KEM-768 | ML-DSA-65 | server only |
| C3 | ML-KEM-768 | Falcon-512 | mutual |
| C3u | ML-KEM-768 | Falcon-512 | server only |
| C3m | ML-KEM-768 | Falcon-512 server and CA, ML-DSA-65 device certificate | mutual |

`chain=2`: each side sends its leaf only (the peer holds the root). `chain=3`: leaf and intermediate.

## X1 + X2: bytes per flight and time to the first authenticated record (TCP)

```bash
sudo python3 x12.py                      # all four profiles; or name some: 5G-hosp 5G-tele LTE-M NB-IoT
```

- Each connection is a cold TCP + TLS 1.3 full handshake (no tickets), then one 1,000-B application record.
  `t_first_record_ms` = server-side read of that record minus the client's `connect()` call (one clock).
- Profiles take their rates and RTTs from the ledger: 5G-hosp UL 91 / DL 790 Mb/s, RTT 10 ms; 5G-tele UL 101 /
  DL 177 Mb/s, RTT 18 ms; LTE-M UL 380 / DL 300 kb/s and NB-IoT UL 66 / DL 26 kb/s with an **assumed** 10 ms RTT
  (the ledger has no measured RTT for them), so those rows isolate serialization.
- Output: `results/testbed_x12.json`. Per cell: the first connection's flights (direction, TCP payload bytes,
  segments) and timing quantiles. Handshake bytes = flight payload minus the client's 1,022-B application
  record (1,000 + 5 + 16 + 1) and the server's 24-B close_notify.

## X4: QUIC (OpenSSL 3.5 client and server)

```bash
sudo python3 x4.py 50                    # 50 connections per cell, 5G profiles, with and without Retry
```

- Does the server's first flight exceed QUIC's anti-amplification limit (three times the bytes received before
  address validation), and what does address validation with Retry add?
- Output: `results/testbed_x4.json`. Byte counts there are **Ethernet frame bytes** (UDP payload + 42 B per
  datagram). With an ML-KEM-768 key share the client's Initial takes two datagrams (2 x 1,200 B of UDP payload,
  2 x 1,242 B of frames), and the C2 server sends exactly three times that (7,200 B of UDP payload) before it
  waits for the client; `models/testbed_tables.py` converts to UDP payload for the paper.

## Timeline: where the TCP flights stall

```bash
sudo python3 timeline.py                 # one cold connection each for C0, C2 and C2 + intermediate (5G-hosp)
```

- From the emulator's per-frame log: each data flight split into bursts at gaps of more than 4 ms, and the stall
  between bursts. Output: `results/testbed_timeline.json`.

## X3: a telemetry stream through measured handover interruptions

```bash
sudo python3 x3.py 5 80                  # 5 runs x 80 s per cell (as in the paper); x3.py 1 25 for a quick check
X3_CELLS="detect:C2:3" X3_PROFILES=5G-tele X3_MERGE=1 sudo -E python3 x3.py 5 80   # rerun one cell and merge it in
```

- Stream: a 1,000-B message generated every 16 ms (0.5 Mb/s, the TR 22.826 cardiac-telemetry target), 100 ms
  deadline from generation to the server's receipt, over TLS 1.3/TCP on the 5G profiles (10 and 18 ms RTT).
  The server acknowledges every message with its 4-byte sequence number.
- Outages: seven per 80-s run, one roughly every 10 s (+/-1 s). Each duration is drawn (seeded, the same in every
  cell, so cells are paired) from the measured NSA primary-cell execution-stage interruptions T2 of the SIGCOMM'22
  artifact.
- Policies (`tele.c`): `keep` (the session and TCP connection survive; TCP recovers on its own); `detect` (the
  session is lost at the outage: the emulator runs with `--kill-flows` and drops the old connection's frames from
  the outage start on; the client is not told, declares the session lost when its oldest unacknowledged message
  has waited one probe timeout, srtt + max(4 rttvar, 1 ms) + 25 ms, the RFC 9002 form with a 25-ms margin chosen
  here, from application-acknowledgment RTT samples with Karn's rule; it reconnects with the same timeout on
  connect and handshake, retries, and resends every unacknowledged message); `detect-resume` (as detect, with
  PSK resumption, psk_dhe_ke). `reconnect` and `resume` are the earlier oracle policies (they read the outage
  file); they are kept in the code but not used in the paper.
- Output: `results/testbed_x3.json`. Per cell and run: per outage, late messages (attributed by generation time
  to the outage whose window [start - 0.5 s, next start - 0.5 s) contains them), time from the outage end to the
  next delivered message, longest delivery gap, detection delay, handshake time, failed attempts; per run, lost
  and duplicate messages. `models/testbed_tables.py` writes Table IV of the paper (`tab5_session.tex`) with the
  excess over `keep` and a two-stage bootstrap 95 % interval (runs, then interruptions), over the windows that
  `x3_qc.py` leaves valid.

## X3 quality control: host stalls

```bash
python3 x3_qc.py                         # reads the emulator logs in $TESTBED_TMP -> results/testbed_x3_qc.json
```

The emulated link has a constant delay, so a frame that `linkemu.py` delivers more than 15 ms after its schedule
means the host did not run the emulator in time. On the 2-vCPU cloud host used for the paper this happened in 72
of 490 interruption windows; such a stall can delay acknowledgments past the probe timeout and trigger a session
loss that the link model does not contain. `x3_qc.py` replays each run's seeded schedule, marks the windows that
contain a stall (the rule looks only at the emulator's timing, never at late records) and also reports
connection requests dropped in an interruption and loss declarations made while the connection was alive.
`models/testbed_tables.py` computes Table IV over each cell's windows without a stall; the excess over the kept
session is the difference of the two cells' means, with a 95 % interval from independent two-stage bootstraps
(runs, then valid interruptions) of the two cells. Running the emulator under `chrt -f 50` with Python's collector disabled did not
remove the stalls in a test.

## Reproducibility notes

- With freshly generated keys, ML-DSA-65 byte counts reproduce exactly. ECDSA and Falcon signatures vary in
  length, so C0, C1 and C3 flights can differ by a few bytes (a rerun gave 885 vs 886 B for the C0 server
  flight and 3,910 vs 3,911 B for C3).
- The script paths (`TESTBED_TMP`, `cleanup.sh`) were parameterized after the first runs. For v1.6 of the paper
  (Oct 17, 2026) the C3m cells, `timeline.py` and the X3 `detect` policies were added and X3 was rerun with
  5 runs per cell; X12/X4 cells measured before were kept (a rerun on Oct 17 reproduced C0, C2, C2 + int. and C3
  over TCP within 0.3 ms of Table III).
- The 5G-tele `detect` C2 cell (no intermediate) was rerun on Oct 17 because a test overwrote its emulator logs,
  which `x3_qc.py` needs.
- The `detect-resume` cells were rerun on Oct 17 after a fix in `tele.c`: the first run freed the lost
  connection without marking it shut down, so OpenSSL marked its session ticket non-resumable and every
  reconnection was a full handshake (resumed share 0). The client now sets the shutdown flags before freeing
  (nothing is sent), and the rerun resumed every reconnection. The other policies use no ticket and were not
  affected.
- In `testbed_x4.json`, the first burst of two cells (5G-hosp C0 and C3 without Retry) is a 42-B frame that is
  not QUIC (the flight parser counts every frame the emulator logs). Their timings are unaffected; the paper uses
  the bursts of the C2 cells only.

## What the testbed does not model

There is no radio MAC, scheduling or 6LoWPAN fragmentation; it tests the protocol and timing model, not the
radio. The user-space emulator and the endpoint cryptography add a roughly constant 1.5 to 4.9 ms per
connection on the 5G profiles (measured time minus the model of round trips plus framed bytes over the rate;
`results/testbed_summary.json`, `model_check_summary`).

## Cleaning up

```bash
sudo ip netns del cli; sudo ip netns del rt; sudo ip netns del srv
```
