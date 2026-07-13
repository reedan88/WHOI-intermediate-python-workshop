---
title: "Documentation and Reuse"
teaching: 80
exercises: 40
---

:::::::::::::::::::::::::::::::::::::: questions

- What does a README need to contain to actually be useful?
- How do docstrings work together across a whole project, not just one function?
- How do I safely reuse or update this repo for a new piece of work?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write a README that lets a new user install and run the project
- Audit docstrings across a small project for consistency
- Adapt an existing repository for a new but related task without breaking it

::::::::::::::::::::::::::::::::::::::::::::::::

## Writing a README

<!-- FIXME: cover the minimum viable README: what the project does, install
     instructions, a minimal usage example, and how to run tests (if any).
     Emphasize writing for someone who is *not* you in six months. -->

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Draft a README

Write a README for the repo built in Block 3, covering at least: purpose,
installation, and one usage example.

:::::::::::::::::::::::: solution

<!-- FIXME -->

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Docstrings at the project level

<!-- FIXME: revisit docstrings from Block 1 — now that there are multiple
     modules, check for consistent style across all of them. Optionally
     introduce a doc-generation tool (e.g. `pdoc` or `sphinx`) briefly. -->

::::::::::::::::::::::::::::::::::::: callout

## Callback to Block 1

<!-- FIXME: explicitly connect back to the docstrings written in Block 1 —
     this is the payoff for writing them early. -->

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Docstring audit

Check every function in the project for a docstring. Fix any that are
missing or inconsistent in style.

::::::::::::::::::::::::::::::::::::::::::::::::

## Reusing and updating the repo

<!-- FIXME: cover cloning the repo as a starting point for new but related
     work, updating dependencies safely, and a lightweight approach to
     versioning changes (git tags, or a CHANGELOG.md). -->

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Adapt for new work

Imagine a new sensor type needs the same summary statistics. Adapt the repo
to support it without duplicating the existing modules.

:::::::::::::::::::::::: solution

<!-- FIXME -->

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Workshop wrap-up

<!-- FIXME: brief recap connecting all four blocks — script to function
     (Block 1), function to module (Block 2), module to repo (Block 3),
     repo to shareable/reusable project (Block 4). -->

::::::::::::::::::::::::::::::::::::: keypoints

- A README's job is to let someone else install and run the project without asking you
- Docstring consistency matters more as a project grows past one file
- Reusing a repo well means updating it deliberately, not copy-pasting it

::::::::::::::::::::::::::::::::::::::::::::::::
