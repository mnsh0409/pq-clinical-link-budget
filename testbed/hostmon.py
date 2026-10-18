"""
hostmon.py -- scheduling monitor for the emulator during an X3 run (v1.9, the controlled repeat; started by x3.py
when X3_HOSTMON=1). It lets each host stall be attributed to the host (the hypervisor or another task took the CPU,
or the emulator was blocked) or to the emulator's own processing.

usage: python3 hostmon.py EMU_PID OUT [PERIOD_MS]          (default period 5 ms; exits when EMU_PID is gone)
Each line: t (CLOCK_MONOTONIC s, the clock of the emulator's log), the emulator's on-CPU time and run-queue wait (ns,
/proc/PID/schedstat), its state letter and current CPU (/proc/PID/stat fields 3 and 39), then for cpu0 and cpu1 the
/proc/stat jiffies user nice system idle iowait irq softirq steal.
"""
import sys, time

pid, out = int(sys.argv[1]), sys.argv[2]
period = (float(sys.argv[3]) if len(sys.argv) > 3 else 5.0) / 1e3
f = open(out, "w")
ss, st = f"/proc/{pid}/schedstat", f"/proc/{pid}/stat"
nxt = time.monotonic()
while True:
    try:
        run_ns, wait_ns = open(ss).read().split()[:2]
        rest = open(st).read().rsplit(")", 1)[1].split()       # fields after the command name
    except (FileNotFoundError, ProcessLookupError, IndexError):
        break
    state, cpu = rest[0], rest[36]                               # field 3 (state) and field 39 (processor)
    cpus = [l.split()[1:9] for l in open("/proc/stat") if l.startswith("cpu") and l[3].isdigit()]
    f.write(f"{time.monotonic():.6f} {run_ns} {wait_ns} {state} {cpu} " + " ".join(" ".join(c) for c in cpus) + "\n")
    nxt += period
    d = nxt - time.monotonic()
    if d > 0:
        time.sleep(d)
    else:
        nxt = time.monotonic()
f.close()
