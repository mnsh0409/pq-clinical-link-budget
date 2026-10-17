"""
x3_model.py -- a-priori model of the telemetry experiment X3 (testbed/x3.py): late records per handover interruption from
the interruption length, the round trip, the configuration's cold handshake time and the client's recovery policy.
No parameter is taken from the telemetry runs.

Inputs (onset of the interruption = time 0; all in ms):
  D       interruption length (drawn from the NSA T2 pool by the run's seed)
  H       cold connect-to-first-record time of the configuration on the same link profile (X12, Table III)
  RTT, OWD  round trip and one-way delay of the profile
  PTO = srtt + max(4 rttvar, 1 ms) + 25 ms (tele.c), with srtt ~ RTT + SRTT_EXTRA (host turnaround per sample) and the
        variation term at its 1-ms floor once the estimator has settled: PTO ~ RTT + 25 + SRTT_EXTRA + 1
  g0      generation time of the oldest record whose acknowledgment the interruption swallows. A record sent at g reaches
          the emulator at ~g and its acknowledgment comes back through the emulator at ~g + OWD, so the first record left
          unacknowledged is the first with g + OWD >= 0: g0 is uniform on [-OWD, PERIOD - OWD) over the record phase.
Mechanism (tele.c, policy detect): the loss is declared at T = g0 + PTO; connection attempts start at T and repeat every
PTO while the link is down (each failed attempt is a SYN dropped in the interruption); the first attempt at or after D
succeeds and the backlog reaches the server at t1 = T + n PTO + H, n = ceil((D - T)/PTO) if T < D else 0. A record
generated before the onset (g0 < 0) was delivered on time (its frame entered the emulator before the interruption; only
its acknowledgment was lost), so the undelivered records are those generated at g >= max(g0, 0), on the 16-ms grid of
g0; those with t1 - g > DEADLINE are late (the backlog drains in a few ms at the 5G rates). The expected count averages
the integer count over g0.
"""
import math
import numpy as np
PERIOD_MS, DEADLINE_MS, MARGIN_MS, SRTT_EXTRA_MS, RTTVAR_FLOOR_MS = 16.0, 100.0, 25.0, 0.5, 1.0

def pto_ms(rtt_ms):
    return rtt_ms + SRTT_EXTRA_MS + RTTVAR_FLOOR_MS + MARGIN_MS

def late_for_phase(D, H, rtt, g0):
    pto = pto_ms(rtt); T = g0 + pto
    n = 0 if T >= D else math.ceil((D - T) / pto)
    t1 = T + n * pto + H
    g_first = g0 if g0 >= 0 else g0 + PERIOD_MS          # first undelivered record (g0 > -PERIOD always, as OWD < PERIOD)
    L = t1 - DEADLINE_MS - g_first
    return (0 if L < 0 else math.floor(L / PERIOD_MS) + 1), n, T

def late_expect(D, H, rtt, owd, step=0.25):
    """Expected late records per interruption, averaged over the record phase; also the expected failed attempts."""
    G = np.arange(-owd, PERIOD_MS - owd, step)
    out = [late_for_phase(D, H, rtt, g0) for g0 in G]
    return float(np.mean([o[0] for o in out])), float(np.mean([o[1] for o in out])), float(np.mean([o[2] for o in out]))

def late_by_retries(H, rtt, owd, n, step=0.25):
    """Expected late records when exactly n retries are needed (the boundary table of the paper)."""
    pto = pto_ms(rtt); G = np.arange(-owd, PERIOD_MS - owd, step)
    vals = []
    for g0 in G:
        g_first = g0 if g0 >= 0 else g0 + PERIOD_MS
        L = (g0 + pto) + n * pto + H - DEADLINE_MS - g_first
        vals.append(0 if L < 0 else math.floor(L / PERIOD_MS) + 1)
    return float(np.mean(vals))
