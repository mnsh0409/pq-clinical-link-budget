"""
linkemu.py -- user-space L2 link emulator between two interfaces (run inside the router netns).

The kernel here has no netem, so delay, per-direction serialization rate and outage windows are
applied in user space: every frame arriving on one side is queued FIFO behind earlier frames of the
same direction (serialization at the direction's rate), then delivered after the one-way delay.
Frames that arrive during an outage window are dropped (data plane halted, as in a handover's
execution stage). Every frame is logged: t_in, direction, frame bytes, t_out (or -1 if dropped).

usage: python3 linkemu.py IF_A IF_B --ab-rate R --ba-rate R --ab-delay-ms D --ba-delay-ms D
                          [--outages FILE] [--log FILE]
A->B is "uplink" when A faces the client.
"""
import argparse, heapq, json, os, select, socket, sys, time

ETH_P_ALL = 0x0003
PACKET_OUTGOING = 4

ap = argparse.ArgumentParser()
ap.add_argument("a"); ap.add_argument("b")
ap.add_argument("--ab-rate", type=float, required=True)
ap.add_argument("--ba-rate", type=float, required=True)
ap.add_argument("--ab-delay-ms", type=float, required=True)
ap.add_argument("--ba-delay-ms", type=float, required=True)
ap.add_argument("--outages", default=None, help="file with lines 'start_s end_s' relative to the time the file is (re)read; re-read on change")
ap.add_argument("--log", default=None)
ap.add_argument("--outages-abs", action="store_true", help="outage times are absolute CLOCK_MONOTONIC seconds")
args = ap.parse_args()

def raw(ifname):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    s.bind((ifname, 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 << 20)
    s.setblocking(False)
    return s

sa, sb = raw(args.a), raw(args.b)
out = {sa: sb, sb: sa}
cfg = {sa: ("AB", args.ab_rate, args.ab_delay_ms / 1e3), sb: ("BA", args.ba_rate, args.ba_delay_ms / 1e3)}
busy = {"AB": 0.0, "BA": 0.0}
heap, seq = [], 0
logf = open(args.log, "w") if args.log else None
outages, out_mtime = [], None

def load_outages():
    global outages, out_mtime
    if not args.outages or not os.path.exists(args.outages):
        return
    m = os.path.getmtime(args.outages)
    if m != out_mtime:
        out_mtime = m
        now = time.monotonic()
        outages = []
        for line in open(args.outages):
            if line.strip():
                a, b = map(float, line.split()[:2])
                outages.append((a, b) if args.outages_abs else (now + a, now + b))

def tcpinfo(frame):
    """(src_port, dst_port, tcp_payload_bytes) for IPv4/TCP frames, else None."""
    if len(frame) < 54 or frame[12:14] != b"\x08\x00" or frame[23] != 6:
        return None
    ihl = (frame[14] & 0x0F) * 4
    tot = int.from_bytes(frame[16:18], "big")
    t = 14 + ihl
    sp, dp = int.from_bytes(frame[t:t+2], "big"), int.from_bytes(frame[t+2:t+4], "big")
    doff = (frame[t+12] >> 4) * 4
    return sp, dp, tot - ihl - doff

def in_outage(t):
    return any(a <= t < b for a, b in outages)

last_check = 0.0
while True:
    now = time.monotonic()
    if now - last_check > 0.05:
        load_outages(); last_check = now
    timeout = max(0.0, heap[0][0] - now) if heap else 0.05
    r, _, _ = select.select([sa, sb], [], [], min(timeout, 0.05))
    for s in r:
        while True:
            try:
                frame, addr = s.recvfrom(65535)
            except BlockingIOError:
                break
            if addr[2] == PACKET_OUTGOING:
                continue
            t_in = time.monotonic()
            d, rate, delay = cfg[s]
            if in_outage(t_in):
                if logf: ti = tcpinfo(frame); logf.write(f"{t_in:.6f} {d} {len(frame)} -1 {ti[0] if ti else 0} {ti[1] if ti else 0} {ti[2] if ti else -1}\n")
                continue
            start = max(t_in, busy[d])
            done = start + len(frame) * 8 / rate
            busy[d] = done
            t_out = done + delay
            seq += 1
            heapq.heappush(heap, (t_out, seq, out[s], frame, t_in, d))
    now = time.monotonic()
    while heap and heap[0][0] <= now:
        t_out, sq, so, frame, t_in, d = heapq.heappop(heap)
        try:
            so.send(frame)
        except (BlockingIOError, OSError):      # veth queue full (ENOBUFS/EAGAIN): retry shortly, keep order
            heapq.heappush(heap, (t_out + 0.0002, sq, so, frame, t_in, d))
            break
        if logf: ti = tcpinfo(frame); logf.write(f"{t_in:.6f} {d} {len(frame)} {time.monotonic():.6f} {ti[0] if ti else 0} {ti[1] if ti else 0} {ti[2] if ti else -1}\n")
    if logf: logf.flush()
