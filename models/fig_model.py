"""
fig_model.py -- figure of the session-loss model (models/x3_model.py) for the paper: (a) expected late records per
interruption against the configuration's cold handshake time H, for the two 5G profiles and for interruptions that
need no retry or one retry, with the measured configurations marked; (b) model against measurement per cell (same valid intervals), for the
development runs (Table IV) and the held-out runs (predictions filed before the runs). Reads results/testbed_summary.json.
Output: paper/figs/fig3_model.pdf
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import x3_model as M
OUT = os.path.join(ROOT, "paper", "figs"); os.makedirs(OUT, exist_ok=True)
S = json.load(open(os.path.join(ROOT, "results", "testbed_summary.json")))
XM = S["x3_model"]
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d3"
plt.rcParams.update({"font.size": 7.5, "axes.labelsize": 7.5, "legend.fontsize": 6.2, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
                     "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK,
                     "text.color": INK, "pdf.fonttype": 42, "font.family": "DejaVu Sans"})
def style(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
PROF = {"5G-hosp": (10.0, 5.0, BLUE, "10 ms"), "5G-tele": (18.0, 9.0, ORANGE, "18 ms")}
fig, (a, b) = plt.subplots(1, 2, figsize=(3.45, 1.3), gridspec_kw={"width_ratios": [1.25, 1]})
# (a) boundary: expected late records against H for no retry (solid) and one retry (dashed); the measured H of C0,
# C2 + int. with the default window and with IW 20 marked as vertical lines in the profile's color
Hs = np.arange(20, 101, 0.5)
for prof, (rtt, owd, col, lab) in PROF.items():
    for n, ls in ((0, "-"), (1, "--")):
        a.plot(Hs, [M.late_by_retries(h, rtt, owd, n) for h in Hs], color=col, ls=ls, lw=1.2, label=f"{lab}, $k={n}$")
    cells = XM["boundary"][prof]["cells"]
    ymk = 5.5 if prof == "5G-hosp" else 5.15
    for key, mk in (("C0|ch2", "o"), ("C2w|ch3", "D"), ("C2|ch3", "s")):
        a.axvline(cells[key]["H_ms"], ymax=(ymk - 0.15 + 0.1) / 5.8, color=col, lw=0.6, alpha=0.55, zorder=1)
        a.plot(cells[key]["H_ms"], ymk, marker=mk, ms=3.0, mfc=col, mec=col, ls="none", zorder=6, clip_on=False)
a.set_xlabel("Connect to first record, $H$ (ms)"); a.set_ylabel("Late records")
a.set_xlim(20, 100); a.set_ylim(-0.1, 5.7); a.set_yticks([0, 1, 2, 3, 4, 5])
style(a)
a.text(0.97, 0.04, "(a)", transform=a.transAxes, ha="right", va="bottom", fontsize=7.5)
# (b) model against measurement per cell
lim = [0, 4.6]
b.plot(lim, lim, color=MUTED, lw=0.7, ls=(0, (3, 2)))
from matplotlib.lines import Line2D
for k, v in XM["development"]["cells"].items():
    prof = k.split("|")[0]; col = PROF[prof][2]
    b.plot(v["late_model"], v["late_obs"], marker="o", ms=3.4, mfc="white", mec=col, mew=0.9, ls="none", zorder=5)
if XM.get("heldout"):
    for k, v in XM["heldout"]["cells"].items():
        prof = k.split("|")[0]; col = PROF[prof][2]
        mk = "D" if "C2w" in k else ("s" if "|C2|ch3" in k else "o")
        b.plot(v["late_model"], v["late_obs"], marker=mk, ms=3.6, mfc=col, mec=col, mew=0.9, ls="none", zorder=6)
b.set_xlim(lim); b.set_ylim(lim); b.set_xticks([0, 1, 2, 3, 4]); b.set_yticks([0, 1, 2, 3, 4])
b.set_xlabel("Model"); b.set_ylabel("Measured")
style(b)
b.text(0.97, 0.04, "(b)", transform=b.transAxes, ha="right", va="bottom", fontsize=7.5)
h2 = [Line2D([], [], color=MUTED, marker="o", ls="none", ms=3.4, mfc="white", mew=0.9, label="development"),
      Line2D([], [], color=MUTED, marker="o", ls="none", ms=3.4, mfc=MUTED, mew=0.9, label="C0"),
      Line2D([], [], color=MUTED, marker="s", ls="none", ms=3.4, mfc=MUTED, mew=0.9, label="C2 + int."),
      Line2D([], [], color=MUTED, marker="D", ls="none", ms=3.4, mfc=MUTED, mew=0.9, label="C2 + int., IW 20")]
_lg = a.legend(loc="upper left", bbox_to_anchor=(0.0, 0.875), ncol=2, frameon=True, facecolor="white", edgecolor="none", framealpha=1.0, handlelength=1.3, handletextpad=0.3, columnspacing=0.6, labelspacing=0.1, borderaxespad=0.15, borderpad=0.15, fontsize=5.0)
_lg.set_zorder(10)   # the box hides the H marker lines behind it
b.legend(handles=h2, loc="upper left", bbox_to_anchor=(0.02, 0.98), frameon=False, handlelength=1.0, handletextpad=0.3, labelspacing=0.15, borderaxespad=0.2, fontsize=5.6)
fig.tight_layout(pad=0.3, w_pad=0.8, rect=(0, 0, 1, 1))
fig.savefig(os.path.join(OUT, "fig3_model.pdf"), metadata={"CreationDate": None}); plt.close(fig)   # no date: reruns are byte-identical
print("fig3_model.pdf written; development cells:", len(XM["development"]["cells"]), "held-out cells:", len(XM.get("heldout", {}).get("cells", {})) if XM.get("heldout") else 0)
