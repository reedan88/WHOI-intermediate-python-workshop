---
title: "Documentation and Reuse"
teaching: 90
exercises: 50
---

:::::::::::::::::::::::::::::::::::::: questions

- What does a README need to contain to actually be useful?
- How do docstrings work together across a whole project, not just one function?
- How do I extend this package for new work without breaking what already works?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write a README that lets a new user install and run the project
- Audit and complete docstrings and type hints across a small project
- Extend the package to support a new variable without editing existing functions

::::::::::::::::::::::::::::::::::::::::::::::::

## Writing a README

A README's job is narrow: let someone who isn't you install the project
and run one thing successfully, without opening an issue or emailing you
first. For `mooring_tools`, that means: what it does, how to install it,
one runnable usage example, and where the data comes from.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Draft the README

Write `README.md` for `gs01sumo-mooring-tools`, covering: what the package
does, install instructions (both `pip install -e .` and
`pip install -r requirements.txt`), and a usage example a new user could
actually run against `data/gs01sumo_nsif_ctd.nc`.

:::::::::::::::::::::::: solution

```markdown
# mooring_tools

Burst-statistics, plotting, and merge utilities for OOI GS01SUMO CTD/DOSTA
data (Global Irminger Sea Array, near-surface instrument frame).

## What this does

OOI moorings sample in short bursts (commonly every 15 minutes). This
package takes raw CTD (temperature, salinity, pressure, density) and DOSTA
(dissolved oxygen) records and:

- computes robust burst-median statistics (median + median absolute
  deviation) for each variable
- fills gaps in the burst-median series with a linear-trend + harmonic fit
- plots raw vs. burst-median data, and observed vs. modeled series
- merges CTD and DOSTA into one annotated, saveable netCDF dataset, flagging
  which values are observed vs. gap-filled

## Install

\`\`\`bash
git clone <this-repo-url>
cd gs01sumo-mooring-tools
python3 -m venv .venv
source .venv/bin/activate      # .venv\\Scripts\\activate on Windows
pip install -e .
\`\`\`

For exact reproducibility of a specific analysis, use the pinned
\`requirements.txt\` instead of the loose bounds in \`pyproject.toml\`:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage

\`\`\`python
import xarray as xr
import numpy as np
from mooring_tools.stats import resample_burst_stats

ctd = xr.open_dataset("data/gs01sumo_nsif_ctd.nc")
scalar_vars = [v for v in ctd.data_vars if ctd[v].dims == ("time",) and np.issubdtype(ctd[v].dtype, np.number)]
ctd_stats = resample_burst_stats(ctd[scalar_vars].to_dataframe())
\`\`\`

See \`notebooks/messy_analysis.ipynb\` for a full worked example.

## Data

\`data/\` contains a one-week subset of the real OOI GS01SUMO deployment
record. The full dataset is available via the OOI Data Portal.

## License

MIT — see \`LICENSE\`.
```

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Docstrings at the project level

Block 1 introduced docstrings at the level of a single function, with
`fill_harmonic_gaps` as the model to write toward. Now that there are three
modules, it's worth checking: did that standard actually get applied
everywhere?

Open `merge.py`. Compare its docstrings to `stats.py`'s:

```python
# merge.py, as it stands after Block 2
def flag_and_flatten(stats, was_filled, keep_vars):
    """Restrict to `keep_vars`, add a modeled_flag per variable, and flatten
    the 2-level (variable, stat) columns into single flat names."""
    ...
```

No type hints, no `Parameters`/`Returns` sections, only a one-line summary
only. Meanwhile `stats.py`'s `fill_harmonic_gaps` has both. This wasn't
deliberate inconsistency; it's what naturally happens when a module gets
built in a hurry during a live-coding challenge. This is exactly what a
docstring audit is for.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Docstring and type-hint audit

Go through `plotting.py` and `merge.py` and bring every function up to the
same standard as `stats.py`: type hints on the signature, and a full
NumPy-style docstring (summary, `Parameters`, `Returns`).

:::::::::::::::::::::::: solution

```python
# merge.py, after the audit
import pandas as pd
import xarray as xr

VARIABLE_ATTRS = {
    "sea_water_temperature": {"units": "degrees_Celsius", "long_name": "Sea Water Temperature"},
    "sea_water_practical_salinity": {"units": "1", "long_name": "Sea Water Practical Salinity"},
    "sea_water_pressure": {"units": "dbar", "long_name": "Sea Water Pressure"},
    "sea_water_density": {"units": "kg m-3", "long_name": "Sea Water Density"},
    "oxygen_concentration_corrected": {"units": "umol kg-1", "long_name": "Corrected Dissolved Oxygen Concentration"},
}


def flag_and_flatten(stats: pd.DataFrame, was_filled: pd.DataFrame, keep_vars: list[str]) -> pd.DataFrame:
    """Restrict to `keep_vars`, add a modeled_flag per variable, and flatten
    the 2-level (variable, stat) columns into single flat names.

    Parameters
    ----------
    stats : pandas.DataFrame
        Output of `resample_burst_stats` (2-level column MultiIndex of
        (variable, stat)).
    was_filled : pandas.DataFrame
        Boolean frame, same shape/columns as the "median" slice of `stats`,
        True where that burst was gap-filled rather than observed.
    keep_vars : list[str]
        Which variables (first-level column names) to keep.

    Returns
    -------
    pandas.DataFrame
        Flat columns like "sea_water_temperature_median",
        "sea_water_temperature_mad", "sea_water_temperature_modeled_flag".
    """
    stats = stats.loc[:, keep_vars].copy()
    for var in keep_vars:
        stats[(var, "modeled_flag")] = was_filled[var].astype(int)

    stats.columns = ["_".join(col).strip() for col in stats.columns.values]
    return stats


def merge_ctd_dosta(ctd_flat: pd.DataFrame, dosta_flat: pd.DataFrame) -> xr.Dataset:
    """Outer-merge flattened CTD and DOSTA tables and attach variable attributes.

    Parameters
    ----------
    ctd_flat, dosta_flat : pandas.DataFrame
        Output of `flag_and_flatten` for each instrument. Both must already
        be flattened to single-level columns -- merging one flattened and
        one still-MultiIndex table raises a `MergeError`.

    Returns
    -------
    xarray.Dataset
        Merged on the shared burst-median time index, with `units` and
        `long_name` attached to each data variable listed in
        `VARIABLE_ATTRS`. To support a new variable, add it to
        `VARIABLE_ATTRS` and include it in the `keep_vars` passed to
        `flag_and_flatten` -- no changes needed here.
    """
    merged = pd.merge(ctd_flat, dosta_flat, left_index=True, right_index=True, how="outer")
    merged.index.name = "time"
    ds = merged.to_xarray()

    for var in ds.data_vars:
        base_name = var.rsplit("_", 1)[0] if var.endswith(("_median", "_mad")) else var
        if base_name in VARIABLE_ATTRS:
            ds[var].attrs.update(VARIABLE_ATTRS[base_name])

    return ds


def save_merged_dataset(ds: xr.Dataset, path: str) -> None:
    """Write a merged dataset to netCDF, with a couple of dataset-level attrs.

    Parameters
    ----------
    ds : xarray.Dataset
        Typically the output of `merge_ctd_dosta`.
    path : str
        Output file path.
    """
    ds.attrs.setdefault("source", "OOI GS01SUMO near-surface instrument frame (CTD + DOSTA)")
    ds.attrs.setdefault("processing", "15-minute burst median/MAD; gaps filled with linear trend + harmonic fit")
    ds.to_netcdf(path)
```

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: instructor

Worth naming explicitly: `merge_ctd_dosta`'s docstring now states the
"add a new variable" extension path directly in its `Returns` section.
This is documenting a design property Block 2's callout and this 
block's reuse challenge both rely on. A good
docstring doesn't just describe current behavior; it tells the next
person (including future-you) what's safe to change without reading the
implementation.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Reusing and updating the repo

The real test of a well-organized package is what happens when the
scientific scope changes. Here's a real one: `data/gs01sumo_nsif_ctd.nc`
has always included a fourth CTD variable — `sea_water_density` — from the
original exploratory notebook. `resample_burst_stats` has been computing
burst statistics for it since Block 1, since it works generically over
every numeric column. But `merge.py`'s `keep_vars` lists (in Block 2's
Challenge 3, and `VARIABLE_ATTRS`) never included it, so it's never made it
into the final merged, saved dataset.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Add density support

Add `sea_water_density` as a supported merged-output variable. You should
not need to edit `resample_burst_stats`, `flag_and_flatten`, or
`merge_ctd_dosta` at all.

:::::::::::::::::::::::: solution

```python
from mooring_tools.merge import VARIABLE_ATTRS

VARIABLE_ATTRS["sea_water_density"] = {"units": "kg m-3", "long_name": "Sea Water Density"}

keep_vars = ["sea_water_temperature", "sea_water_practical_salinity",
             "sea_water_pressure", "sea_water_density"]
ctd_flat = flag_and_flatten(ctd_stats, was_filled_ctd, keep_vars)
```

`resample_burst_stats` already computed statistics for every numeric
column in the input dataframe, including density, since it was never
told to look for specific variable names. `flag_and_flatten` and
`merge_ctd_dosta` are equally generic; they only needed `VARIABLE_ATTRS`
extended and a longer `keep_vars` list at the call site. If this
*didn't* work without touching function bodies, that would be a sign the
functions were less generic than Block 2 intended.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Versioning changes

As the package evolves, with new variables, a bug fix in `fill_harmonic_gaps`,
a new plotting function, etc., here are ways to keep that documented:

- **Bump the version** in `pyproject.toml` (`version = "0.1.0"` →
  `"0.2.0"`) when you make a change someone else relying on the package
  would care about.
- **Tag the commit in git** (`git tag v0.2.0`) so "the version I ran this
  analysis with" is always recoverable later, even after further changes.

Neither requires new tooling — both are just a habit of treating the
package as something other people (including future-you) depend on, not
just a folder of scripts.

## Wrap-up

Across all four blocks: a repeated block became a function (Block 1), the
function joined others in a package (Block 2), the package became
installable with a managed environment (Block 3), and now it's documented
well enough, and generic enough, to extend for new scientific questions
without touching working code (Block 4). That last property — extending
without editing — is the actual payoff of everything before it.

::::::::::::::::::::::::::::::::::::: keypoints

- A README's job is to let someone else install and run the project without asking you
- Docstring consistency matters more as a project grows past one file — audit it explicitly rather than assuming it happened
- A well-documented function's docstring tells the reader what's safe to extend, not just what the function currently does
- Reusing a repo well means extending generic functions with new data/config, not copy-pasting or editing working code
- Bumping a version number and tagging the commit is enough to keep "what did I run this with" answerable later

::::::::::::::::::::::::::::::::::::::::::::::::
