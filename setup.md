---
title: Setup
---

## Before the workshop

Please complete the [Getting Started](getting-started.md) page **before
Session 1**. It walks you through installing the three things you need
(git, uv, and a GitHub account), downloading the workshop files, and testing
that everything works. We will not have time to troubleshoot installations
during the sessions.

## The workshop files

The starter files are distributed as a single zip file, `starter-files.zip`,
on the lesson's
[Releases page](https://github.com/reedan88/WHOI-intermediate-python-workshop/releases/latest).
It contains:

- `first_analysis.ipynb`: a deliberately "messy" Jupyter notebook that we
  refactor throughout the two sessions. It reflects the kind of exploratory
  notebook someone would use for initial data analysis and visualization.
- `data/gi01sumo_nsif_ctd.nc` and `data/gi01sumo_nsif_dosta.nc`: a full
  deployment of real [OOI](https://oceanobservatories.org/) data from the
  Global Irminger Sea Array (GI01SUMO) Near-Surface Instrument Frame (NSIF):
  CTD (temperature, salinity, pressure, density) and DOSTA (dissolved
  oxygen). The files keep only the relevant parameters. Downloading a similar
  dataset from the OOI Data Explorer yields many more lower-processing-level
  parameters and engineering data.

The data files are large (roughly 120 MB for the CTD and 800 MB for the DOSTA).

## Software

You need three things, all covered in [Getting Started](getting-started.md):

1. **uv**, a tool that installs Python, creates environments, and installs
   packages. It replaces `venv`, `pip`, and (for this workshop) `conda`. You
   do **not** need to install Python separately.
2. **git**.
3. A free [GitHub](https://github.com) account.

The workshop is written for a **Jupyter notebook** workflow. You will use a
terminal for a few short commands. Using another editor or IDE (VS Code,
PyCharm, and so on) is fine if you already prefer one.
