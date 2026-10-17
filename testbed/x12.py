"""
x12.py -- X1 (bytes per flight and direction) and X2 (time to first authenticated record) on the
emulated links. Rates and RTTs come from the ledger (models/common.p). Results -> results/testbed_x12.json.

Profiles (client = device, so client->server is the uplink):
  5G-hosp   UL 91 / DL 790 Mb/s [chen2024], RTT 10 ms [berlet2022]
  5G-tele   UL 101 / DL 177 Mb/s [ye2026], RTT 18 ms [moustris2023]
  LTE-M     UL 380 / DL 300 kb/s [gsma-nbiot], RTT 10 ms (assumed, to isolate serialization; no ledger RTT)
  NB-IoT    UL 66 / DL 26 kb/s [gsma-nbiot], RTT 10 ms (assumed, as above)
"""
import json, os, statistics, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "models"))
from common import p
from run import run_case, CLEANUP

PROFILES = [
    {"name": "5G-hosp", "ul": p("ul_5gsa_chen2024_avg_bps"), "dl": p("dl_5gsa_chen2024_avg_bps"), "owd_ms": p("rtt_5g_berlet2022_ms") / 2, "n": 200,
     "src": "rates chen2024, RTT berlet2022"},
    {"name": "5G-tele", "ul": p("ul_5g_ye2026_bps"), "dl": p("dl_5g_ye2026_bps"), "owd_ms": p("rtt_5g_moustris2023_ms") / 2, "n": 200,
     "src": "rates ye2026, RTT moustris2023"},
    {"name": "LTE-M", "ul": p("ltem_hd_ul_bps"), "dl": p("ltem_hd_dl_bps"), "owd_ms": 5.0, "n": 30,
     "src": "rates gsma-nbiot; RTT 10 ms assumed (not a measured LTE-M RTT)"},
    {"name": "NB-IoT", "ul": p("nbiot_peak_ul_bps"), "dl": p("nbiot_peak_dl_bps"), "owd_ms": 5.0, "n": 15,
     "src": "peak rates gsma-nbiot; RTT 10 ms assumed (not a measured NB-IoT RTT)"},
]
CASES = [("C0", 2), ("C1", 2), ("C2", 2), ("C2u", 2), ("C2", 3), ("C3", 2), ("C3u", 2), ("C3", 3), ("C3m", 2), ("C3m", 3)]
APP_RECORD = 1000 + 22   # 1,000-B payload + 5-B header + 16-B tag + 1-B content type

def q(xs, f):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(f * len(xs)))]

def main():
    subprocess.run(["bash", os.path.join(HERE, "netns_up.sh")], check=True, stdout=subprocess.DEVNULL)
    which = sys.argv[1:] or [pr["name"] for pr in PROFILES]
    outp = os.path.join(HERE, "..", "results", "testbed_x12.json")
    allres = json.load(open(outp)) if os.path.exists(outp) else {}
    for pr in PROFILES:
        if pr["name"] not in which: continue
        for cfg, ch in CASES:
            key = f"{pr['name']}|{cfg}|ch{ch}"
            if key in allres and not os.environ.get("X12_REDO"): continue   # keep cells already measured
            t0 = time.time()
            r = run_case(pr, cfg, chain=ch, n=pr["n"], gap_ms=100)
            rec = [x["t_first_record_server_ms"] for x in r["runs"]]
            hs = [x["t_hs_client_ms"] for x in r["runs"]]
            tcp = [x["t_tcp_ms"] for x in r["runs"]]
            fl0 = r["flights"][0]
            # handshake bytes: all payload except the client's 1,022-B application record and the server's 24-B close_notify
            per_conn = []
            for fl in r["flights"]:
                cs = sum(f[1] for f in fl if f[0] == "C>S"); sc = sum(f[1] for f in fl if f[0] == "S>C")
                per_conn.append((cs, sc, len(fl)))
            allres[key] = {"profile": pr, "cfg": cfg, "chain": ch, "group": r["runs"][0]["group"], "n": len(rec),
                "flights_first_conn": [[f[0], f[1], f[2]] for f in fl0],
                "payload_C2S_B": {"min": min(c[0] for c in per_conn), "max": max(c[0] for c in per_conn)},
                "payload_S2C_B": {"min": min(c[1] for c in per_conn), "max": max(c[1] for c in per_conn)},
                "n_flights": sorted(set(c[2] for c in per_conn)),
                "app_record_B": APP_RECORD,
                "t_tcp_ms": {"median": statistics.median(tcp)},
                "t_hs_client_ms": {"median": statistics.median(hs), "p90": q(hs, .9)},
                "t_first_record_ms": {"median": statistics.median(rec), "p10": q(rec, .1), "p90": q(rec, .9), "min": min(rec), "max": max(rec)},
                "wall_s": round(time.time() - t0, 1)}
            subprocess.run(CLEANUP)
            print(key, allres[key]["t_first_record_ms"], allres[key]["flights_first_conn"], flush=True)
            json.dump(allres, open(outp, "w"), indent=1)

if __name__ == "__main__":
    main()
