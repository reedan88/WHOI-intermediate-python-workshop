# Workshop starter files

- `messy_analysis.ipynb` — open in Jupyter and run top to bottom. Loads
  `data/gs01sumo_nsif_ctd.nc` and `data/gs01sumo_nsif_dosta.nc`, does some
  exploratory plotting, computes 15-minute burst-median statistics, and
  gap-fills them. The last two cells ("Merge and save") are **deliberately
  broken** — a real `MergeError` and a real `NameError` — for Block 2's
  merge-module challenge.
- `data/gs01sumo_nsif_ctd.nc`, `data/gs01sumo_nsif_dosta.nc` — real
  [OOI](https://oceanobservatories.org/) data from the **GS01SUMO** mooring
  (Global Irminger Sea Array, surface mooring, near-surface instrument
  frame), trimmed to one week (2020-09-01 to 2020-09-08) and to just the
  variables this workshop uses, so the files stay small (~2 MB total)
  while still being real, burst-sampled instrument data with genuine gaps.

**Dependencies:** `xarray`, `netCDF4`, `pandas`, `numpy`, `matplotlib`.
Block 3 covers setting these up properly in a virtual environment with a
pinned dependency file — for now, `pip install xarray netCDF4 pandas numpy
matplotlib` is enough to follow along. `jupyter` (or JupyterLab) is assumed
throughout — this workshop is written for a notebook-first audience, not a
script/IDE workflow.

## A note for instructors

The full-resolution GS01SUMO deployment record for these two instruments
runs about a year (Aug 2020–Aug 2021) and is well over 300 MB combined —
too large to hand out for a workshop. The `data/` files here are a
one-week subset (matching the window the original exploratory notebook
itself zooms into), with only the scientifically relevant variables kept
(the full OOI files also carry extensive QARTOD/QC bookkeeping columns,
which are out of scope for this workshop). If you want the full dataset for
your own reference, it's available via the
[OOI Data Portal](https://dataexplorer.oceanobservatories.org/) or the
`ooinet` Python package used in the original source notebook this workshop
is adapted from.

`fill_harmonic_gaps` in `messy_analysis.ipynb` is left as a clean,
documented function on purpose — it's the "already good" example learners
compare their own docstring against in Block 1, rather than something they
need to refactor themselves.

The "Merge and save" section at the end is copied faithfully from the
unfinished state of the real source notebook, including its two actual
bugs (an un-flattened DOSTA table causing a `MergeError` on merge, and a
`ctd_ds`/`ds` typo). These aren't staged — they're what happens when you
try to run exploratory analysis code start-to-finish, which is exactly the
point of Block 2's merge-module challenge: writing `flag_and_flatten` as a
function that's called identically for both instruments makes the missing
step impossible to skip, whereas it was easy to miss in a long notebook.
