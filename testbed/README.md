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
| C2w | ML-KEM-768 | ML-DSA-65 (C2's keys and certificates) | mutual; TCP initial congestion and receive windows of 20 segments on both endpoints (`run.py: IW`, `set_iw`) |

`chain=2`: each side sends its leaf only (the peer holds the root). `chain=3`: leaf and intermediate.

## X1 + X2: bytes per flight and time to the first authenticated record (TCP)

```bash
sudo python3 x12.py                      # all four profiles; or name some: 5G-hosp 5G-tele LTE-M NB-IoT
X12_CASES=C2w:3 sudo -E python3 x12.py   # one case, merged into the existing results (v1.8: C2 + int. with IW 20)
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
TL_CASES=C2w:3 sudo -E python3 timeline.py   # adds C2 + intermediate with IW 20 without rerunning the others
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
  artifact. A run's seed fixes the durations and the onsets relative to the schedule origin; the client's record
  clock starts when the client process does, 0 to 30 ms after that origin (`x3_qc.py`,
  `client_start_after_origin_ms`), so the phase of the 16-ms record grid at an onset is not matched across cells.
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
  and duplicate messages. `models/testbed_tables.py` writes Table IV of the paper (`tab5_session.tex`): the paired
  difference from the lost classical cell (`detect` C0): per interruption (same seed and index), late in the cell
  minus late in C0, averaged over the n windows valid in both cells (n is printed per comparison), with a 95 %
  interval from a two-stage bootstrap of those differences (runs, the independent unit, then interruptions; 10,000
  draws). Each cell's own mean over its own valid windows (`late_per_interruption`) stays in
  `results/testbed_summary.json` but is not printed in the table: the differences use the common windows, so the
  own means do not subtract to them. Two checks are stored with each difference: the same difference over all 35 windows,
  and a t-interval over the five run means (`diff_from_lost_c0_all_windows*`, `diff_from_lost_c0_run_t_ci95`).
  `detect_before_end_share`: share of valid lost-session windows in which the loss was declared before the
  interruption ended (measured from the onset).
- The `keep` cell runs no detector: its row is the ideal of a client that knows its session survived. Its gap to
  `detect` C0 is therefore the cost of losing a session under this particular detector and retry policy (the
  detector fires before most interruptions end, so reconnection attempts go into the interruption), not a
  policy-independent cost of session loss.

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
`models/testbed_tables.py` uses, for the paired difference from `detect` C0, the windows valid in both cells (22 to
29 of 35 per comparison). The `keep` cells lost 7 and 8 of their 35 windows, the other cells 2 to 7; the all-window
check above shows how much the exclusion matters. Running the emulator
under `chrt -f 50` with Python's collector disabled did not remove the stalls in a test, and neither did the
controlled repeat below (the emulator on its own CPU at real-time priority): 20 of 210 windows (9.5 %, against
14.7 % in the development and 5.7 % in the held-out runs).

## X3 held-out block and the model of the late records (v1.8)

`models/x3_model.py` predicts the late records of a `detect` (lost-session) interval from the interruption length,
the profile's RTT and one-way delay, and the configuration's cold connect-to-first-record time H (the X12 median of
Table III); it has no parameter taken from the telemetry runs, but its form was settled on the development runs
(seeds 20261015 to 20261019, `results/testbed_x3.json`). One constant is assumed: 0.5 ms of host turnaround in the
smoothed RTT; `results/testbed_summary.json` (`x3_model.heldout.sensitivity_host_turnaround_ms`) shows the mean
absolute errors with it at 0 to 2 ms.

The held-out test was filed before it was run:

```bash
python3 ../models/x3_prereg.py           # writes results/testbed_x3_heldout_prereg.json (per-interruption predictions)
X3_SEED0=20261020 X3_CELLS="detect:C0:2,detect:C2:3,detect:C2w:3" X3_OUT=$PWD/../results/testbed_x3_heldout.json \
  sudo -E python3 x3.py 5 80             # five new seeds (20261020 to 20261024), both 5G profiles
X3_RESULTS=testbed_x3_heldout.json python3 x3_qc.py   # the unchanged 15-ms host-stall rule -> testbed_x3_heldout_qc.json
python3 ../models/testbed_tables.py      # held-out rows of Table IV, results/testbed_summary.json x3_model.heldout
python3 ../models/fig_model.py           # Fig. 1 of the paper (paper/figs/fig3_model.pdf)
```

- The prediction file was written at 2026-10-17T18:14:24+00:00 (UTC); its SHA-256 is
  `7fc547475ab5a242e9eb027a5a576ac3f010c06a67529f615b78d39c0abdf690`. The block started at 2026-10-17T18:14:51 UTC. A copy of
  the file was placed on a second machine before the runs. `testbed_tables.py` checks that the filed numbers are
  the model's predictions for the drawn interruptions and scores the runs against the filed numbers themselves.
- Outcome on the 198 of 210 windows the unchanged exclusion (host-stall) rule kept: mean absolute
  error 0.58 late records per interval (development: 0.50); every paired 95 % interval contains the
  prediction. C2 + int. minus C0: 0.82 [0.46, 1.20] at 10 ms
  (predicted 0.81) and 2.30 [1.74, 2.84] at 18 ms (predicted
  1.88); C2w minus C0: 0.19 [-0.14, 0.49] and 0.21 [-0.29, 0.87]
  (predicted 0). With the window, as with C0, every late record falls in a window with a failed attempt.
- Negative control in numbers (`x3_model.heldout.cells`, valid windows, 10 / 18 ms): windows with a failed attempt
  were 28 of 34 and 25 of 34 for C0, 26 of 32 and 21 of 29 with the window, 27 of 35 and 24 of 34 for C2 + int.
  Per such window: C0 0.93 and 2.68 late records (model 0.97 and 2.55), the window 1.19 and 3.14 (model 1.01 and 2.59),
  C2 + int. 2.04 and 5.38 (model 1.99 and 4.51). In the windows without one, C0 and the window had no late record at
  either RTT; C2 + int. had none at 10 ms (model 0.32) and 1.60 per window at 18 ms (model 2.08).
- Against the default window, on the same seeds, the window changed the late records of C2 + int. by
  -0.66 [-0.97, -0.35] and -2.18 [-2.78, -1.64] (predicted -0.83 and -1.88). t-intervals over
  the five run means (`run_t_ci95`) also contain every prediction.
- Weak points, also in the paper: the model underestimates C2 + int. at 18 ms by about half a record per
  interruption (development and held-out alike), and it misses the 0.22 of C2 with leaf certificates at 10 ms in
  the development runs (0 predicted; cause not identified). The window runs hold 9 of the 12 excluded held-out
  windows (`exclusions_per_cell`). `x3_qc.py` now also records when each window's first stall came after the onset
  and when the reconnection request passed (`stall_first_ms_after_onset`, `reconnect_syn_ms_after_onset`; the
  `invalid` flags are unchanged): every held-out stall came 0.7 to 8.3 s after the onset, after the
  reconnection, so none coincides with the window's first burst. The largest excluded window (seed 20261021,
  interruption 3 at 18 ms: 35 late records) held a stall about 7.4 s after the onset with false loss declarations
  and six failed attempts. With all windows the 18 ms window contrasts are
  1.54 [-0.06, 4.91] against C0 and -0.86 [-2.34, 2.17] against C2 + int., so at 18 ms both rest on the exclusion. Analysis jobs also ran on the same 2-vCPU host during the held-out block;
  why the stalls fell mostly in the window cells is not known, and a quiet host is the remedy.
- `set_iw` changes the route to the peer in both namespaces (`ip route change ... initcwnd 20 initrwnd 20`) for C2w
  and restores the kernel default for every other case; after an interrupted run, `python3 -c "from run import
  set_iw; set_iw('C0')"` restores it by hand.

## X3 controlled repeat of the 18 ms comparison (v1.9)

In the held-out block the window's 18 ms results rested on the host-stall exclusion (the window runs held 9 of the
12 excluded windows, and analysis jobs ran on the same host). The repeat asks whether the window's benefit holds
with every interval kept, on a host whose scheduling is controlled and recorded. It was filed before it was run:

```bash
python3 ../models/x3_repeat_prereg.py    # predictions, plan, stall attribution rule and run order
                                         #   -> results/testbed_x3_repeat_prereg.json, testbed_x3_repeat_order.json
sudo ./x3_repeat.sh 10 80                # ten new seeds (20261030 to 20261039), 5G-tele only, about 41 minutes
X3_RESULTS=testbed_x3_repeat.json python3 x3_qc.py           # the unchanged 15 ms rule -> testbed_x3_repeat_qc.json
X3_RESULTS=testbed_x3_repeat.json python3 x3_stallclass.py   # the filed attribution -> testbed_x3_repeat_stallclass.json
python3 x3_stalldiag.py                  # post hoc, not filed: did the monitor stall too? -> testbed_x3_repeat_stalldiag.json
python3 ../models/testbed_tables.py      # results/testbed_summary.json x3_model.repeat (checks hashes and run order)
python3 ../models/fig_model.py --repeat ../paper/figs-repeat   # Fig. 1 of v1.9c: the repeat's markers over all intervals
python3 x3_attempts.py                   # post hoc: loss declarations and reconnection attempts against the model's timing
```

- Host control (`x3.py` options, all off by default, so the earlier blocks run exactly as before):
  `X3_EMU_CPU=1 X3_EMU_RT=50` runs the emulator on CPU 1 under SCHED_FIFO priority 50 (`taskset`, `chrt`);
  `X3_EP_CPU=0` pins client, server and monitor to CPU 0; `X3_HOSTMON=1` starts `hostmon.py`, which samples every
  5 ms the emulator's on-CPU time and run-queue wait (`/proc/PID/schedstat`), its state and CPU, and both CPUs'
  jiffies including steal (log `x3_mon_*.log` next to the emulator log); `X3_ORDER=interleave` runs the cells seed by
  seed in the order of `X3_ORDER_FILE`. `x3_repeat.sh` moves every movable process to CPU 0 for the block and
  restores the affinities afterwards; per-CPU kernel threads and interrupt work stay where they are. Its output,
  `results/testbed_x3_repeat_run.log`, holds the affinities, the load and both CPUs' `/proc/stat` lines at the start
  and end (45 s of softirq and 3.7 s of steal time on CPU 1 over the block). During the block only text files
  were edited on the host; no build or analysis output was written. Each run stores `host_control` and `t_start_utc`.
- The prediction file was written at 2026-10-18T00:57:38+00:00 (UTC); its SHA-256 is
  `1bd52b0d9b5407fd1cca6c61a1a04c061fd76a6f971ee5c37fc1664647d47d07`, that of the order file
  `9d7e26569cdf566a454451d2cf0783b67b4c2e91cdb727e65c7882b4fa29c442`. Copies of both were on a second machine at 00:57:58 UTC,
  and the block started at 00:58:33 UTC. The run order was drawn with seed 20261040. Filed plan
  (`analysis_plan`): the exclusion rule unchanged; the three contrasts, paired by seed and interruption, over the
  windows valid in both cells and over all 70; Q1, the window's benefit counts as robust if the all-interval
  C2w minus C2 + int. interval lies below 0; Q2, its remaining penalty is the all-interval C2w minus C0 interval;
  Q3, exclusions per cell, each attributed by the filed rule (`stall_classification`).
- Outcome (`x3_model.repeat.contrasts`; late records per interruption, 95 % two-stage bootstrap intervals):

  | Contrast at 18 ms | all 70 windows | predicted | windows valid in both (n) | predicted |
  |---|---|---:|---|---:|
  | C2 + int. minus C0 | 2.20 [1.71, 2.66] | 1.82 | 2.22 [1.81, 2.66] (59) | 1.81 |
  | C2w minus C2 + int. | -1.96 [-2.50, -1.36] | -1.82 | -2.07 [-2.61, -1.64] (57) | -1.84 |
  | C2w minus C0 | 0.24 [-0.27, 0.84] | 0.00 | 0.21 [-0.02, 0.44] (56) | 0.00 |

  Every bootstrap interval, with and without the exclusions, contains its prediction, and so do the t-intervals over
  the ten run means (`run_t_ci95*`) except those of C2 + int. minus C0 ([1.90, 2.58] and [1.88, 2.52], against 1.81 and
  1.82 predicted: the model's underestimate of the chain, below). Q1: the benefit is robust. Q2: no remaining
  penalty is detectable (equivalence not tested).
- Exclusions (Q3): 20 of 210 windows, 6 for C0, 6 for C2 + int. and 8 for the window, holding
  28 late records each; their first stall came from 4 ms before to 10.7 s after the onset. The filed rule
  attributed 19 of the excluded windows to "idle" stalls (the emulator neither ran, nor waited for a CPU, nor was
  blocked) and 1 to "steal"; over all 35 stall episodes, 31 were "idle" and 4 "steal". No episode was
  "busy", the only class that could come from the emulator's own processing and so from the condition.
- Post hoc (`x3_stalldiag.py`, written after the outcome was known, so not a filed test): the monitor on CPU 0
  took 493,849 samples with a median spacing of 5.0 ms; 58 of its gaps exceeded 15 ms, 29 of them
  during an emulator stall, and 28 of the 35 episodes held such a gap. Both vCPUs stopping together points
  to the virtual machine as a whole being paused, which the steal counter (10 ms jiffies) records only in part (it
  rose between two samples before and 0.1 s after 15 of them). On this cloud host the stalls could be recorded, not
  removed.
- Weak points, also in the paper: the model again underestimates C2 + int. at 18 ms (3.94 observed against
  3.48 per valid window; t-interval of observed minus model over the ten runs [0.10, 0.83]) and the
  window (1.85 against 1.62, [0.02, 0.50]); the window's excess over C0 (0.21 and 0.24) may hide a
  residual of about 0.2 records. One host, one profile, ten runs per condition.
- Post hoc timing check (`x3_attempts.py`, written after the repeat and not filed; output
  `results/testbed_x3_attempt_timing.json`): the client declared the loss about when the model says (condition means
  42.5 to 45.8 ms after the onset at 18 ms, 43.5 to 43.6 ms in the repeat; model 43.5 ms), so the 18 ms misses are not a
  detection delay.
  Failed attempts, however, lasted 49.5 to 51.1 ms at 18 ms (tau = 44.5 ms) and 41.8 to 43.1 ms at 10 ms (tau = 36.5 ms), consistent
  with the socket timeout being rounded up to the kernel's 4 ms tick (`CONFIG_HZ=250` on this host), and the first
  attempt started about 2 ms after the declaration. With these delays measured on the development runs
  (5.7 ms per failed attempt, 2.0 ms first), the model matches the C2 + int. cell at 18 ms (held-out 4.26 observed,
  4.31 modeled; repeat 3.94, 3.93), but it then overpredicts the chain's paired penalty (2.55 against 2.30;
  repeat 2.38 against 2.22) and the window's excess over C0 (0.68 and 0.55 against 0.21 and 0.21). The attempt
  timing explains the chain condition's miss, not the contrasts: at 18 ms the 16 ms steps of the model sit within a
  few milliseconds of all three conditions. Not in the paper (space); a J-BHI item.

## Reproducibility notes

- With freshly generated keys, ML-DSA-65 byte counts reproduce exactly. ECDSA and Falcon signatures vary in
  length, so C0, C1 and C3 flights can differ by a few bytes (a rerun gave 885 vs 886 B for the C0 server
  flight and 3,910 vs 3,911 B for C3).
- v1.9 (Oct 18, 2026) added the controlled repeat above (`hostmon.py`, `x3_stallclass.py`, `x3_stalldiag.py`,
  `x3_repeat.sh`, `models/x3_repeat_prereg.py`; options in `x3.py`, `x3_qc.py` split into reusable functions with
  unchanged output) and the post hoc timing check `x3_attempts.py`; no earlier cell was rerun. Every block ran on a
  two-vCPU cloud virtual machine (KVM); it was restarted before the repeat (booted 00:44:52 UTC on 18 Oct), so the
  blocks need not have run on the same physical host.
- v1.8 (Oct 18, 2026) added the C2w case (X12, timeline) and the held-out X3 block above; the development cells
  were not rerun.
- v1.7 of the paper (Oct 17, 2026) changed only the analysis of X3 (paired difference from `detect` C0 instead of
  the unpaired excess over `keep`); no cell was rerun.
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
