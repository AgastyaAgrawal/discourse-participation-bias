import json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
S = json.load(open("data/final_sample.json")); order = json.load(open("data/blind_order.json"))
lab = [int(x) for x in open("data/final_labels.txt").read().replace("\n", "")]
df = pd.DataFrame(S); df["D"] = 0
for k, i in enumerate(order): df.loc[i, "D"] = lab[k]
df.to_csv("results/final_users.csv", index=False)
def stats(d):
    c, D = d.c.values.astype(float), d.D.values; w = 1 / c; w = w / w.sum()   # population weights (inclusion ~ c)
    Ec, Ec2 = (w * c).sum(), (w * c * c).sum()
    fit = LogisticRegression(C=1e6).fit(np.log(c)[:, None], D)                # unweighted: selection is on c only
    q = fit.predict_proba(np.log(c)[:, None])[:, 1]
    return dict(d=(w * D).sum(), beta=fit.coef_[0, 0], B_head=(w * D * c).sum() / (w * D).sum() / Ec,
                B=(w * c * c * q).sum() / ((w * c * q).sum() * Ec), B0=Ec2 / Ec**2, B_emp=(w * c * c * D).sum() / ((w * c * D).sum() * Ec))
est = stats(df); rng = np.random.default_rng(0)
boot = pd.DataFrame([stats(df.sample(len(df), replace=True, random_state=rng.integers(1e9))) for _ in range(1000)])
est["B_over_B0"] = est["B"] / est["B0"]; boot["B_over_B0"] = boot["B"] / boot["B0"]
res = pd.DataFrame({"estimate": est, "ci_lo": boot.quantile(.025), "ci_hi": boot.quantile(.975)})
res.to_csv("results/final_estimates.csv"); print(res.round(3))
print(f"\nn={len(df)} users, raw discourse rate {df.D.mean():.2f}, top-level share {df.top_level.mean():.2f}; c median {df.c.median():.0f}, max {df.c.max()}")
print(df.groupby(pd.qcut(df.c, 4)).D.agg(["mean", "count"]))
# figures
bins = pd.qcut(df.c, 4); g = df.groupby(bins, observed=True)
m, n = g.D.mean(), g.D.count(); se = np.sqrt(m * (1 - m) / n); x = g.c.median()
fit = LogisticRegression(C=1e6).fit(np.log(df.c.values)[:, None], df.D); xs = np.logspace(0, np.log10(df.c.max()), 100)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].errorbar(x, m, yerr=1.96 * se, fmt="o", label="binned rate (95% CI)"); ax[0].plot(xs, fit.predict_proba(np.log(xs)[:, None])[:, 1], label=f"logistic fit, β={est['beta']:.2f}")
ax[0].axhline(est["d"], ls="--", c="gray", label=f"population d={est['d']:.2f}"); ax[0].set_xscale("log"); ax[0].set_xlabel("comments in last 30 days (c)"); ax[0].set_ylabel("P(discourse)"); ax[0].legend(); ax[0].set_title("Discourse propensity vs activity")
k = ["B0", "B", "B_head"]; ax[1].bar(["1+CV² (volume only)", "B (voice)", "B_head"], res.loc[k, "estimate"], yerr=[res.loc[k, "estimate"] - res.loc[k, "ci_lo"], res.loc[k, "ci_hi"] - res.loc[k, "estimate"]], capsize=5)
ax[1].axhline(1, c="k", ls=":", label="no bias"); ax[1].set_yscale("log"); ax[1].set_ylabel("activity ratio vs avg active user"); ax[1].legend(); ax[1].set_title("Bias factors (bootstrap 95% CI)")
plt.savefig("figs/final_bias.png", dpi=150, bbox_inches="tight")
