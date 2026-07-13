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

Open `messy_analysis.py` from the setup materials. It reads three days of
hourly CTD/DOSTA readings from an ocean mooring (temperature, salinity, and
dissolved oxygen — modeled on the kind of data an
[OOI](https://oceanobservatories.org/) Coastal Endurance surface mooring
would report) and calculates summary statistics for each variable, one block
at a time, with the same six lines of code copy-pasted and lightly edited
each time.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Spot the repetition

Skim `messy_analysis.py`. Without changing any code yet, write down (in a
comment at the top of the file) which blocks of code are doing "the same
thing" to different data.

:::::::::::::::::::::::: solution

The temperature, salinity, and dissolved oxygen blocks: each drops missing
readings (recorded as blank cells from telemetry dropouts), computes
mean/std/min/max, and prints a formatted summary. Only the input list and a
label string change between them.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

A good rule of thumb: **if you've written the same logic twice, it should be
a function.** By the third copy-paste, a bug fix means finding and fixing it
in three places — functions turn that into one place.

## Function anatomy

We'll live-code the extraction together:

```python
def summarize_readings(values, label="temperature_c"):
    cleaned = [v for v in values if v is not None]
    mean = sum(cleaned) / len(cleaned)
    print(f"{label}: mean={mean:.2f}, n={len(cleaned)}")
    return mean
```

Key parts to narrate as you write:

- **Positional arguments** (`values`) vs. **keyword arguments with defaults**
  (`label="temperature_c"`)
- The **return value** — a function that only `print`s is hard to reuse in
  another function; returning the result is what makes it composable
- `*args` and `**kwargs` for the rare case where a function needs to accept a
  variable number of arguments (e.g. a wrapper that logs, then calls another
  function with whatever arguments it was given)

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Extract a function

Working from `messy_analysis.py`, extract the repeated block into a function
called `summarize_readings` and call it three times, once per variable
(temperature, salinity, dissolved oxygen).

:::::::::::::::::::::::: solution

```python
def summarize_readings(values, label="temperature_c"):
    cleaned = [v for v in values if v is not None]
    mean = sum(cleaned) / len(cleaned)
    print(f"{label}: mean={mean:.2f}, n={len(cleaned)}")
    return mean

summarize_readings(temperature_readings, label="temperature_c")
summarize_readings(salinity_readings, label="salinity_psu")
summarize_readings(do_readings, label="dissolved_oxygen_umol_kg")
```

::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## Single responsibility

A function that cleans data, computes statistics, *and* prints formatted
output is doing three jobs. That's fine for a quick script, but as functions
get reused, each responsibility you bundle together is one more reason the
function can't be reused somewhere that only needs one of those things.
We'll revisit this idea when we split code into modules in the next block.

::::::::::::::::::::::::::::::::::::::::::::::::

## Type hints

Type hints don't change how Python runs your code — they're documentation
that your editor and static-analysis tools can check for you.

```python
def summarize_readings(values: list[float], label: str = "sensor") -> float:
    ...
```

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Add type hints

Add type hints to the `summarize_readings` function you wrote in Challenge 2.
What type should the return value be?

:::::::::::::::::::::::: solution

```python
def summarize_readings(values: list[float], label: str = "sensor") -> float:
    cleaned = [v for v in values if v is not None]
    mean = sum(cleaned) / len(cleaned)
    print(f"{label}: mean={mean:.2f}, n={len(cleaned)}")
    return mean
```

The return type is `float`, since `mean` is the value being returned.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Docstrings

A docstring is the first statement inside a function, written as a triple-quoted
string. It's what shows up when someone runs `help(summarize_readings)`.

```python
def summarize_readings(values: list[float], label: str = "sensor") -> float:
    """Compute and print the mean of a list of sensor readings.

    Parameters
    ----------
    values : list[float]
        Raw sensor readings; ``None`` entries are dropped before computing.
    label : str, default "sensor"
        Name used in the printed summary line.

    Returns
    -------
    float
        The mean of the non-missing values.
    """
    ...
```

We're using the NumPy docstring style here since it's common in scientific
Python, but the important content is the same regardless of style: what the
function does, what each argument means, and what comes back.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 4: Document your function

Add a docstring to `summarize_readings`. Then, in a Python shell, run
`help(summarize_readings)` and confirm it displays what you expect.

::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: instructor

Some learners will want to skip docstrings as "extra work." It's worth
pointing out here that we'll rely on these docstrings again in Block 4 when
generating project documentation — the investment pays off later in the
workshop, not just in some hypothetical future project.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Wrap-up

By the end of this block, learners should have a small set of clean,
type-hinted, documented functions extracted from `messy_analysis.py`. This
file is what Block 2 organizes into a module — don't let learners discard it.

::::::::::::::::::::::::::::::::::::: keypoints

- Extract a function when you find yourself repeating logic, not just to look tidy
- Prefer returning values over printing them, so functions can be composed
- Type hints document expected input/output types for editors and readers
- A docstring documents purpose, parameters, and return value — write it as
  part of writing the function, not as an afterthought

::::::::::::::::::::::::::::::::::::::::::::::::
