---
title: "Building a Repository and Managing Environments"
teaching: 90
exercises: 50
---

:::::::::::::::::::::::::::::::::::::: questions

- What actually belongs in a code repository?
- Why does each project need its own environment?
- How do I turn `mooring_tools/` into something `pip install`-able?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Lay out a repository with a `src/` (aka "source") package, notebooks, and data kept separate
- Create an isolated virtual environment and install the project into it in "editable" mode
- Explain why a `src/` layout catches packaging bugs that a flat layout hides
- Generate a dependency file that lets someone else reproduce your environment

::::::::::::::::::::::::::::::::::::::::::::::::

## What goes in a repo

By the end of Block 2, `mooring_tools/` is three modules and an
`__init__.py`, sitting next to `messy_analysis.ipynb`. That's enough to
import from this notebook. It's not enough to `pip install`, share with 
a colleague, or use from a notebook anywhere else on your machine. 
For that, the package needs a proper home:

```text
mooring-tools/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── mooring_tools/
│       ├── __init__.py
│       ├── stats.py
│       ├── plotting.py
│       └── merge.py
├── notebooks/
│   └── messy_analysis.ipynb
└── data/
    ├── gs01sumo_nsif_ctd.nc
    └── gs01sumo_nsif_dosta.nc
```

A few things to note about the layout:

- `src/mooring_tools/`, not just `mooring_tools/` as the repo root.
- `notebooks/` and `data/` are separate from the package. The package
  is code meant to be imported; the notebook is one particular analysis
  that uses it.
- **`.gitignore`** keeps generated/environment files out of version
  control, such as the venv folder, `__pycache__/`, and Jupyter checkpoint files.
- **`LICENSE`** states what others are allowed to do with the code.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Lay out the repository

Create this directory structure, moving `stats.py`, `plotting.py`, and
`merge.py` (and `__init__.py`) into `src/mooring_tools/`, and
`messy_analysis.ipynb` into `notebooks/`. Don't worry about
`pyproject.toml` yet.

::::::::::::::::::::::::::::::::::::::::::::::::

## Why `src/`, specifically

Compare two layouts, both without the package actually installed:

```bash
# flat layout: mooring_tools/ directly at the repo root
cd flat-layout-repo
python3 -c "import mooring_tools"
```
```output
(imports successfully — from mooring_tools/__init__.py right there in the folder)
```

```bash
# src layout: mooring_tools/ inside src/
cd src-layout-repo
python3 -c "import mooring_tools"
```
```output
ModuleNotFoundError: No module named 'mooring_tools'
```

With a flat layout, Python finds the package because your current
directory is always searched first. That means `import mooring_tools`
can silently "work" from inside the repo even if the package was never
actually installed, or if the install is broken. The bug only shows up
later, when someone tries to use the package from outside the repo and
it's nowhere to be found. With `src/`, that failure happens immediately.


::::::::::::::::::::::::::::::::::::::::::::::::

## Environments

Every Python installation on your machine has one set of installed
packages by default. If two projects need different, incompatible
versions of the same library, installing globally means only one project
can work at a time. A virtual environment gives each project its own
isolated set of installed packages.

```bash
python3 -m venv .venv

# activate it:
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate            # Windows
```

Once activated, `pip install` only affects this environment. Other
projects, and the system Python, are untouched.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Create an environment

Create a virtual environment for `mooring-tools` and activate it.
Confirm you're in it: `which python` (macOS/Linux) or `where python`
(Windows) should point inside the `.venv` folder, not your system Python.

::::::::::::::::::::::::::::::::::::::::::::::::

## Making the package installable

`pyproject.toml` (Tom's Obvious Minimal Language), at the repo root, is what turns a `src/` folder into something `pip` understands:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mooring_tools"
version = "0.1.0"
description = "Burst-statistics, plotting, and merge utilities for OOI CTD/DOSTA data"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "you@example.org" },
]
dependencies = [
    "xarray>=2024.1",
    "netCDF4>=1.6",
    "pandas>=2.0",
    "numpy>=1.24",
    "matplotlib>=3.7",
]

[project.optional-dependencies]
notebook = ["jupyter"]

[tool.setuptools.packages.find]
where = ["src"]
```

The last two lines are what tell `setuptools` to look inside `src/` for
packages, rather than the repo root. With this in place:

```bash
pip install -e .
```

This command installs `mooring_tools` in **editable mode** (this is the `-e .`). `pip` points at your `src/mooring_tools/` files directly rather than copying them, so edits
you make take effect immediately without reinstalling.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Install the package into your environment

Write the `pyproject.toml` above (adjust name/email), then run
`pip install -e .` from the repo root. Confirm it worked by opening a
Python shell from a different directory entirely and running:

```python
import mooring_tools
from mooring_tools.stats import resample_burst_stats
print(mooring_tools.__file__)
```

The printed path should point at your repo's `src/mooring_tools/`, even
though you are working in a different folder.

:::::::::::::::::::::::: solution

If this raises `ModuleNotFoundError`, the most common cause is running
`pip install -e .` with the wrong environment active. Double check
`which pip` points inside `.venv` before installing.

::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Package management: pinning dependencies

`pyproject.toml`'s `dependencies` list uses minimum versions
(`xarray>=2024.1`), enough to achieve what's required, loose enough to
not fight with other projects. For *exact reproducibility* generate a fully pinned lock
file from your working environment:

```bash
pip freeze > requirements.txt
```

From this project's tested environment, that produces something like:

```text
matplotlib==3.11.2
netCDF4==1.7.4
numpy==2.4.6
pandas==3.0.6
xarray==2026.7.0
-e /path/to/mooring-tools
```

The distinction matters: `pyproject.toml` says what your *code* needs to
run at all; `requirements.txt` (or a proper lock file) says exactly what
*this specific environment* has installed, version by version. A
colleague reproducing your result wants the second one.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 4: Generate a lock file

Run `pip freeze > requirements.txt` in your activated environment. Then,
starting from a fresh virtual environment, confirm a teammate could
reproduce it with `pip install -r requirements.txt`.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## `.gitignore` for this project

Virtual environments and Jupyter checkpoint files don't belong in version
control. A minimal `.gitignore` for this repo will look something like this:

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
```

If your data files are large or sensitive, consider whether `data/`
belongs in `.gitignore` too, with a note in the README on where to get it.

::::::::::::::::::::::::::::::::::::::::::::::::

## Wrap-up

By the end of this block, `mooring_tools` is a real, installable package:
`src/` layout, `pyproject.toml`, an activated virtual environment it's
installed into with `pip install -e .`, and a `requirements.txt` capturing
exactly what's installed. Block 4 adds the README and docstring pass that
makes this repo usable by someone who isn't you.

::::::::::::::::::::::::::::::::::::: keypoints

- Separate the installable package (`src/mooring_tools/`) from notebooks and data
- A `src/` layout turns "the package isn't actually installed" from a silent bug into an error with a traceback
- `pip install -e .` installs your package so edits to `src/` take effect immediately, from any project, without reinstalling
- `pyproject.toml` declares what your code needs (loose bounds); `requirements.txt`/`pip freeze` records exactly what's installed (exact pins)

::::::::::::::::::::::::::::::::::::::::::::::::
