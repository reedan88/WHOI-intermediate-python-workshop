---
title: "Building a Repository and Managing Environments"
teaching: 80
exercises: 40
---

:::::::::::::::::::::::::::::::::::::: questions

- What actually belongs in a code repository, beyond the code itself?
- Why does each project need its own environment?
- How do I record and share which packages a project depends on?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Initialize a git repository with a sensible directory structure
- Create an isolated virtual environment for a project
- Generate and use a dependency file (`requirements.txt` or `pyproject.toml`)

::::::::::::::::::::::::::::::::::::::::::::::::

## What goes in a repo

<!-- FIXME: walk through a minimal but complete repo layout, e.g.:
     project/
       README.md
       LICENSE
       .gitignore
       pyproject.toml (or requirements.txt)
       src/project_name/
       tests/
     Discuss what each piece is for and why tests/README/.gitignore matter
     even for a "just for me" project. -->

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Initialize the repo

<!-- FIXME: `git init`, add the package from Block 2 into `src/`, write a
     first `.gitignore` (Python template), first commit. -->

:::::::::::::::::::::::: solution

<!-- FIXME -->

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Environments

<!-- FIXME: explain *why* (dependency conflicts between projects), then
     demonstrate venv (`python -m venv .venv`) and/or conda, activating,
     and installing a package into it. -->

::::::::::::::::::::::::::::::::::::: callout

## "Why not just install everything globally?"

<!-- FIXME: a good callout for the most common pushback in this section —
     conflicting version requirements across unrelated projects. -->

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Create an environment for the project

Create a virtual environment for the repo from Challenge 1 and install one
external dependency into it (e.g. `numpy`).

:::::::::::::::::::::::: solution

<!-- FIXME -->

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Package management

<!-- FIXME: `requirements.txt` (`pip freeze > requirements.txt`) vs.
     `pyproject.toml` (declared dependencies, editable installs with
     `pip install -e .`), and pinning versions vs. leaving them open. -->

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Record dependencies

Generate a dependency file for the environment you created, and confirm a
teammate could recreate it from a clean environment.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A repo is more than code: structure, `.gitignore`, and a dependency file are part of making it usable by someone else
- Each project gets its own environment to avoid dependency conflicts
- Recording exact dependencies (with versions) is what makes a project reproducible

::::::::::::::::::::::::::::::::::::::::::::::::
