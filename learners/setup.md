---
title: Setup
---

## Data Sets

Download the [starter files](../starter-files) and unzip them to your
Desktop before the workshop. This contains:

- `first_analysis.ipynb`: a deliberately "messy" Jupyter notebook that we
  refactor throughout the two sessions. Meant to reflect a type of exploratory
  notebook someone would use for initial data analysis/visualization.
- `data/gi01sumo_nsif_ctd.nc`, `data/gi01sumo_nsif_dosta.nc` — one week
  (2020-09-01 to 2020-09-08) of real [OOI](https://oceanobservatories.org/)
  Global Irminger Sea Array (GI01SUMO) Near-Surface Instrument Frame (NSIF) data:
  CTD (temperature, salinity, pressure) and DOSTA (dissolved oxygen). The data files
  contain a full-deployments worth of data but with only the relevant parameters
  retained. Downloading a similar dataset from the OOI Data Explorer will yield a dataset
  with a signficant number of extra, lower-processing-level parameters and engineering
  data.

<!-- FIXME: once this repo is on GitHub, replace the relative link above
     with a link to a release zip, e.g.
     https://github.com/FIXME/python-intermediate-workshop/releases -->

This data requires `xarray`, `netCDF4`, `pandas`, `numpy`, `Jupyter`, and
`matplotlib`. These should all be installed ahead of time, although Block 3
deals specifically with library and package management and environments.

```bash
pip install xarray netCDF4 pandas numpy matplotlib jupyter
python3 -c "import xarray as xr; print(xr.open_dataset('data/gi01sumo_nsif_ctd.nc'))"
```

## Software Setup

This workshop is written for a **Jupyter notebook** workflow and interactive programming
development approach. Terminal work should be limited, but there will be a few points where
learners will need to use the command line for a couple of things. That said, if the learner
wishes to use an IDE (such as VS-Code) they are welcome to.

::::::::::::::::::::::::::::::::::::::: discussion

### Details

You will need:

1. **Python 3.10+**
2. **Jupyter** (`pip install jupyter`, or JupyterLab)
    — Optional: A code editor with Python support (VS
      Code's Jupyter extension works well for editing the `.py` modules
      you'll write alongside your notebook)
3. **git**, and a free [GitHub](https://github.com) account
4. The ability to create a virtual environment (`venv`, `conda`, or `mamba`)


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
