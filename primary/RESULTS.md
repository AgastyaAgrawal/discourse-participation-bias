# Participation bias in online discourse (Hacker News)

**Question:** are people who take part in discourse "the kind of people who participate" — i.e. more active than the average active user?

- **Sample:** 140 HN users, each reached via a random site-wide comment from the last 30 days (Algolia API); inclusion ∝ activity c (30-day comment count), corrected with weights 1/c.
- **Discourse (binary):** the sampled comment takes a side in a disagreement (contradicts/challenges/rebuts the parent or story, sides with a party in a disagreement, or asserts a political/contested-value position). Labelled blind to author and activity. Rubric: `src/rubric.md`.
- **Bias:** B = E[c | D=1] / E[c] (activity of discoursers relative to all active users).
- **Result:** B = 1.18, 95% bootstrap CI [0.92, 1.62] → no clear evidence that discoursers are more active than other active users. Discourse rate d = 0.54 [0.37, 0.71].
- **Checks:** independent blind relabelling by Codex (38/40, κ = 0.89) and a fresh Claude subagent (36/40, κ = 0.80); swapping in their labels does not change the conclusion. Reviews: `results/review_codex.md`, `results/review_claude.md`.
- **Caveats:** one site; effective sample ≈ 30 after weighting; timestamp sampling over-weights quiet-hour comments; labels are model-made (no human check); broad rubric.

Files: `results/LOG.md` (pre-registration + results), `results/final_estimates.csv`, `results/final_users.csv`, `figs/final_bias.png`, code in `src/` (`fetch_final.py` → `print_blind.py` → labels `data/final_labels.txt` → `analyze_final.py`). `auto/` contains the separate autonomous Claude session's work.
