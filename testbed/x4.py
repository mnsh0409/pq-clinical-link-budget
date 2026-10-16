"""
x4.py -- X4: QUIC (OpenSSL 3.5 client and server) on the 5G profiles. Does the post-quantum server flight exceed
QUIC's 3x anti-amplification allowance (one more round trip), and what does address validation (Retry) add?
Time to first record = server-side read of the 1,000-B stream message minus the client's SSL_connect() call.
Results -> results/testbed_x4.json.   usage: python3 x4.py [N]
"""
import json, os, signal, statistics, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "models"))
from common import p
from run import CONFIGS, PKI, env_for, TMP

N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
PROFILES = [
    {"name": "5G-hosp", "ul": p("ul_5gsa_chen2024_avg_bps"), "dl": p("dl_5gsa_chen2024_avg_bps"), "owd_ms": p("rtt_5g_berlet2022_ms") / 2},
    {"name": "5G-tele", "ul": p("ul_5g_ye2026_bps"), "dl": p("dl_5g_ye2026_bps"), "owd_ms": p("rtt_5g_moustris2023_ms") / 2},
]
CASES = [("C0", 2), ("C1", 2), ("C2", 2), ("C2u", 2), ("C2", 3), ("C3", 2), ("C3u", 2), ("C3", 3)]

def flights(log):
    """datagram bursts of the first connection: direction, bytes, datagrams (gap > 2 ms or direction change splits)."""
    L = [l.split() for l in open(log) if len(l.split()) >= 4]
    out, t0 = [], None
    for l in L:
        t, d, n = float(l[0]), l[1], int(l[2])
        if t0 is None: t0 = t
        if out and (out[-1][0] != d or (t - out[-1][4]) > 0.002):
            if out[-1][0] == d == "AB" and len(out) > 1 and (t - t0) > 0.15: break
        if out and out[-1][0] == d and (t - out[-1][4]) <= 0.002:
            out[-1][1] += n; out[-1][2] += 1; out[-1][4] = t
        else:
            if out and (t - t0) > 0.15: break      # next connection
            out.append([d, n, 1, round((t - t0) * 1e3, 1), t])
    return [["C>S" if f[0] == "AB" else "S>C", f[1], f[2], f[3]] for f in out]

def run(pr, cfg, chain, validate, n):
    groups, fam, mutual = CONFIGS[cfg]
    P = os.path.join(PKI, fam)
    log = f"{TMP}/x4_{pr['name']}_{cfg}_{chain}_{validate}.log"
    emu = subprocess.Popen(["ip", "netns", "exec", "rt", "python3", f"{HERE}/linkemu.py", "r0", "r1", "--ab-rate", str(pr["ul"]), "--ba-rate", str(pr["dl"]),
                            "--ab-delay-ms", str(pr["owd_ms"]), "--ba-delay-ms", str(pr["owd_ms"]), "--log", log], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    scert = f"{P}/srv.byroot.crt"; schain = f"{P}/srv.chain3.pem" if chain == 3 else "-"
    env = env_for(fam)
    srv = subprocess.Popen(["ip", "netns", "exec", "srv", f"{HERE}/quic", "s", "4433", scert, f"{P}/srv.key", schain, f"{P}/root.crt", groups, str(mutual), str(validate), str(n)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    srv.stderr.readline()
    if mutual:
        cc, ck = f"{P}/cli.byroot.crt", f"{P}/cli.key"; cch = f"{P}/cli.chain3.pem" if chain == 3 else "-"
    else:
        cc = ck = cch = "-"
    cli = subprocess.run(["ip", "netns", "exec", "cli", f"{HERE}/quic", "c", "10.9.0.2", "4433", f"{P}/root.crt", groups, cc, ck, cch, str(n), "100"],
                         capture_output=True, text=True, timeout=600, env=env)
    try: sout, _ = srv.communicate(timeout=30)
    except subprocess.TimeoutExpired: srv.kill(); sout, _ = srv.communicate()
    emu.send_signal(signal.SIGINT)
    try: emu.wait(timeout=5)
    except subprocess.TimeoutExpired: emu.kill()
    C = [list(map(float, l.split()[1:])) for l in cli.stdout.splitlines() if l.startswith("C ")]
    S = [l.split()[1:] for l in sout.splitlines() if l.startswith("S ")]
    rec = [(float(s[1]) - c[0]) * 1e3 for c, s in zip(C, S)]
    q = lambda xs, f: sorted(xs)[min(len(xs) - 1, int(f * len(xs)))]
    return {"n": len(rec), "group": S[0][2] if S else None, "t_first_record_ms": {"median": statistics.median(rec), "p10": q(rec, .1), "p90": q(rec, .9)},
            "flights_first_conn": flights(log), "client_err": cli.stderr[-200:]}

def main():
    subprocess.run(["bash", os.path.join(HERE, "netns_up.sh")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    outp = os.path.join(ROOT, "results", "testbed_x4.json")
    res = json.load(open(outp)) if os.path.exists(outp) else {}
    for pr in PROFILES:
        for cfg, ch in CASES:
            for v in (0, 1):
                key = f"{pr['name']}|{cfg}|ch{ch}|{'retry' if v else 'noretry'}"
                if key in res: continue
                res[key] = {"profile": pr, "cfg": cfg, "chain": ch, "retry": bool(v), **run(pr, cfg, ch, v, N)}
                print(key, res[key]["t_first_record_ms"], flush=True)
                json.dump(res, open(outp, "w"), indent=1)

if __name__ == "__main__":
    main()
