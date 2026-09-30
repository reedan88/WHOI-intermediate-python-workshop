---
title: "Organizing Functions into Modules"
teaching: 90
exercises: 50
---

:::::::::::::::::::::::::::::::::::::: questions

- When does a collection of functions become a module?
- How do I use my own modules from a Jupyter notebook, not just a script?
- How should I decide what becomes a module, and what doesn't?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain the difference between a script, a module, and a package
- Import a local module into a running notebook, and pick up edits without restarting the kernel
- Split a set of related functions into modules by responsibility, not by dataset
- Recognize when *not* to make something a module

::::::::::::::::::::::::::::::::::::::::::::::::

## Why modules?

By the end of Part 1, `messy_analysis.ipynb` has two good functions in it:
`resample_burst_stats` and `fill_harmonic_gaps`. But they're still living in
notebook cells. If next month you or someone else wants to reuse
`resample_burst_stats` for a third instrument in a *different* notebook,
they'd have to copy the function out of this one by hand, which is *not* what
we want to be doing.

Instead, we are going to put the functions into a **module**. A module is a single `.py` file that other code can `import`. This is how we make a function reusable *outside* the notebook that first needed it.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: From notebook cell to module

Create a new file, `stats.py`, next to `messy_analysis.ipynb`, and move
`resample_burst_stats` and `fill_harmonic_gaps` into it, along with whatever
`import` lines they need (`numpy`, `pandas`).

:::::::::::::::::::::::: solution

```python
# stats.py
"""Burst-statistics and gap-filling for OOI instrument time series."""

import numpy as np
import pandas as pd


def resample_burst_stats(df: pd.DataFrame, freq: str = "900s") -> pd.DataFrame:
    """Compute burst-median statistics for OOI instrument data."""
    resampler = df.resample(freq, origin="start_day", offset=pd.Timedelta("3150s"))
    median = resampler.median()

    group_median = resampler.transform("median")
    deviations = (df - group_median).abs()
    mad = deviations.resample(freq, origin="start_day", offset=pd.Timedelta("3150s")).median()

    stats = pd.concat([median, mad], axis=1, keys=["median", "mad"]).swaplevel(axis=1).sort_index(axis=1)
    stats.index = stats.index + pd.Timedelta(freq) / 2
    return stats


def fill_harmonic_gaps(series: pd.Series, periods=("365.25D", "182.625D")):
    """Fill NaNs in a time-indexed Series with a trend + harmonic fit."""
    t = (series.index - series.index[0]) / pd.Timedelta("1s")
    omegas = [2 * np.pi / (pd.Timedelta(p) / pd.Timedelta("1s")) for p in periods]

    X = np.column_stack([
        np.ones_like(t),
        t,
        *[f(omega * t) for omega in omegas for f in (np.cos, np.sin)],
    ])

    valid = series.notna().values
    coeffs, *_ = np.linalg.lstsq(X[valid], series.values[valid], rcond=None)

    fitted = pd.Series(X @ coeffs, index=series.index)
    filled = series.where(valid, fitted)
    return filled, fitted
```

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Importing your own module into a notebook

With `stats.py` sitting next to `messy_analysis.ipynb`, a notebook cell can
import it exactly like any other package:

```python
from stats import resample_burst_stats, fill_harmonic_gaps
```

::::::::::::::::::::::::::::::::::::: callout

## autoreload: editing a module without restarting the kernel

By default, once a notebook has imported a module, editing that module's
`.py` file and re-running the import cell does *nothing* because Python caches
the module after the first import. Thus any changes you made in the module
will not be picked up by the notebook/script/other module you are using.

The fix is two "magic" commands at the top of the notebook, before any of
your own imports:

```python
%load_ext autoreload
%autoreload 2
```

With this turned on, editing `stats.py` in your editor and re-running a
cell that calls `resample_burst_stats(...)` picks up the change immediately. This is the single biggest quality-of-life fix for a notebook + local-module workflow, and a much better approach than restarting the kernel and rerunning all of your cells.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## A real, reproducible gotcha: don't shadow the standard library

Watch what happens if a module happens to share a name with something in
Python's standard library. In an empty scratch folder:

```bash
echo "pass" > random.py
python3 -c "import numpy as np; np.random.rand(3)"
```

```output
ImportError: cannot import name 'SystemRandom' from 'random' (/.../random.py)
```

NumPy tried to `import random` internally and got *your* empty file instead
of the real standard-library module, three layers deep in someone else's
code. `random.py`, `csv.py`, `json.py`, `types.py`, and `test.py` are the
classic examples because Python and, by extension, Jupyter notebooks, always
checks your notebook's own directory before the standard library. 

::::::::::::::::::::::::::::::::::::::::::::::::

## Deciding what becomes a module

It's tempting to make a module for every conceptual piece of the pipeline. Let's
take a look at what a module for loading the data in this workflow would actually contain:

```python
def load_ooi_dataset(path):
    return xr.open_dataset(path)
```

One line, wrapping one library call, with nothing project-specific in it.
A module built around this doesn't save future-you any real work because ``xarray.open_dataset``` already is one line. **Modularize logic that's
substantial, reusable, or repeated.** 

What *does* deserve a module in our notebook? The plotting code. Scroll through
`messy_analysis.ipynb` and count how many nearly-identical plotting cells
it has. This is the type of repeated code that makes sense as a function and a module.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Extract a plotting module

Pull the repeated plotting logic out of `messy_analysis.ipynb` into
`plotting.py`, with one function per distinct *kind* of plot (not one
function per cell). Aim for something like:

- `plot_raw_timeseries(ctd, dosta, t1=None, t2=None)`
    * the raw temperature/salinity/oxygen plots (used at three different zoom levels
  in the notebook)
- `plot_burst_stats(raw, stats, var, label, color, t1=None, t2=None)`
    * raw points with the burst-median ± 2·MAD band

:::::::::::::::::::::::: solution

```python
# plotting.py
"""Plotting helpers for OOI CTD/DOSTA burst-statistics time series."""

import matplotlib.pyplot as plt


def plot_raw_timeseries(ctd, dosta, t1=None, t2=None):
    """Plot raw (unresampled) CTD temperature/salinity and DOSTA oxygen."""

    # Subset the data based on the window to look at
    window = slice(t1, t2)
    ctd_w = ctd.sel(time=window)
    dosta_w = dosta.sel(time=window)

    # Plot the first subplot
    fig, (ax, axb) = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

    ax.plot(ctd_w["time"], ctd_w["sea_water_temperature"], color="tab:red",
            linestyle="", marker=".", label="Temperature (°C)")
    ax.set_ylabel("Temperature (°C)", color="tab:red")
    ax.set_title("Irminger Sea Temperature and Salinity at 12m Depth")

    # Create a second y-axis on the first subplot
    ax2 = ax.twinx()
    ax2.plot(ctd_w["time"], ctd_w["sea_water_practical_salinity"], color="tab:blue",
              linestyle="", marker=".", label="Salinity (PSU)")
    ax2.set_ylabel("Salinity (PSU)", color="tab:blue")
    ax.grid()
    ax2.grid()

    # Plot the second subplot
    axb.plot(dosta_w["time"], dosta_w["oxygen_concentration_corrected"], color="tab:green",
              linestyle="", marker=".", label="Oxygen (µmol/kg)")
    axb.set_ylabel("Oxygen (µmol/kg)", color="tab:green")
    axb.grid()

    fig.autofmt_xdate()
    return fig


def plot_burst_stats(raw, stats, var, label, color, t1=None, t2=None):
    """Plot raw points against burst-median +/- 2*MAD for one variable."""

    # Subset the data based on the window to look at
    window = slice(t1, t2)
    raw_w = raw.sel(time=window)
    median = stats[var]["median"].loc[window]
    mad = stats[var]["mad"].loc[window]

    # Plot the subsetted data
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.plot(raw_w["time"], raw_w[var], color=color, linestyle="", marker=".",
            alpha=0.4, label="Raw")
    ax.plot(median.index, median, color=color, label="Burst median")
    ax.fill_between(median.index, median - 2 * mad, median + 2 * mad,
                     color=color, alpha=0.3, linewidth=0, label="±2 MAD")
    ax.set_ylabel(label)
    ax.set_title(f"{label}: burst median ± 2 MAD")
    ax.legend()
    ax.grid()
    fig.autofmt_xdate()
    return fig
```

In the notebook the plotting cells collapse to:

```python
plot_raw_timeseries(ctd, dosta)
plot_raw_timeseries(ctd, dosta, t1="2020-09-01", t2="2020-09-08")
plot_raw_timeseries(ctd, dosta, t1="2020-09-01T03:00:00", t2="2020-09-01T04:00:00")
```

This is much cleaner and easier to read.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Fixing real bugs while modularizing

Scroll to the "Merge and save" section at the bottom of
`messy_analysis.ipynb` which is currently unfinished.

```output
MergeError: Not allowed to merge between different levels. (1 levels on the left, 2 on the right)
```

and

```output
NameError: name 'ctd_ds' is not defined
```

This is a common and useful side effect of turning exploratory code into
functions: **writing a function forces you to be explicit about inputs and
outputs**. Here, the merge fails because only `ctd_stats`'s columns were
flattened to single-level names before merging; `dosta_stats` still has its original 2-level (variable, stat) columns, so pandas refuses to align them. The second error is a plain typo (`ctd_ds` instead of `ds`) that wasn't caught because the notebook was
never run start-to-finish in-order after that line was written.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Build a merge module — and fix the bugs

Write `merge.py` with the following three functions:
1.  A function to flatten a stats table's columns and add a `modeled_flag` column
2.  A function to merge the flattened CTD and DOSTA tables and attach variable attributes (units, long names) from the original datasets
3.  A function to save the result as a netCDF

You will need to fix both bugs from the notebook along the
way. 

:::::::::::::::::::::::: solution

```python
# merge.py
"""Merge CTD + DOSTA burst statistics into a dataset with metadata."""

import pandas as pd
import xarray as xr

VARIABLE_ATTRS = {
    "sea_water_temperature": 
        {"units": "degrees_Celsius", 
         "long_name": "Sea Water Temperature"},
    "sea_water_practical_salinity": 
        {"units": "1", 
         "long_name": "Sea Water Practical Salinity"},
    "sea_water_pressure": 
        {"units": "dbar",
         "long_name": "Sea Water Pressure"},
    "oxygen_concentration_corrected": 
        {"units": "umol kg-1", 
         "long_name": "Corrected Dissolved Oxygen Concentration"},
    "median":
        {"comment": "This value represents the median value of the data collected using a 15-minute burst sampling approach"},
    "mad":
        {"comment": "This value is the median-absolute-deviation of each sampled burst"},
    "modeled":
        {"comment": "This flag indicates wether a value was observed (0) or modeled (1)"}
}


def flag_and_flatten(stats, was_filled, keep_vars):
    """Restrict to `keep_vars`, add a modeled_flag per variable, and flatten
    the 2-level (variable, stat) columns into single flat names."""
    stats = stats.loc[:, keep_vars].copy()
    for var in keep_vars:
        stats[(var, "modeled_flag")] = was_filled[var].astype(int)

    stats.columns = ["_".join(col).strip() for col in stats.columns.values]
    return stats


def merge_ctd_dosta(ctd_flat, dosta_flat, ctd, dosta):
    """Outer-merge flattened CTD and DOSTA tables and attach variable attributes."""
    merged = pd.merge(ctd_flat, dosta_flat, left_index=True, right_index=True, how="outer")
    merged.index.name = "time"
    ds = merged.to_xarray()

    for var in ds.data_vars:
        base_name = var.rsplit("_", 1)[0] if var.endswith(("_median", "_mad")) else var
        if base_name in VARIABLE_ATTRS:
            ds[var].attrs.update(VARIABLE_ATTRS[base_name])
        if var.endswith("_median"):
            ds[var].attrs.update(VARIABLE_ATTRS['median'])
        if var.endswith("_mad"):
            ds[var].attrs.update(VARIABLE_ATTRS['mad'])
        if var.endswith("_modeled"):
            ds[var].attrs.update(VARIABLE_ATTRS['modeled'])

    return ds


def save_merged_dataset(ds, path):
    """Write a merged dataset to netCDF, with a couple of dataset-level attrs."""
    ds.attrs.setdefault("source", "OOI GS01SUMO near-surface instrument frame (CTD + DOSTA)")
    ds.attrs.setdefault("processing", "15-minute burst median/MAD; gaps filled with linear trend + harmonic fit")
    ds.to_netcdf(path)
```

Note that **both** CTD and DOSTA go through `flag_and_flatten` now, which is
what the original notebook was missing:

```python
ctd_flat = flag_and_flatten(ctd_stats, was_filled_ctd,
                             ["sea_water_temperature", "sea_water_practical_salinity", "sea_water_pressure"])
dosta_flat = flag_and_flatten(dosta_stats, was_filled_dosta,
                               ["oxygen_concentration_corrected"])
merged_ds = merge_ctd_dosta(ctd_flat, dosta_flat)
save_merged_dataset(merged_ds, "gs01sumo_merged.nc")
```

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: instructor

This challenge is where the workshop's core message lands hardest: modules
aren't just tidiness, they change what bugs you can even see. As long as
`ctd_stats`/`dosta_stats` were just names in one long notebook, "did I
flatten both of these the same way?" was invisible. As soon as
`flag_and_flatten` exists as one function called twice, the question
answers itself by construction. Worth saying this out loud rather than
letting it pass as just another challenge.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Turning modules into a package

Two or three loose `.py` files next to a notebook works for now, but as
soon as you want to `pip install` this, or import it from a notebook in a
different folder, you need a **package**: a directory with an
`__init__.py` file.

```text
mooring_tools/
├── __init__.py
├── stats.py
├── plotting.py
└── merge.py
```

`__init__.py` can be empty; its presence is what tells Python
`mooring_tools` is an importable package, and modules inside it are
addressed as `mooring_tools.stats`, `mooring_tools.plotting`,
`mooring_tools.merge`:

```python
from mooring_tools.stats import resample_burst_stats, fill_harmonic_gaps
from mooring_tools.plotting import plot_raw_timeseries, plot_burst_stats
from mooring_tools.merge import flag_and_flatten, merge_ctd_dosta, save_merged_dataset
```

::::::::::::::::::::::::::::::::::::: callout

## Module vs. package

A **module** is a single `.py` file. A **package** is a directory of
modules with an `__init__.py`. `stats.py` is a module; `mooring_tools/`
(once it has an `__init__.py`) is a package containing three modules.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 4: Notebook to package

Turn `stats.py`, `plotting.py`, and `merge.py` into a `mooring_tools/`
package (add the `__init__.py`), and update `messy_analysis.ipynb`'s import
cell to pull from it instead. 

::::::::::::::::::::::::::::::::::::::::::::::::

## Wrap-up

By the end of this section, you should have a `mooring_tools/` package
with three modules, `stats`, `plotting`, `merge`, and a notebook that
imports from it with `autoreload` active. This package is what the next section
will turn into a repository with a managed environment, READMEs, and setup files.

::::::::::::::::::::::::::::::::::::: keypoints

- A module is a single `.py` file; a package is a directory of modules with an `__init__.py`
- `%load_ext autoreload` + `%autoreload 2` lets a notebook pick up edits to your own modules without a kernel restart
- Python checks your notebook's own directory before the standard library, such that a module named `random.py` or `csv.py` can silently break unrelated imports elsewhere in your code
- Not everything needs a module. Modularize logic that's substantial or repeated

::::::::::::::::::::::::::::::::::::::::::::::::
