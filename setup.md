---
title: Setup
---

## Data Sets

Download the [starter files](../starter-files/data) and unzip them to your
Desktop before the workshop. This contains:

- `first_analysis.ipynb`: a deliberately "messy" Jupyter notebook that we
  refactor throughout the two sessions. Meant to reflect a type of exploratory
  notebook someone would use for initial data analysis/visualization.
- `data/gi01sumo_nsif_ctd.nc` and `data/gi01sumo_nsif_dosta.nc`: these are
  a full deployment of real [OOI](https://oceanobservatories.org/)
  Global Irminger Sea Array (GI01SUMO) Near-Surface Instrument Frame (NSIF) data:
  CTD (temperature, salinity, pressure) and DOSTA (dissolved oxygen). The data files
  contain a full-deployments worth of data but with only the relevant parameters
  retained. Downloading a similar dataset from the OOI Data Explorer will yield a dataset
  with a signficant number of extra, lower-processing-level parameters and engineering
  data.


## Software Setup

This workshop is written for a **Jupyter notebook** workflow throughout.
You won't need to run scripts from a terminal or work in a full IDE, though
either is fine if you already prefer one (e.g. PyCharm, VSCode, etc). 
You will use the terminal for a few short commands.

You will need:

1. **uv**, a tool that installs Python, creates environments, and installs
   packages. It replaces `venv`, `pip`, and (for this workshop) `conda`. You
   do **not** need to install Python separately; uv will download a suitable
   version when needed.
2. **git**, and a free [GitHub](https://github.com) account.
3. Optionally, a code editor with Python support (VS Code's Jupyter
   extension works well for editing the `.py` modules you'll write
   alongside your notebook).

:::::::::::::::: spoiler

### Windows

1. Open PowerShell and install uv:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   or, if you use WinGet: `winget install --id=astral-sh.uv -e`.
2. Install [Git for Windows](https://git-scm.com/download/win), which
   includes Git Bash.
3. **Close and reopen** your terminal, then check with `uv --version`.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### MacOS

1. Install uv, in Terminal:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   or, if you use Homebrew: `brew install uv`.
2. Git is usually pre-installed; verify with `git --version` in Terminal.
3. **Close and reopen** Terminal, then check with `uv --version`.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### Linux

1. Install uv:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install git via your package manager, e.g. `sudo apt install git`.
3. **Close and reopen** your terminal, then check with `uv --version`.

::::::::::::::::::::::::

If you already have `pip`, `pip install uv` also works, but the installers
above are preferred because they don't depend on any particular Python.

## Check your setup before the workshop

Do this once, with an internet connection, **before** the first session. It
downloads the packages we use so that the workshop itself isn't spent
waiting on them. In a terminal, go to the unzipped starter-files folder
and run:

```bash
cd Desktop/starter-files
uv run --no-project --with jupyterlab --with xarray --with netCDF4 --with pandas --with numpy --with matplotlib jupyter lab
```

The first run can take a few minutes and downloads several hundred
megabytes. When it finishes, JupyterLab opens in your browser. Open
`messy_analysis.ipynb` and run the first few cells; if the dataset prints,
you are ready. Close JupyterLab by pressing `Ctrl+C` in the terminal.

Run the same command again and it should start within seconds, because uv
re-uses what it downloaded.

This is the command we use in Blocks 1 and 2, before we have created a
project of our own. In Block 3 you'll replace it with a project that
records these dependencies for you.

::::::::::::::::::::::::::::::::::::::: discussion

### What `--no-project` and `--with` mean

`--with jupyterlab` (and the others) asks uv to build a temporary
environment containing those packages and run the command inside it.
`--no-project` stops uv from looking for a `pyproject.toml` in the current
folder, since you don't have one yet.

:::::::::::::::::::::::::::::::::::::::::::::::::::
