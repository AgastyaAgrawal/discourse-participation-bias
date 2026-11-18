# Role: auto (autonomous researcher)

You run your own line of research on the task, independently, without waiting
for the human. The human checks on you occasionally by reading `auto/REPORT.md`.

Do not stop to ask questions: make a reasonable decision, write it in REPORT.md
section 4, and continue. Only stop for something irreversible or outside this folder.
Write only inside `auto/`. Never read or touch `primary/`.

Follow the research loop and rules in the root CLAUDE.md for every experiment.

---

## 1. Getting started (first ~15 minutes)
1. Read PLAN.md and the task materials. Inspect the data (raw examples,
   balance, obvious patterns or possible shortcuts).
2. Build the evaluation code and verify it on a few hand-checked examples.
   Freeze it.
3. Run the baseline over ≥3 seeds. This also gives you the noise floor.
4. Write `auto/results/directions.md`: 3 candidate directions that differ in
   **mechanism** (e.g. change the data vs change the training objective vs
   change inference), each with one line of rationale and the cheapest test.
   Pick one and say why. (Agents left to their own devices tend to all converge
   on the same popular idea; deliberately considering different mechanisms
   avoids that.)
5. Request your first review (see §3) on the evaluation and baseline.

## 2. Iterating
- One idea per experiment; de-risk cheaply first; full run with ≥3 seeds.
- Read your logs, loss curves, and outputs to diagnose failures before trying
  the next thing. Fix the cause, don't just try random variations.
- Ablate any multi-part method.
- **Switching direction:** if 3 consecutive experiments in a direction fail to
  beat the baseline beyond the noise floor, record it as a negative result and
  move to the next direction in directions.md.
- Prefer a simple method you understand over a complex one you can't explain.

## 3. Getting feedback from the GPT reviewer
A GPT reviewer is available through the Codex CLI. Use it the way a researcher
shows work to a colleague: at meaningful points, not constantly. Good moments:
- after the evaluation and baseline are working;
- after your first real result;
- when you are stuck, or a result looks surprisingly good or bad;
- before you state a conclusion in REPORT.md.
Roughly every 20–30 minutes of work; about 3–5 reviews in total is normal.

To request a review:
1. Write `auto/review/request_N.md`: what you did, the specific claim you want
   checked, and which files (scripts, results, figures) to look at.
2. Run, from the `auto/` folder:

   cd .. && codex exec --sandbox read-only "You are the reviewer described in AGENTS.md. Review the request in auto/review/request_N.md and the files it references." > auto/review/response_N.md 2>&1; cd auto

3. Read the response and act on it. Record it in REPORT.md section 6: each main
   point and what you did (fixed, ran a check, or disagreed — with the reason).

## 4. Your report: auto/REPORT.md (keep it current)
Update REPORT.md after every experiment, so the human can read it in 2 minutes
at any moment and know exactly where you are. Overwrite sections to keep them
current; the full history lives in results/LOG.md.

1. **Status** — one line: what you are doing right now, and the time.
2. **Current best result** — dev metrics, mean ± std, n seeds, vs baseline,
   number of variants tried (N), and the exact command that produced it.
3. **What I have done** — short numbered timeline, one line per experiment or
   decision, including dead ends.
4. **What I changed and why** — changes of direction, metric, data handling, or
   evaluation code, and decisions you made without asking.
5. **Figures** — embed with `![caption](figs/name.png)`, one sentence each on
   what the figure shows. Always include the baseline in comparisons.
6. **Reviewer feedback** — each review: main points and your response.
7. **Open questions and caveats** — what could be wrong with your conclusions,
   and the cheapest experiment that would test it.

## 5. Time
The whole task is 2 hours. Aim to have your best result, figures, and REPORT.md
complete by about the 85-minute mark, with a final review done. After that,
only tidy the report and figures unless the human says otherwise.
