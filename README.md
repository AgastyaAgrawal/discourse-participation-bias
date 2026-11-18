# Participation Bias in Online Discourse

> In public discourse (like on X), people who participate tend to be the kind of people who participate in discourse. **Can we model and measure that bias?**

A 2-hour research work test, run with three AI collaborators: a **primary** Claude session pair-programming with the human, an **autonomous** Claude session exploring its own direction, and **GPT (Codex)** acting as an independent reviewer. Data: public Hacker News comments via the official Algolia / Firebase APIs.

📄 **Writeup:** [`writeup.md`](writeup.md) · 📊 **Primary results:** [`primary/RESULTS.md`](primary/RESULTS.md) · 🤖 **Autonomous session report:** [`auto/REPORT.md`](auto/REPORT.md)

---

## Primary experiment (human + Claude)

### Definitions
| Term | Definition |
|---|---|
| **Active user** | Posted ≥ 1 HN comment in the last 30 days. Activity `c` = their 30-day comment count. |
| **Discourse** | A comment that takes a side in a disagreement: contradicts / challenges / corrects / sarcastically rebuts its parent (or the story), sides with a party in an ongoing disagreement, or asserts a political or contested-value position. |
| **Discourser** (`D = 1`) | One comment drawn at random from the user is discourse. One comment per user, so heavy posters don't get more chances to be counted. |

### Method
1. **Sampling:** 140 users, each reached through a random site-wide comment from the last 30 days. Inclusion is ∝ `c`, so population estimates use weights `1/c`.
2. **Labelling:** each sampled comment was labelled 0/1 by Claude against a fixed rubric ([`primary/src/rubric.md`](primary/src/rubric.md)), **blind** to author and activity, and **before** any profile analysis.
3. **Bias:**

$$B \;=\; \frac{E[c \mid D=1]}{E[c]}$$

How much more active discoursers are than the average active user. `B = 1` means no bias.

### Result

| Quantity | Estimate | 95% CI (bootstrap, n = 140) |
|---|---|---|
| **Bias B** | **1.18** | 0.92 – 1.62 |
| Discourse rate d | 0.54 | 0.37 – 0.71 |

**No clear evidence that discoursers are more active than other active users.** The interval includes 1.

Context, not the headline: a randomly *seen* discourse comment's author is about 9–11× more active than the average user. That comes almost entirely from heavy posters writing more of everything, not from discoursers being a distinct type. See [`primary/results/final_estimates.csv`](primary/results/final_estimates.csv).

![Bias figure](primary/figs/final_bias.png)

### Verification
| Check | Outcome |
|---|---|
| Codex (GPT), blind relabel of items 0–39 | 38/40 agree, κ = 0.89 |
| Fresh Claude subagent, blind relabel of items 100–139 | 36/40 agree, κ = 0.80 |
| Using the reviewers' labels instead | Conclusion unchanged |
| Code and statistics review | Formulas correct, caveats below. [`review_codex.md`](primary/results/review_codex.md), [`review_claude.md`](primary/results/review_claude.md) |

### Caveats
- One site (Hacker News) and one 30-day window.
- Effective sample is about 30 users after `1/c` weighting, so intervals are wide.
- Picking a random timestamp slightly over-samples comments from quiet hours.
- Labels are model-made. Agreement shows consistency, not human-validated correctness.
- The rubric is broad. A stricter "political only" definition was not tested.

### Reproduce
```bash
cd primary
python src/fetch_final.py      # sample 140 users via random comments (HN Algolia API)
python src/print_blind.py      # shuffled, author-blind pairs for labelling
# labels: data/final_labels.txt (hand-labelled with src/rubric.md)
python src/analyze_final.py    # estimates -> results/, figure -> figs/
```
A live re-run draws a different 30-day window. The exact sample used is in `primary/data/final_sample.json`.

---

## Autonomous Claude session (`auto/`)

An independent direction, run without human steering and reviewed by GPT. On 273,574 HN comments (Sep 2025):
- **Comment concentration:** the top 10% of commenters wrote about 50% of comments.
- **Propensity is a persistent trait:** week-to-week Spearman correlation of 0.57.
- **Counting users instead of comments** removes most of the error when predicting what unseen participants look like.

These numbers are the autonomous session's own and were not re-run by the primary session. Full details and caveats are in [`auto/REPORT.md`](auto/REPORT.md).

---

## Repository layout
```
writeup.md          human's writeup
PLAN.md             task statement
CLAUDE.md           shared research rules (pre-registration, eval hygiene, honesty)
AGENTS.md           GPT reviewer instructions
primary/            human + Claude experiment
  RESULTS.md        one-page summary
  src/              fetch, blind-print, analysis scripts, rubric
  data/             sample, blind order, labels
  results/          LOG.md (pre-registered, append-only), estimates, reviews
  figs/             figures
auto/               autonomous Claude session (report, code, data, reviews)
```
