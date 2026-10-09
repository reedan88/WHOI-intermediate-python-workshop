# Workshop starter files

- `first_analysis.ipynb`: open in Jupyter and run top to bottom. Loads
  `data/gi01sumo_nsif_ctd.nc` and `data/gi01sumo_nsif_dosta.nc`, does some
  exploratory plotting, computes 15-minute burst-median statistics, and
  gap-fills them. The last couple of cells ("Merge and save") are incomplete, as is often the case with initial data exploration
- `data/gi01sumo_nsif_ctd.nc`, `data/gi01sumo_nsif_dosta.nc`: real
  [OOI](https://oceanobservatories.org/) data from the **GI01SUMO** mooring
  (**G**lobal **I**rminger Sea Array, **Su**rface **Mo**oring) **NSIF** (**N**ear-**S**urface **I**nstrument
  **F**rame) for a single year-long deployment. The datasets have had most of their extraneous parameters removed to cut down on dataset size, but they are still failry hefty files. They contain actual, measured, burst-sampled instrument data with genuine gaps.

**Dependencies:** `xarray`, `netCDF4`, `pandas`, `numpy`, `matplotlib`.
Block 3 covers setting these up properly in a virtual environment with a
pinned dependency file. That said, learners should have the following packages installed: `pip install xarray netCDF4 pandas numpy
matplotlib jupyter`. This workshop is written for a notebook-first audience, not a
script/IDE workflow.

## A note for instructors

`fill_harmonic_gaps` in `first_analysis.ipynb` is left as a clean, documented function to serve as an example for learners to compare their own docstring against in Block 1, rather than something they need to refactor themselves.

The "Merge and Save" part of the notebook is incomplete. The learners should have the skill to write a function for the process. That said, the actual function's guts are less important than having a function that can be turned into a module and then a package, so don't spend too much time on physical coding.
