---
title: 'Instructor Notes'
---

## Overall timing

Two four-hour sessions, each split into two two-hour blocks with a ~10-minute
break roughly every 50-60 minutes within a block, plus a longer break between
the two blocks of each session.

| Session | Block | Episode file | Topic | Time |
|---|---|---|---|---|
| 1 | 1 | `01-writing-functions.md` | Writing Effective Functions | 2h |
| 1 | 2 | `02-modules.md` | Organizing Functions into Modules | 2h |
| 2 | 3 | `03-repo-environments.md` | Repository + Environments | 2h |
| 2 | 4 | `04-documentation-reuse.md` | Documentation and Reuse | 2h |

## Design notes

- The whole workshop is built around two real datasets: CTD and DOSTA data
  from the GI01SUMO (**G**lobal **I**rminger Sea Array **Su**rface **Mo**oring)
  NSIF (**N**ear **S**urface **I**nstrument **F**rame), which is located at 12 m
  depth at 59.935683°N, -39.471917°W. Each block builds
  directly on the previous one. The functions from Block 1
  become the module in Block 2, the module becomes the repo in Block 3, and
  the repo gets documented and reused in Block 4. 
- `messy_analysis.ipynb`'s is intended as an example notebook of which many learners
  may be familiar with. Its intended to contain (almost) all the logic that
  learners may need and is the source from which learners will be pulling
  much of the code that goes into the functions and modules. Overall, though, this is a notebook-first workshop throughout: no standalone
  `.py` scripts are run from a terminal, with everything happenning in
  `messy_analysis.ipynb`, with functions moved out into `.py` modules that
  the notebook then imports.
- Docstrings are introduced early (Block 1, at the function level) and
  revisited at the project level in Block 4. This is intentional. Flag the
  callback for learners so it doesn't feel repetitive.
- Have learners work from the same starter files (see `learners/setup.md`)
  so that live-coding and challenges stay in sync across the room.
- Block 3's environment challenge assumes learners already have Python and
  git installed per the setup page. Confirm this and remind learners that
  having python, Jupiter, and the associated packages installed is a prereq.


## Common sticking points

- Clearly distinguish "module" vs "package" and the callout in Episode 2
  explicitly which explicitly addresses this difference.
- `PATH` and environment activation issues during Block 3 may be an issue.
- Episode 2's `random.py` shadowing demo is a real, reproducible failure
  (verified) — it's worth actually running live rather than describing it,
  since the traceback (NumPy failing three layers deep, inside
  `secrets.py`) is far more convincing than a description would be. Have
  learners run it in a scratch folder, not their project folder.
- Episode 2's merge-module challenge (Challenge 3) reproduces two real bugs
  from the source notebook: a `MergeError` from an un-flattened DOSTA
  table, and a `ctd_ds`/`ds` typo. This is a good moment to make explicit:
  writing `flag_and_flatten` as one function called identically for both
  instruments makes the missing flatten step impossible to skip, whereas
  it was easy to miss scrolling through a long notebook.
- The `%load_ext autoreload` / `%autoreload 2` pattern in Episode 2 is
  worth demonstrating live (edit a function in `stats.py`, re-run a
  notebook cell, show the change take effect without restarting the
  kernel). It's a detail that makes the notebook + module workflow feel natural.

