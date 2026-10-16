"""
run.py -- drive hs (OpenSSL 3.5.4) through linkemu between the cli and srv namespaces.

run_case(profile, cfg, chain, n) starts the emulator with the profile, a server and a client,
captures the client-side interface with tcpdump, and returns per-connection timings and the
TCP payload bytes of every flight (consecutive payload segments in one direction).
"""
import json, os, re, signal, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
PKI = os.path.join(HERE, "pki")
HS = os.path.join(HERE, "hs")
TMP = os.environ.get("TESTBED_TMP", os.path.join(tempfile.gettempdir(), "pqtb")); os.makedirs(TMP, exist_ok=True)   # emulator logs, X3 scratch files
CLEANUP = ["bash", os.path.join(HERE, "cleanup.sh")]   # kills leftover emulator/endpoint processes between cells

CONFIGS = {  # name: (groups, family, mutual)
    "C0":      ("secp256r1",      "ec",    1),
    "C1":      ("X25519MLKEM768", "ec",    1),
    "C2":      ("MLKEM768",       "mldsa", 1),
    "C2u":     ("MLKEM768",       "mldsa", 0),
    "C2h":     ("X25519MLKEM768", "mldsa", 1),
    "C1u":     ("X25519MLKEM768", "ec",    0),
    "C3":      ("MLKEM768",       "falcon", 1),   # Falcon-512 certificates (round-3 Falcon via oqs-provider 0.12.0, experimental code point 0xfed7)
    "C3u":     ("MLKEM768",       "falcon", 0),
}
OQS_CONF = os.path.join(HERE, "oqs.cnf")
def env_for(fam):
    """Falcon needs oqs-provider; other families run without it so their ClientHello is unchanged."""
    e = dict(os.environ)
    if fam == "falcon":
        e["OPENSSL_CONF"] = OQS_CONF
        e["LD_LIBRARY_PATH"] = "/opt/ossl35/lib:/opt/oqs/lib"
    return e

def sh(cmd, **kw):
    return subprocess.Popen(cmd, shell=True, **kw)

def run_case(profile, cfg, chain=2, n=1, gap_ms=50, pcap=True, outages=None, tag=None):
    groups, fam, mutual = CONFIGS[cfg]
    P = os.path.join(PKI, fam)
    tag = tag or f"{profile['name']}_{cfg}_ch{chain}"
    pc = f"{TMP}/emu_{tag}.log"
    port = 4433
    procs = []
    ecmd = ["ip", "netns", "exec", "rt", "python3", f"{HERE}/linkemu.py", "r0", "r1", "--ab-rate", str(profile['ul']), "--ba-rate", str(profile['dl']),
            "--ab-delay-ms", str(profile['owd_ms']), "--ba-delay-ms", str(profile['owd_ms'])] + (["--outages", outages] if outages else []) + ["--log", pc]
    emu = subprocess.Popen(ecmd)
    procs.append(emu)
    time.sleep(0.6)
    scert = f"{P}/srv.byroot.crt"; schain = f"{P}/srv.chain3.pem" if chain == 3 else "-"
    env = env_for(fam)
    srv = subprocess.Popen(["ip", "netns", "exec", "srv", HS, "s", str(port), scert, f"{P}/srv.key", schain, f"{P}/root.crt", groups, str(mutual), str(n)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    srv.stderr.readline()  # ready
    if mutual:
        ccert, ckey = f"{P}/cli.byroot.crt", f"{P}/cli.key"; cchain = f"{P}/cli.chain3.pem" if chain == 3 else "-"
    else:
        ccert = ckey = cchain = "-"
    cli = subprocess.run(["ip", "netns", "exec", "cli", HS, "c", "10.9.0.2", str(port), f"{P}/root.crt", groups, ccert, ckey, cchain, str(n), str(gap_ms)],
                         capture_output=True, text=True, timeout=600, env=env)
    sout, serr = srv.communicate(timeout=60)
    time.sleep(0.3)
    for p in procs:
        p.send_signal(signal.SIGINT)
    for p in procs:
        try: p.wait(timeout=5)
        except subprocess.TimeoutExpired: p.kill()
    if cli.returncode != 0:
        raise RuntimeError(f"client failed: {cli.stderr[:500]}")
    C = [list(map(float, l.split()[1:])) for l in cli.stdout.splitlines() if l.startswith("C ")]
    S = [l.split()[1:] for l in sout.splitlines() if l.startswith("S ")]
    S = [list(map(float, s[:3])) + [s[3]] for s in S]
    res = {"tag": tag, "profile": profile, "cfg": cfg, "groups": groups, "family": fam, "mutual": mutual, "chain": chain, "runs": []}
    for c, s in zip(C, S):
        res["runs"].append({"t_tcp_ms": (c[1] - c[0]) * 1e3, "t_hs_client_ms": (c[2] - c[0]) * 1e3,
                            "t_first_record_server_ms": (s[2] - c[0]) * 1e3, "group": s[3]})
    if pcap:
        res["flights"] = flights(pc)
    return res

def flights(pc):
    """From the emulator log: per connection (client port), flights [direction, TCP payload bytes, segments, t_in_first, t_in_last]."""
    conns = {}
    for line in open(pc):
        f = line.split()
        if len(f) < 7: continue
        t, d, ln, tout, sp, dp, pl = float(f[0]), f[1], int(f[2]), float(f[3]), int(f[4]), int(f[5]), int(f[6])
        if pl < 0: continue
        cport = sp if d == "AB" else dp
        conns.setdefault(cport, []).append((t, "C>S" if d == "AB" else "S>C", pl, tout))
    res = []
    for cport in sorted(conns):
        fl = []
        for t, d, pl, tout in sorted(conns[cport]):
            if pl == 0: continue
            if fl and fl[-1][0] == d:
                fl[-1][1] += pl; fl[-1][2] += 1; fl[-1][4] = t
            else:
                fl.append([d, pl, 1, t, t])
        res.append(fl)
    return res

if __name__ == "__main__":
    prof = {"name": "fast", "ul": 1e9, "dl": 1e9, "owd_ms": 0.5}
    r = run_case(prof, sys.argv[1] if len(sys.argv) > 1 else "C2", chain=int(sys.argv[2]) if len(sys.argv) > 2 else 2, n=1)
    print(json.dumps(r, indent=1))
