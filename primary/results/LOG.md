# primary log

### 00:00 HN front page: are discoursers "the kind who post a lot"?
Plan: Reddit returns 403 to unauthenticated clients, so use Hacker News official APIs (Firebase + Algolia) instead.
Sample = top 30 stories by points created in the last 3 days (front-page proxy). Active = commented in these threads.
Discourse = wrote >=1 reply to ANOTHER user's comment that disagrees with it (hand-labelled by Claude with the rubric in src/rubric.md, before profiles are fetched).
Random sample of 120 active users; up to 3 reply-pairs each are labelled. Profile per user: HN karma, account age, lifetime items/day, site-wide comments in last 3 days (Algolia).
Hypothesis: discoursers post far more than non-discoursing posters (site-wide 3-day comment count ratio > 2x) and hold a larger share of comment volume than of users.
Metric: median & mean site-wide 3-day comments, discoursers vs non-discoursers; bootstrap 95% CI over users (1000 resamples, seed 0). Secondary: karma, items/day, in-thread comment share.
Would change my mind: ratio CI includes 1.
Caveat known in advance: users with more comments have more chances to be labelled discoursers (exposure confound) -> also report the comparison restricted to users with exactly 1 labelled reply.

### 00:40 Discourse vs activity on HN (final design; previous entry abandoned before profiles/analysis)
Plan: Sample users via random site-wide comments in last 30 days (random timestamp -> latest comment before it), so inclusion prob ~ c_i (user's 30-day comment count) and population estimates use weights 1/c_i.
D_i = binary label of that sampled comment (a uniform draw among the user's comments) using the aggressive rubric in src/rubric.md; top-level comments judged vs story title. Labelling is blind: pairs shown shuffled, without author or c.
Metrics: d (weighted), beta from logistic D ~ log c (unweighted: selection is on c only, so conditional fit is unbiased), B_head, B, B0=1+CV^2, B/B0; bootstrap 95% CI over users (1000, seed 0).
Hypothesis (Pew/Robertson): beta > 0, B > B0. Would change my mind: beta CI includes 0 -> bias is volume-only (1+CV^2).
n ~ 120 users (time budget ~10 min). Known caveats: time-gap sampling over-weights quiet-hour comments; single labeller (Claude); HN-only.
Command: python src/fetch_final.py; python src/print_blind.py; (Claude hand-labels data/final_labels.txt blind); python src/analyze_final.py
Result (n=140 users, 1 labelled comment each, bootstrap 95% CI): d=0.54 [0.37,0.71] (pop-weighted; raw 0.64); beta=0.04 [-0.18,0.27];
B_head=1.18 [0.92,1.62]; B=10.9 [6.6,17.1]; B0=1+CV^2=10.6 [6.7,15.7]; B/B0=1.03 [0.87,1.18]. Rate by c-quartile: 0.59/0.68/0.66/0.62.
Files: results/final_users.csv, results/final_estimates.csv, figs/final_bias.png
Takeaway: no evidence discoursers are heavier posters (beta CI spans 0). The ~11x voice bias is almost entirely the volume term 1+CV^2. Caveats: single labeller (Claude), aggressive rubric -> d high; HN only; time-gap sampling.

### Final decisions (human)
Independent label checks: Codex 38/40 (kappa 0.89, items 0-39), Claude subagent 36/40 (kappa 0.80, items 100-139) -> keep primary (Claude) labels unchanged.
Single reported bias metric: B_head = E[c | D=1] / E[c] (pop-weighted) = 1.18, 95% CI [0.92, 1.62], n=140 -> no clear effect. Other quantities in results/final_estimates.csv are kept for transparency but not headline.
Reviews: results/review_codex.md, results/review_claude.md. No further experiments (time limit).
