import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hn_data import load, FEATS

BLUE, GRAY = "#2a78d6", "#8a8a85"
d = load()
out = {}

# 1. Concentration per week
for wk in range(4):
    k = d[d.day // 7 == wk].groupby("user").size().sort_values(ascending=False)
    out[f"week{wk + 1}"] = dict(comments=int(k.sum()), users=len(k),
                                top1pct_share=float(k.iloc[:max(1, len(k) // 100)].sum() / k.sum()),
                                top10pct_share=float(k.iloc[:len(k) // 10].sum() / k.sum()),
                                single_comment_users=float((k == 1).mean()))

# 2. Propensity stability W1 vs W2, and capture-recapture
k1 = d[d.win == "W1"].groupby("user").size()
k2 = d[d.win == "W2"].groupby("user").size()
both = k1.index.intersection(k2.index)
kk = pd.concat([k1, k2], axis=1).fillna(0)
out["stability"] = dict(spearman_k1_k2_among_W1=float(kk.loc[k1.index].corr("spearman").iloc[0, 1]),
                        frac_W1_users_back_in_W2=float(len(both) / len(k1)))
out["lincoln_petersen_active_users"] = float(len(k1) * len(k2) / len(both))
out["seen_W1_users"] = len(k1)

# 3. Attribute gradient across activity (users binned by W2 count, measured on W1 comments; independent windows)
u1 = d[d.win == "W1"].groupby("user")[FEATS].mean()
u1["k2"] = k2.reindex(u1.index, fill_value=0)
u1["bin"] = pd.cut(u1.k2, [-1, 0, 1, 3, 10, 30, 1e9], labels=["0", "1", "2-3", "4-10", "11-30", ">30"])
grad = u1.groupby("bin", observed=True)[FEATS].agg(["mean", "sem", "size"])
grad.to_csv("../results/hn_gradient.csv")
json.dump(out, open("../results/hn_describe.json", "w"), indent=1)
print(json.dumps(out, indent=1))
print(grad.round(4).to_string())

# Fig A: Lorenz curve of comments over users, all 4 weeks
k = np.sort(d.groupby("user").size().values)[::-1]
fig, ax = plt.subplots(figsize=(5, 3.6))
ax.plot(np.arange(1, len(k) + 1) / len(k) * 100, np.cumsum(k) / k.sum() * 100, color=BLUE, lw=2, label="HN commenters, Sep 2025")
ax.plot([0, 100], [0, 100], color=GRAY, ls=":", lw=1, label="equal participation")
ax.set_xlabel("% of commenters (most active first)")
ax.set_ylabel("% of all comments")
ax.set_title("Who produces the discourse (4 weeks, %d users)" % len(k), fontsize=10)
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
plt.savefig("../figs/hn_lorenz.png", dpi=150, bbox_inches="tight")

# Fig B: attribute gradient vs activity
fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for ax, f in zip(axes, FEATS):
    g = grad[f]
    ax.errorbar(range(len(g)), g["mean"], yerr=1.96 * g["sem"], color=BLUE, marker="o", ms=4, capsize=3)
    ax.set_xticks(range(len(g)), g.index, fontsize=8); ax.set_title(f, fontsize=9)
    ax.set_xlabel("comments in W2 (activity)", fontsize=8); ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("mean of W1 user value (95% CI)")
plt.suptitle("How W1 content varies with users' propensity to participate", fontsize=10)
plt.savefig("../figs/hn_gradient.png", dpi=150, bbox_inches="tight")
print("cd src && python describe_hn.py")
