---
title: "Writing Effective Functions"
teaching: 80
exercises: 40
---

:::::::::::::::::::::::::::::::::::::: questions

- When should I turn a block of code into a function?
- How do I design a function so someone else (or future-me) can use it correctly?
- What belongs in a docstring, and why write one at all?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Identify repeated or reusable logic that should be extracted into a function
- Write functions with clear positional arguments, defaults, and `*args`/`**kwargs`
- Add type hints to a function signature
- Write a docstring that documents a function's purpose, arguments, and return value

::::::::::::::::::::::::::::::::::::::::::::::::

## Why write functions?

Open `messy_analysis.ipynb` from the setup materials. It loads a full-year of
data from the [OOI](https://oceanobservatories.org/) **GI01SUMO** (**G**lobal **I**rminger Sea Array **Su**rface **Mo**oring) **NSIF** (**N**ear-**S**urface **I**nstrument **F**rame) and computes 15-minute burst-median statistics for the CTD (temperature, salinity) and the DOSTA (dissolved oxygen). It calculates the *same*
statistics for both instruments, with a six-line block copy-pasted and
lightly edited between them.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Spot the repetition

Skim `messy_analysis.ipynb`. Without changing any code yet, identify (you can write a
comment at the top of the file) which blocks of code are doing "the same
thing" to different data.

:::::::::::::::::::::::: solution

The CTD block and the DOSTA block: both convert an xarray `Dataset` to a
dataframe, resample it to 15-minute bins, compute the median and the median
absolute deviation (MAD) per bin, and reassemble the two into one table.
Only the input dataset changes between them.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

A good rule of thumb: **if you've written the same logic twice, it should be
a function.** As you add instruments or expand your analysis, a bug fix means finding and fixing it in every copy. Functions turn that into one place.

## Function anatomy

We'll live-code the extraction together, pulling the burst-statistics logic
out of the CTD block:

```python
def resample_burst_stats(df, freq="900s"):
    resampler = df.resample(freq, origin="start_day", offset=pd.Timedelta("3150s"))
    median = resampler.median()

    group_median = resampler.transform("median")
    deviations = (df - group_median).abs()
    mad = deviations.resample(freq, origin="start_day", offset=pd.Timedelta("3150s")).median()

    stats = pd.concat([median, mad], axis=1, keys=["median", "mad"]).swaplevel(axis=1).sort_index(axis=1)
    stats.index = stats.index + pd.Timedelta(freq) / 2
    return stats
```

Key parts to narrate as you write:

- **Positional arguments** (`df`) vs. **keyword arguments with defaults**
  (`freq="900s"`): the burst interval defines the length of time between the
  start of collection intervals. It may change between instruments (but not here)
- The **return value**: the original script only ever printed or plotted
  `ctd_stats`/`dosta_stats`; returning it is what lets the same function
  produce *both*
- `*args`/`**kwargs` would come in if, say, this needed to pass extra
  options through to `.resample()` without the function knowing about all
  of them in advance.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Extract a function

Working from `messy_analysis.ipynb`, extract the repeated resampling block into
`resample_burst_stats` and call it twice: once for the CTD dataframe, once
for the DOSTA dataframe.

:::::::::::::::::::::::: solution

```python
def resample_burst_stats(df, freq="900s"):
    resampler = df.resample(freq, origin="start_day", offset=pd.Timedelta("3150s"))
    median = resampler.median()

    group_median = resampler.transform("median")
    deviations = (df - group_median).abs()
    mad = deviations.resample(freq, origin="start_day", offset=pd.Timedelta("3150s")).median()

    stats = pd.concat([median, mad], axis=1, keys=["median", "mad"]).swaplevel(axis=1).sort_index(axis=1)
    stats.index = stats.index + pd.Timedelta(freq) / 2
    return stats

ctd_stats = resample_burst_stats(ctd_df)
dosta_stats = resample_burst_stats(dosta_df)
```

::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## Single responsibility

`resample_burst_stats` computes statistics. It doesn't load data and it
doesn't plot. The original notebook's cells did all three in sequence,
which is fine for exploring, but bundling them together is exactly what
would stop this function from being reused and limits its flexibility. 
We'll revisit this when we split code into modules in the next block.

::::::::::::::::::::::::::::::::::::::::::::::::

## Type hints

Type hints don't change how Python runs your code. Rather, they're documentation
that your editor and static-analysis tools can check for you.

```python
def resample_burst_stats(df: pd.DataFrame, freq: str = "900s") -> pd.DataFrame:
    ...
```

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Add type hints

Add type hints to `resample_burst_stats`. What type should the return value be?

:::::::::::::::::::::::: solution

```python
def resample_burst_stats(df: pd.DataFrame, freq: str = "900s") -> pd.DataFrame:
    resampler = df.resample(freq, origin="start_day", offset=pd.Timedelta("3150s"))
    median = resampler.median()

    group_median = resampler.transform("median")
    deviations = (df - group_median).abs()
    mad = deviations.resample(freq, origin="start_day", offset=pd.Timedelta("3150s")).median()

    stats = pd.concat([median, mad], axis=1, keys=["median", "mad"]).swaplevel(axis=1).sort_index(axis=1)
    stats.index = stats.index + pd.Timedelta(freq) / 2
    return stats
```

The return type is `pd.DataFrame` because both `median` and the final `stats`
table are dataframes, and `stats` is what gets returned.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Docstrings

A docstring is the first statement inside a function, written as a triple-quoted
string. It's what shows up when someone runs `help(resample_burst_stats)`.
`messy_analysis.ipynb` already has one good example to look at:
`fill_harmonic_gaps`, which fills gaps in the burst-median series using a
linear-trend-plus-harmonic fit. It's already written as a clean, documented
function. Use it as a reference example.

```python
def resample_burst_stats(df: pd.DataFrame, freq: str = "900s") -> pd.DataFrame:
    """Compute burst-median statistics for OOI instrument data.

    OOI instruments often sample in short bursts; this
    collapses each burst into a robust summary statistic.

    Parameters
    ----------
    df : pandas.DataFrame
        Time-indexed instrument data, one column per variable, at full sampling resolution.
    freq : str, default "900s"
        Burst interval as a pandas offset string.

    Returns
    -------
    pandas.DataFrame
        Columns are a 2-level MultiIndex (variable, statistic), where
        statistic is one of "median" or "mad" (median absolute deviation).
        Index is the start time of each burst.
    """
    ...
```

We're using the NumPy docstring style here since it's common in scientific
Python, but the important content is the same regardless of style: what the
function does, what each argument means, and what comes back.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 4: Document your function

Add a docstring to `resample_burst_stats`. Then, in a notebook cell, run
`help(resample_burst_stats)` and confirm it displays what you expect.
Compare it to `fill_harmonic_gaps`'s docstring already in the file.

::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: instructor

It's worth pointing out here that we'll rely on these docstrings again in Block 4 when
generating project documentation, and thus the investment pays off later in the
workshop, not just in some hypothetical future project. `fill_harmonic_gaps`
is deliberately left already-documented in the starter file so learners have
a working example to model their own docstring on, rather than writing one
from a blank page.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Wrap-up

By the end of this block, learners should have `resample_burst_stats`
extracted, type-hinted, and documented, alongside the already-clean
`fill_harmonic_gaps`. These two functions are what Block 2 organizes into a module.

::::::::::::::::::::::::::::::::::::: keypoints

- Extract a function when you find yourself repeating logic, not just to look tidy
- Prefer returning values over printing them, so functions can be composed
- Type hints document expected input/output types for editors and readers
- A docstring documents purpose, parameters, and return value. Its often best to write it as part of writing the function, not as an afterthought

::::::::::::::::::::::::::::::::::::::::::::::::
