import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, GRAY = "#2a78d6", "#8a8a85"
df = pd.concat([pd.read_csv("../results/v2.csv"), pd.read_csv("../results/ablate.csv").query("method in ['eb_kA','raw_kB']")])

# Fig 1: support error by method, mean ± std over 3 seeds
order = ["posts", "const", "users", "eb_kA", "raw_kB", "eb_ipw", "eb_ipw_binned", "oracle_ipw"]
kind = {"posts": GRAY, "const": GRAY, "users": GRAY, "oracle_ipw": "white"}
s = df.groupby(["method", "seed"]).err_support.mean().groupby("method").agg(["mean", "std"]).loc[order]
fig, ax = plt.subplots(figsize=(7, 3.6))
for i, (m, r) in enumerate(s.iterrows()):
    ax.barh(i, r["mean"], xerr=r["std"], color=kind.get(m, BLUE), edgecolor=GRAY if m == "oracle_ipw" else "none",
            hatch="//" if m == "oracle_ipw" else None, height=0.6, capsize=3)
    ax.text(r["mean"] + r["std"] + 0.004, i, f"{r['mean']:.3f}", va="center", fontsize=8, color="#333")
ax.axvline(s.loc["users", "mean"], color=GRAY, ls=":", lw=1)
ax.set_yticks(range(len(order)), ["posts (naive)", "const 0.5", "users (baseline)", "abl: rate from kA",
                                  "abl: no shrinkage", "eb_ipw", "eb_ipw + opinion bins", "oracle (true rates)"])
ax.invert_yaxis()
ax.set_xlabel("mean abs error, population support share (lower is better)")
ax.set_title("Recovering population opinion from discourse (v2 worlds, 3 seeds × 30)", fontsize=10)
ax.spines[["top", "right"]].set_visible(False)
plt.savefig("../figs/methods_support_err.png", dpi=150, bbox_inches="tight")

# Fig 2: signed error vs opinion tilt of posting rate (c)
fig, ax = plt.subplots(figsize=(6, 3.6))
for m, col, lab in [("users", GRAY, "users (baseline)"), ("eb_ipw", BLUE, "eb_ipw")]:
    e = df[df.method == m]
    y = e.est_support - e.true_support
    ax.scatter(e.c, y, s=14, color=col, alpha=0.7, label=lab, edgecolor="white", linewidth=0.5)
    k = np.polyfit(e.c, y, 1); xs = np.linspace(-0.7, 0.7, 2); ax.plot(xs, np.polyval(k, xs), color=col, lw=2)
ax.axhline(0, color="#333", lw=0.8)
ax.set_xlabel("c: how much posting rate rises with opinion (log-rate per unit opinion)")
ax.set_ylabel("estimate − true support share")
ax.set_title("Bias follows the opinion tilt of participation; reweighting flattens it", fontsize=10)
ax.legend(frameon=False, fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
plt.savefig("../figs/bias_vs_tilt.png", dpi=150, bbox_inches="tight")
print("python figures.py")
