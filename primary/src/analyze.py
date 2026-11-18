import json, numpy as np, pandas as pd
P = json.load(open("data/pairs.json")); prof = json.load(open("data/profiles.json")); C = json.load(open("data/hn_threads.json"))["comments"]
lab = [int(x) for x in open("data/labels.txt").read().replace("\n", "")]
pairs = pd.DataFrame(P["pairs"]).assign(dis=lab)
df = pd.DataFrame.from_dict(prof, orient="index")
df["items_per_day"] = df["items"] / df["age_days"]
df["in_thread"] = pd.Series(pd.Series([c["author"] for c in C]).value_counts())
df["dis_any"] = pairs.groupby("user").dis.max().reindex(df.index).fillna(0).astype(int)   # top-level-only users = 0
df["dis_first"] = pairs.groupby("user").dis.first()                                        # one label per user (exposure control); NaN for top-level-only
df.to_csv("results/hn_users.csv")
rng = np.random.default_rng(0)
def cmp(col, grp):
    d = df.dropna(subset=[grp]); a, b = d[d[grp] == 1][col].values, d[d[grp] == 0][col].values
    boot = [rng.choice(a, len(a)).mean() / rng.choice(b, len(b)).mean() for _ in range(1000)]
    return dict(group=grp, metric=col, n_dis=len(a), n_non=len(b), mean_dis=a.mean(), mean_non=b.mean(), med_dis=np.median(a), med_non=np.median(b),
                ratio_means=a.mean() / b.mean(), ci_lo=np.percentile(boot, 2.5), ci_hi=np.percentile(boot, 97.5))
res = pd.DataFrame([cmp(m, g) for g in ("dis_any", "dis_first") for m in ("comments_3d", "in_thread", "karma", "items_per_day")])
res.to_csv("results/hn_compare.csv", index=False)
pd.set_option("display.width", 200); print(res.round(2).to_string(index=False))
print(f"\nusers {len(df)} | discoursers (any) {df.dis_any.sum()} = {df.dis_any.mean():.2f} | reply pairs {len(pairs)}, disagree rate {pairs.dis.mean():.2f}")
print(f"share of users = {df.dis_any.mean():.2f}; share of in-thread comments by discoursers = {df[df.dis_any==1].in_thread.sum()/df.in_thread.sum():.2f}; share of site-wide 3d comments = {df[df.dis_any==1].comments_3d.sum()/df.comments_3d.sum():.2f}")
