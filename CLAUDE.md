# Shared research rules (read by every Claude session in this project)

This project is a 2-hour research work task. Two Claude sessions work here, in
separate folders, plus a GPT reviewer (see AGENTS.md):

- `primary/` — pair-programming with the human. See primary/CLAUDE.md.
- `auto/`    — autonomous researcher on its own direction. See auto/CLAUDE.md.

The two sessions are independent. Never read from, write to, or copy from the
other session's folder unless the human explicitly tells you to.
Task materials and the human's plan are in `PLAN.md` at the project root.

These rules follow lessons from Anthropic's automated-alignment-researcher work:
agents get the most done when they (a) protect the evaluation, (b) test ideas
cheaply before committing, (c) diagnose from logs rather than only final scores,
and (d) report honestly, including failures.

---

## 1. Research loop (follow for every idea)

1. **Understand.** Before the first experiment, read the task materials and look
   at real data: print 10–20 raw examples, label/class balance, lengths, any
   obvious patterns. Note anything that could be a shortcut (see §4).
2. **Pre-register.** Before running an experiment, append an entry to your
   `results/LOG.md` with: hypothesis, what the code will do, metric, baseline,
   expected result, and what result would change your mind. Never edit this
   entry after seeing results — add a new entry instead.
3. **De-risk cheaply.** Run on a tiny subset / few steps first to check the
   pipeline works and the idea is not dead on arrival.
4. **Full run.** Run with ≥3 seeds. No single run longer than ~10 minutes unless
   the human approves.
5. **Diagnose, don't just score.** Look at loss curves, prediction distributions,
   per-class / per-difficulty results, and actual outputs. A score alone doesn't
   tell you why something worked or failed.
6. **Ablate.** If a method has several parts, remove each part to check it
   actually contributes. Drop parts that don't.
7. **Check generalization.** If any other split, subset, or dataset is
   available, check whether the gain holds there too. A gain that only appears
   on the data you tuned on is weak evidence.
8. **Record.** Log the result (format in §6), including failures and dead ends.

## 2. Evaluation hygiene

- Write the evaluation (scoring) code once, verify it on a few hand-checked
  examples, then freeze it. If it ever must change, say so in LOG.md and re-run
  the baseline with the new version.
- Always run the baseline first, with exactly the same evaluation code.
- Split data into train / dev / test. Iterate only on dev. Test is used once, at
  the end, and only when the human says so.
- Never touch anything outside this project folder. Held-out data is kept
  elsewhere on purpose.
- Never use test labels, the evaluation's answer key, or a stronger model to
  create training data or to choose between methods, unless the human
  explicitly allows it.

## 3. Statistics and claims

- **Noise floor.** Use the baseline's spread across seeds as your noise
  estimate. An improvement smaller than about 2× the baseline std is not a
  result; report it as "no clear effect".
- Report mean ± std and the number of seeds for every number.
- **Never seed-shop**: no re-running unchanged code hoping for a better number,
  and never report only the best seed.
- **Best-of-N bias.** If you tried N variants, the best one is biased upward.
  Always state N alongside the best result.
- **Several metrics.** Track at least one secondary metric (e.g. a different
  split, a capability or calibration measure). Say explicitly whether anything
  got worse. A method that improves the main metric but clearly regresses
  another is not a clean win — report the trade-off.
- If there are several datasets/benchmarks, report each one; don't hide a
  regression inside an average.

## 4. Known ways automated researchers fool themselves (do not do these)

- Seed cherry-picking or re-running for luck.
- Using evaluation feedback to recover labels (e.g. flipping uncertain
  predictions and keeping whichever raises the score).
- Exploiting data shortcuts — e.g. "the most common answer is usually right",
  or clustering by which model generated an example — instead of solving the task.
- Bypassing the intended setup (e.g. running code or looking up answers to get
  labels the method isn't supposed to have).
- Overfitting to one metric while others regress.
- Writing a claim that the code doesn't support.

If you notice one of these happening — or discover a shortcut in the data —
stop and report it. It is a finding, not a solution.

## 5. Honesty and legibility

- Every number you report must come from a file in your `results/` folder.
  Never estimate or invent numbers.
- When reporting a result, show a few raw examples (actual outputs / data rows)
  alongside the aggregate.
- Before claiming a method works, describe in 2–3 sentences what the code
  actually does, so a reader can check that the claim matches the code.
- Prefer simple, explainable methods. If a method works but you can't explain
  why, say so.

## 6. Log format (`results/LOG.md`, append-only)

    ### HH:MM <short title>
    Plan: hypothesis … | code does … | expected …   (written BEFORE running)
    Command: …
    Result: dev <metric> mean ± std (n seeds) vs baseline …; secondary metrics …
    Files: results/…, figs/…
    Takeaway / next: …

## 7. Mechanics

- Scripts in `src/`, outputs (CSV/JSON) in `results/`, figures in `figs/` —
  all inside your own folder. One experiment per script.
- Fix random seeds. Save raw predictions, not only summary numbers.
- Never call plt.show(); always
  plt.savefig("figs/<name>.png", dpi=150, bbox_inches="tight").
  Label axes, include error bars, and include the baseline in comparison plots.
- Print the exact command used to run each script.
- The Python environment is the project's .venv (already activated).
