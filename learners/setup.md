---
title: Setup
---

## Data Sets

Download the [starter files](../starter-files) and unzip them to your
Desktop before the workshop. This contains:

- `messy_analysis.ipynb` — a deliberately "messy" Jupyter notebook that we
  refactor throughout the two sessions
- `data/gs01sumo_nsif_ctd.nc`, `data/gs01sumo_nsif_dosta.nc` — one week
  (2020-09-01 to 2020-09-08) of real [OOI](https://oceanobservatories.org/)
  Global Irminger Sea Array (GS01SUMO) near-surface instrument frame data:
  CTD (temperature, salinity, pressure) and DOSTA (dissolved oxygen),
  trimmed down from the full year-long deployment record so the files stay
  small enough to work with comfortably in a workshop setting

<!-- FIXME: once this repo is on GitHub, replace the relative link above
     with a link to a release zip, e.g.
     https://github.com/FIXME/python-intermediate-workshop/releases -->

This data requires `xarray`, `netCDF4`, `pandas`, `numpy`, and
`matplotlib` — installing these is part of Block 3, but if you'd like to
confirm ahead of time that things work on your machine:

```bash
pip install xarray netCDF4 pandas numpy matplotlib jupyter
python3 -c "import xarray as xr; print(xr.open_dataset('data/gs01sumo_nsif_ctd.nc'))"
```

## Software Setup

This workshop is written for a **Jupyter notebook** workflow throughout —
you won't need to run scripts from a terminal or work in a full IDE, though
either is fine if you already prefer one.

::::::::::::::::::::::::::::::::::::::: discussion

### Details

You will need:

1. **Python 3.10+**
2. **Jupyter** (`pip install jupyter`, or JupyterLab if you prefer) —
   and, if you have a preference, a code editor with Python support (VS
   Code's Jupyter extension works well for editing the `.py` modules
   you'll write alongside your notebook)
3. **git**, and a free [GitHub](https://github.com) account
4. The ability to create a virtual environment (`venv`, `conda`, or `mamba`)
5. The `jupyter-autoreload` behavior (built into IPython/Jupyter already —
   nothing extra to install) — we'll turn this on in Block 2 so edits to
   your own `.py` files show up in the notebook without restarting the
   kernel

:::::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::: spoiler

### Windows

1. Install Python from [python.org](https://python.org) — check "Add
   Python to PATH" during install.
2. Install [Git for Windows](https://git-scm.com/download/win), which
   includes Git Bash.
3. `pip install jupyter`, then confirm it launches with `jupyter notebook`
   or `jupyter lab`.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### MacOS

1. Install Python 3 via [python.org](https://python.org) or `brew install python`.
2. Git is usually pre-installed; verify with `git --version` in Terminal.
3. `pip install jupyter`, then confirm it launches with `jupyter notebook`
   or `jupyter lab`.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### Linux

1. Python 3 is usually pre-installed; verify with `python3 --version`.
2. Install git via your package manager, e.g. `sudo apt install git`.
3. `pip install jupyter`, then confirm it launches with `jupyter notebook`
   or `jupyter lab`.

::::::::::::::::::::::::
