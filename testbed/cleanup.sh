#!/bin/bash
# Kill emulator and endpoint processes left over from an interrupted cell (called by x12.py and x3.py between cells).
# The bracketed patterns keep pgrep from matching this script's own command line; bash processes are skipped.
for p in $(pgrep -f "linkemu[.]py|testbed/h[s] [sc] |testbed/tel[e] [sc] |testbed/qui[c] [sc] |tcpdum[p] -i c0"); do
  c=$(tr "\0" " " < /proc/$p/cmdline 2>/dev/null)
  case "$c" in *bash\ -c*|*/bin/bash*) continue;; esac
  kill $p 2>/dev/null
done
exit 0
