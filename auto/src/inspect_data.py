import numpy as np
from world import draw_params, simulate, truth

rng = np.random.default_rng(0)
for wi in range(3):
    p = draw_params(rng)
    pop, obs = simulate(p, rng)
    t = truth(pop)
    print(f"\nworld {wi}: " + " ".join(f"{k}={v:.2f}" for k, v in p.items()))
    print(f"  seen {len(obs['x'])}/{len(pop['x'])} users ({len(obs['x'])/len(pop['x']):.1%}), posts {obs['kA'].sum()}")
    kA = np.sort(obs["kA"])[::-1]
    print(f"  top 1% of seen users write {kA[:max(1,len(kA)//100)].sum()/kA.sum():.1%} of posts; median kA {np.median(kA):.0f}, max {kA.max()}")
    post_sup = np.sum(obs["kA"] * (obs["x"] > 0)) / obs["kA"].sum()
    print(f"  support: true {t['support']:.3f} | users-seen {np.mean(obs['x']>0):.3f} | posts {post_sup:.3f}")
    print(f"  extreme: true {t['extreme']:.3f} | users-seen {np.mean(np.abs(obs['x'])>1.5):.3f}")
    print("  10 raw seen rows (x, kA, kB):", [(round(a, 2), b, c) for a, b, c in zip(obs["x"][:10], obs["kA"][:10], obs["kB"][:10])])
