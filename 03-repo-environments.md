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

- Create a project with `uv` and lay out a repository with a `src/` package, notebooks, and data kept separate
- Add dependencies to a project and explain what `pyproject.toml` and `uv.lock` each record
- Run a Jupyter notebook inside the project's environment and import your own package from it
- Explain why a `src/` layout catches packaging bugs that a flat layout hides

::::::::::::::::::::::::::::::::::::::::::::::::

## What goes in a repo

By the end of Block 2, `mooring_tools/` is three modules and an
`__init__.py`, sitting next to `first_analysis.ipynb`. That's enough to
import from this notebook. It's not enough to share with 
a colleague, or use from a notebook anywhere else on your machine. 
For that, the package needs a proper home:

```text
gs01sumo-mooring-tools/
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
├── pyproject.toml
├── uv.lock
├── src/
│   └── mooring_tools/
│       ├── __init__.py
│       ├── stats.py
│       ├── plotting.py
│       └── merge.py
├── notebooks/
│   └── first_analysis.ipynb
└── data/
    ├── gi01sumo_nsif_ctd.nc
    └── gi01sumo_nsif_dosta.nc
```

A few things to note about the layout:

- **`src/mooring_tools/`**, not just **`mooring_tools/`** as the repo root.
- **`notebooks/`** and **`data/`** are separate from the package. The package
  is code meant to be imported; the notebook is one particular analysis
  that uses it.
- **`pyproject.toml`** and **`uv.lock`** describe the project and the exact
  packages it was run with. Both are committed. We'll build them up over
  this block.
- **`.python-version`** records which version of Python the project is
  developed with.
- **`.gitignore`** keeps generated/environment files out of version
  control, such as the venv folder, `__pycache__/`, and Jupyter checkpoint files.
- **`LICENSE`** states what others are allowed to do with the code.

## Creating the project with uv

You could create all of that by hand. Instead, we'll let
[uv](https://docs.astral.sh/uv/) create the skeleton. `uv` is one tool that
replaces several you may have used separately: it installs Python itself,
creates virtual environments, installs packages, and records what it
installed. Confirm it's available:

```bash
uv --version
```

Then create the project:

```bash
uv init --lib --name mooring-tools gi01sumo-mooring-tools
```

- `--lib` asks for a **library** layout: a `src/` folder with a package
  inside it, ready to be imported by other code.
- `--name mooring-tools` is the name the project is installed under. The
  folder is named `gi01sumo-mooring-tools`, so we give the name explicitly.
- uv also runs `git init` for you, so the folder is already a repository.

::::::::::::::::::::::::::::::::::::: callout

## Two names for one thing

The project is called `mooring-tools` (with a hyphen) but you import it as
`mooring_tools` (with an underscore). The first is the name used to install
and publish it; the second is a Python identifier, so it can't contain a
hyphen. `uv` turns one into the other automatically. If you see
`ModuleNotFoundError: No module named 'mooring-tools'`, that's the mix-up.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Lay out the repository

1. Run the `uv init` command above, then `cd` into the new folder and look
   at what it created (`ls -a`, or `dir` on Windows).
2. `uv init` puts a placeholder `hello()` function in
   `src/mooring_tools/__init__.py`. Replace that file with your `__init__.py`
   from Block 2, and move `stats.py`, `plotting.py`, and `merge.py` into
   `src/mooring_tools/`.
3. Create `notebooks/` and `data/`, and move `first_analysis.ipynb` and the
   two `.nc` files into them. (Update the data paths in the notebook to
   `../data/...`.)

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
can work at a time. A **virtual environment** gives each project its own
isolated set of installed packages.

With uv you don't create or activate one yourself. The first time you add a
dependency (next section), uv creates a `.venv` folder in the project and
installs into it. Every `uv run ...` command then uses that environment
automatically, from the project folder or any folder inside it. There is no
`activate` step to forget, and no way to install into the wrong environment
by accident.

::::::::::::::::::::::::::::::::::::: callout

## The `.venv` folder is disposable

Nothing in `.venv` is precious. If it ever gets into a confusing state,
delete the folder and run `uv sync`. `uv` will rebuild it from the project files.
That is also why `.venv` is in `.gitignore`: it's machine-specific, and
fully recreatable.

::::::::::::::::::::::::::::::::::::::::::::::::

## Making the package installable

`pyproject.toml` (Tom's Obvious Minimal Language), at the repo root, is what turns a `src/` folder into something `pip` understands:

```toml
[project]
name = "mooring-tools"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = [
    { name = "Your Name", email = "you@example.org" }
]
requires-python = ">=3.14"
dependencies = []

[build-system]
requires = ["uv_build>=0.11.32,<0.12.0"]
build-backend = "uv_build"
```

Two things need your attention before we go on. (Your version numbers and
author will differ.)

- **`requires-python`** defaults to the version of Python uv found on *your*
  machine. If yours is 3.14, a colleague on 3.11 would be told they cannot
  install your package, for no real reason. Our code runs fine on older
  versions, so relax it to `">=3.10"`.
- **`description`** should say what the package does. Make it
  `"Burst-statistics, plotting, and merge utilities for OOI GS01SUMO CTD/DOSTA data"`.

The `[build-system]` table tells tools how to turn `src/` into an
installable package. uv fills it in; you don't need to edit it.

## Adding dependencies

Our code needs `xarray`, `netCDF4`, `pandas`, `numpy`, and `matplotlib`.
Add them with:

```bash
uv add xarray netcdf4 pandas numpy matplotlib
```

That one command does three things:

1. creates `.venv` if it doesn't exist yet,
2. installs the packages (and everything they depend on) into it
3. records them in two places.

Look at `pyproject.toml` again:

```toml
dependencies = [
    "matplotlib>=3.10.9",
    "netcdf4>=1.7.3",
    "numpy>=2.2.6",
    "pandas>=2.3.3",
    "xarray>=2025.6.1",
]
```

uv has written a **minimum** version for each one: the version it
installed, or the oldest version that works with the oldest Python you
allow. This says what your code needs to run at all, loose enough not to
fight with other projects.

For notebooks, add JupyterLab as a **development** dependency. This is something
you need to work on the project, but that someone else who is only using 
`mooring_tools` does not:

```bash
uv add --dev jupyterlab
```

```toml
[dependency-groups]
dev = [
    "jupyterlab>=4.6.5",
]
```
::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Set up the project's dependencies

In the project folder, fix `requires-python` and `description` in
`pyproject.toml`, then run both `uv add` commands above. Open
`pyproject.toml` and confirm the `dependencies` and `[dependency-groups]`
tables were filled in for you. Which new files and folders has uv created?

:::::::::::::::::::::::: solution

`.venv/` (the environment, git-ignored) and `uv.lock` (the exact record of
what was installed, which we look at shortly). `pyproject.toml` itself was
edited by `uv add`.

Your minimum versions will differ from the ones above, because they reflect
whatever was current when you ran the command.

::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Running code in the project

To run a command inside the project's environment, put `uv run` in front of
it:

```bash
uv run python -c "import mooring_tools; print(mooring_tools.__file__)"
```

The printed path should point into your repo's `src/mooring_tools/`. uv
installs your own package into `.venv` in editable mode: Python imports
it directly from your `src/` files rather than from a copy, so edits you make
take effect immediately without reinstalling (This is the persistent cousin 
of Block 2's `%autoreload`).

Now start JupyterLab inside the project:

```bash
uv run jupyter lab
```

Open `notebooks/first_analysis.ipynb`. The notebook's kernel is the
project's `.venv` Python, so `import mooring_tools` simply works.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Use the package from a notebook

Launch JupyterLab with `uv run jupyter lab` from the repo root. In a new
notebook inside `notebooks/`, run:

```python
import mooring_tools
from mooring_tools.stats import resample_burst_stats
print(mooring_tools.__file__)
```

Then change the body of a function in `src/mooring_tools/stats.py` (for
example, the default `freq`), and call it again. Do you need to restart the
kernel? (Remember what `%autoreload 2` did in Block 2.)

:::::::::::::::::::::::: solution

The printed path points at your repo's `src/mooring_tools/`. Whether the
edit shows up without a restart depends on whether you ran
`%load_ext autoreload` and `%autoreload 2`: the editable install makes the
package findable from anywhere, while `autoreload` makes already-imported
code refresh in a running kernel.

If `import mooring_tools` raises `ModuleNotFoundError`, the notebook is
almost certainly running in a different Python than the project's. Check
that you started JupyterLab with `uv run jupyter lab`, not with a `jupyter`
installed elsewhere on your machine.

::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Package management: the lock file

`pyproject.toml` has loose, minimum versions. For exact reproducibility look at the other file
uv created: `uv.lock`. It records the exact version of every package in the
environment, including the ones you never asked for directly (`xarray`
pulls in `packaging`, `pandas` pulls in `python-dateutil`, and so on):

```text
[[package]]
name = "xarray"
version = "2026.9.0"
...
```

(You don't write or edit `uv.lock`; uv maintains it every time you
`uv add`, `uv remove`, or `uv lock`.)

The difference between `pyproject.toml` and `uv.lock` is that the former
declares what is needed to run your code whereas the latter states exactly
what your environment has installed at the time that `uv` was run.
installed, version by version. The lock file covers every platform and Python version your
project supports, so a lock file made on a Mac works on Windows and Linux.

Commit both files. Then reproducing your environment on a new machine is:

```bash
git clone <repo-url>
cd gi01sumo-mooring-tools
uv sync
```

`uv sync` creates `.venv` and installs exactly what `uv.lock` says. If
the right Python isn't installed on the new machine, uv downloads it too.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 4: Reproduce your environment

Commit your work (`git add .` then `git commit`). Then, in a *different*
folder, clone your own repo and run `uv sync`. Compare the output of
`uv run python -c "import xarray; print(xarray.__version__)"` in the clone
and in your original. What do you expect?

When that works, delete the `.venv` folder in your *original* project and
run `uv sync` again. How long does it take compared to the first time?

:::::::::::::::::::::::: solution

The versions match, because both environments were built from the same
`uv.lock`.

Rebuilding is much faster the second time: uv keeps a cache of everything
it has already downloaded, so a rebuild is mostly linking files from that
cache into a new `.venv`.

::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Changing your mind later

You'll rarely get the dependency list right the first time. The same
commands work whenever you need them:

```bash
uv add scipy           # new dependency
uv remove scipy        # no longer needed
uv lock --upgrade      # move to the newest versions allowed, then...
uv sync                # ...bring .venv in line with uv.lock
```

Each of these edits `pyproject.toml` and/or `uv.lock` for you, so the two
files and the environment stay consistent. Commit the changed files
together.

::::::::::::::::::::::::::::::::::::: callout

## `.gitignore` and what to commit

`uv init` already wrote a `.gitignore` containing `.venv`, `__pycache__/`,
`*.py[oc]`, `build/`, `dist/`, `wheels/`, and `*.egg-info`. Add one line for
Jupyter:

```text
.ipynb_checkpoints/
```

Commit: `pyproject.toml`, `uv.lock`, `.python-version`, `README.md`,
`LICENSE`, and everything under `src/` and `notebooks/`. Don't commit
`.venv/`.

If your data files are large or sensitive, consider whether `data/`
belongs in `.gitignore` too, with a note in the README on where to get it.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## What about conda?

Many scientists use conda or mamba, and for good reason: it can install
non-Python libraries (compilers, GDAL, and so on) that `uv` cannot. Every
package in this workshop is available as a pre-built wheel for macOS,
Windows, and Linux, so `uv` is enough here. If a future project needs
non-Python system libraries, conda remains a sensible choice for that
project. The ideas in this block — one environment per project, minimum
versions in the project file, exact versions in a lock file, commit both —
apply either way.

::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: instructor

Two practical points. First, uv must be on each learner's `PATH` in a
**new** terminal window; "command not found: uv" right after installing is
almost always an old terminal. Second, the first `uv add` downloads several
hundred megabytes (xarray, pandas, numpy, matplotlib, netCDF4, and
JupyterLab with its dependencies). On workshop wifi, have learners run
Challenge 2 at the same time rather than one at a time, or pre-warm uv's
cache by asking them to run the commands from `learners/setup.md` before
the session.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Wrap-up

By the end of this block, `mooring_tools` is a real, installable package:
`src/` layout, a `pyproject.toml` declaring what it needs, a `uv.lock`
recording exactly what was installed, and an environment that uv builds and
uses without any activation. A colleague can reproduce all of it with
`git clone` and `uv sync`. Block 4 adds the README and docstring pass that
makes this repo usable by someone who isn't you.

::::::::::::::::::::::::::::::::::::: keypoints

- Separate the installable package (`src/mooring_tools/`) from notebooks and data
- A `src/` layout turns "the package isn't actually installed" from a silent bug into a raised error
- `uv init --lib` creates the project skeleton; `uv add` installs a dependency and records it in `pyproject.toml` and `uv.lock`
- `uv run` runs a command in the project's environment with nothing to activate; the `.venv` folder is disposable and never committed
- `pyproject.toml` declares what your code needs (minimum versions); `uv.lock` records exactly what's installed: commit both, and reproduction is `git clone` plus `uv sync`

::::::::::::::::::::::::::::::::::::::::::::::::

