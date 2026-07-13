# Workshop starter files

- `messy_analysis.py` — run from this directory (`python3 messy_analysis.py`).
  Reads `data/ooi_mooring_sample.csv` and prints summary statistics for
  temperature, salinity, and dissolved oxygen.
- `data/ooi_mooring_sample.csv` — 72 hours of synthetic mooring data
  (hourly), loosely modeled on OOI Coastal Endurance surface mooring
  CTD/DOSTA output. Values are synthetic, not real OOI observations, and
  include realistic missing-data gaps (blank cells) to mimic telemetry
  dropouts.

## A note for instructors

`messy_analysis.py` contains one intentional, non-crashing bug: the outlier
check at the bottom reuses the `std` variable left over from the dissolved
oxygen block instead of recomputing it for temperature. It won't raise an
error and won't flag any (real) outliers in this dataset, so it's easy to
miss — which is exactly the point. It's a good moment in Block 1 or Block 2
to make explicit: copy-pasted blocks that share variable names are a common,
quiet source of bugs, and one more reason to extract a function instead.
