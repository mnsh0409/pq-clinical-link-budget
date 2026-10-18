#!/bin/bash
# x3_repeat.sh -- v1.9: the controlled repeat of the 18 ms comparison (5G-tele; detect C0, C2 + int., C2w + int.),
# run as filed in results/testbed_x3_repeat_prereg.json and results/testbed_x3_repeat_order.json
# (write both first with: python3 ../models/x3_repeat_prereg.py).
# Every other process is moved to CPU 0 for the block and restored afterwards; the emulator runs alone on CPU 1 under
# SCHED_FIFO 50 (x3.py: X3_EMU_CPU, X3_EMU_RT), the endpoints and hostmon.py on CPU 0. Needs root and two CPUs.
# usage: sudo ./x3_repeat.sh [RUNS] [DURATION_S]          (the paper: 10 80; about 41 minutes)
set -u
TB=$(cd "$(dirname "$0")" && pwd); R=$TB/../results
RUNS=${1:-10}; DUR=${2:-80}
date -u +"start %Y-%m-%dT%H:%M:%SZ"
for p in $(ls /proc | grep -E '^[0-9]+$'); do taskset -a -p -c 0 "$p" >/dev/null 2>&1; done      # every other process to CPU 0
echo "affinity of all tasks:"; grep -h Cpus_allowed_list /proc/[0-9]*/status 2>/dev/null | sort | uniq -c
echo "load: $(cat /proc/loadavg)"; grep -E "^cpu[01] " /proc/stat
cd "$TB"
X3_EMU_CPU=1 X3_EMU_RT=50 X3_EP_CPU=0 X3_HOSTMON=1 X3_ORDER=interleave X3_ORDER_FILE=$R/testbed_x3_repeat_order.json \
X3_PROFILES=5G-tele X3_OUT=$R/testbed_x3_repeat.json taskset -c 0 python3 x3.py "$RUNS" "$DUR" 2>&1 | grep -v "disable_ipv6"
rc=${PIPESTATUS[0]}
grep -E "^cpu[01] " /proc/stat
for p in $(ls /proc | grep -E '^[0-9]+$'); do taskset -a -p -c 0-"$(($(nproc) - 1))" "$p" >/dev/null 2>&1; done   # restore
date -u +"end %Y-%m-%dT%H:%M:%SZ rc $rc"
exit "$rc"
