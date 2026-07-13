---
title: 'Instructor Notes'
---

## Overall timing

Two four-hour sessions, each split into two two-hour blocks with a 10-minute
break roughly every 50-60 minutes within a block, plus a longer break between
the two blocks of each session.

| Session | Block | Episode file | Topic | Time |
|---|---|---|---|---|
| 1 | 1 | `01-writing-functions.md` | Writing Effective Functions | 2h |
| 1 | 2 | `02-modules.md` | Organizing Functions into Modules | 2h |
| 2 | 3 | `03-repo-environments.md` | Repository + Environments | 2h |
| 2 | 4 | `04-documentation-reuse.md` | Documentation and Reuse | 2h |

## Design notes

- Each block builds directly on the previous one: the code learners write in
  Block 1 becomes the module in Block 2, the module becomes the repo in
  Block 3, and the repo gets documented and reused in Block 4. Avoid
  substituting your own example mid-workshop, or later challenges will not
  line up.
- Docstrings are introduced early (Block 1, at the function level) and
  revisited at the project level in Block 4. This is intentional — flag the
  callback for learners so it doesn't feel repetitive.
- Have learners work from the same "messy starter script" (see
  `learners/setup.md`) so that live-coding and challenges stay in sync across
  the room.
- Block 3's environment challenge assumes learners already have Python and
  git installed per the setup page — confirm this in a pre-workshop email,
  since debugging installs live eats into the two-hour block fast.

## Common sticking points

- Learners conflate "module" and "package" — Episode 2 explicitly
  distinguishes them; don't skip the terminology callout.
- `PATH` and environment activation issues are the most common Block 3
  derailment; consider a TA circulating during that challenge specifically.
