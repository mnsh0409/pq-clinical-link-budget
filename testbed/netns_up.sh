#!/bin/bash
# Three namespaces: cli -- [rt: linkemu.py] -- srv, bridged at layer 2 in user space.
set -e
for n in cli rt srv; do ip netns del $n 2>/dev/null || true; done
for n in cli rt srv; do ip netns add $n; ip -n $n link set lo up; done
ip link add c0 netns cli type veth peer name r0 netns rt
ip link add s0 netns srv type veth peer name r1 netns rt
ip -n cli addr add 10.9.0.1/24 dev c0
ip -n srv addr add 10.9.0.2/24 dev s0
for pair in "cli c0" "srv s0" "rt r0" "rt r1"; do
  set -- $pair
  ip -n $1 link set $2 up
  ip netns exec $1 ethtool -K $2 tso off gso off gro off tx off rx off >/dev/null 2>&1 || true
done
ip -n rt link set r0 promisc on
ip -n rt link set r1 promisc on
# keep the router kernel out of the path
ip netns exec rt sysctl -qw net.ipv6.conf.all.disable_ipv6=1 || true
for n in cli srv; do ip netns exec $n sysctl -qw net.ipv6.conf.all.disable_ipv6=1 || true; done
echo up
