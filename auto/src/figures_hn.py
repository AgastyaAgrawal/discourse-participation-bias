import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, GRAY = "#2a78d6", "#8a8a85"
r = pd.read_csv("../results/hn_predict_ebT.csv").query("adj == 'drift_adj'")
s = r.groupby(["method", "feat", "fold"]).signed.mean().groupby(["method", "feat"]).agg(["mean", "std"])
order = ["posts", "users", "extrap", "eb_unseen", "eb_T"]
names = {"f_ai": "share on AI stories", "f_len": "log comment length", "f_top": "share top-level", "f_url": "share with link"}
fig, axes = plt.subplots(1, 4, figsize=(13, 3.2), sharey=False)
for ax, f in zip(axes, names):
    g = s.xs(f, level="feat").loc[order]
    ax.barh(range(len(order)), g["mean"], xerr=g["std"], color=[GRAY, GRAY, BLUE, BLUE, BLUE], height=0.6, capsize=3)
    ax.axvline(0, color="#333", lw=0.8)
    ax.set_yticks(range(len(order)), order if f == "f_ai" else [""] * len(order)); ax.invert_yaxis()
    ax.set_title(names[f], fontsize=9); ax.set_xlabel("estimate − truth", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
plt.suptitle("Predicting users absent from week 1 who appear in weeks 3–4 (HN Sep 2025; drift-adjusted; mean ± std over 3 user folds)", fontsize=10)
plt.savefig("../figs/hn_signed_errors.png", dpi=150, bbox_inches="tight")
print("cd src && python figures_hn.py")
