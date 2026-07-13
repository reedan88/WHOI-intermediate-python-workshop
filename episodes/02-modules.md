---
title: "Organizing Functions into Modules"
teaching: 80
exercises: 40
---

:::::::::::::::::::::::::::::::::::::: questions

- When does a collection of functions become a module?
- How does Python find code when I `import` it?
- How should I name and organize modules so a colleague can find things later?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain the difference between a script, a module, and a package
- Split a set of related functions into a module and import it elsewhere
- Apply naming and organization conventions to a small multi-module project

::::::::::::::::::::::::::::::::::::::::::::::::

## Why modules?

<!-- FIXME: introduce the motivating problem — the functions from Block 1
     now live in a script that's getting long, and/or need to be reused from
     a second script. Live-code moving them into `analysis.py`. -->

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: From script to module

<!-- FIXME: have learners move `summarize_readings` (and friends) from
     Block 1 into a new file, e.g. `sensors.py`. -->

:::::::::::::::::::::::: solution

<!-- FIXME -->

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Import mechanics

<!-- FIXME: cover `import module`, `from module import name`, `import module
     as alias`, and `__init__.py` for turning a directory into a package. -->

::::::::::::::::::::::::::::::::::::: callout

## Module vs. package

A **module** is a single `.py` file. A **package** is a directory of modules
with an `__init__.py`. Learners often use these terms interchangeably —
worth pausing on the distinction explicitly.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Import between two modules

<!-- FIXME: split code into two modules, e.g. `sensors.py` and
     `report.py`, where `report.py` imports from `sensors.py`. -->

:::::::::::::::::::::::: solution

<!-- FIXME -->

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Naming and organization conventions

<!-- FIXME: cover snake_case module names, avoiding shadowing stdlib names,
     grouping related modules into a package directory (e.g. `sensors/`
     containing `cleaning.py`, `stats.py`, `report.py`). -->

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Capstone — script to package

Starting from the original `messy_analysis.py`, produce a small package with
at least two modules and a clean top-level script that imports and calls them.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A module is a single `.py` file; a package is a directory of modules with an `__init__.py`
- `import`, `from ... import`, and `as` all change *how* a name is brought into scope, not what code runs
- Consistent naming and folder structure is what makes a project navigable to someone who didn't write it

::::::::::::::::::::::::::::::::::::::::::::::::
