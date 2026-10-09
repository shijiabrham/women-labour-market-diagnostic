"""
dataset_1_analytics.py
======================
Reusable analytical layer for Dataset 1.

Source (read-only):
    outputs/phase_4_eda/dataset_1_reusable_analytical.csv

Grain of the source:
    State × Year × Gender × Area_Type × Education
    with indicators: LFPR, WPR, Unemployment_Rate

Public API
----------
load()                  → load (and cache) the reusable layer
filter_data(...)        → apply one or more dimension filters
analyse(...)            → group by selected dimensions, aggregate indicator
compare(...)            → side-by-side comparison of two group values
trend(...)              → year-on-year view with optional YoY delta
year_vs_year(...)       → endpoint comparison (any two years)
change(...)             → absolute and percentage change between two years

All functions return plain pandas DataFrames.
No CSV files are written by this module.
No source files are modified.
"""

from __future__ import annotations
import os
import functools
import pandas as pd
import numpy as np
from typing import Optional, Union

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DIMENSIONS  = ["State", "Year", "Gender", "Area_Type", "Education"]
INDICATORS  = ["LFPR", "WPR", "Unemployment_Rate"]

_DEFAULT_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "outputs", "phase_4_eda", "dataset_1_reusable_analytical.csv",
)

# ---------------------------------------------------------------------------
# Internal cache
# ---------------------------------------------------------------------------
_cache: dict[str, pd.DataFrame] = {}


# ---------------------------------------------------------------------------
# 1. load
# ---------------------------------------------------------------------------
def load(path: str = _DEFAULT_CSV) -> pd.DataFrame:
    """
    Load the reusable analytical layer from CSV.
    Cached after the first call. Source file is never modified.
    """
    if path not in _cache:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Reusable analytical layer not found at: {path}")
        df = pd.read_csv(path)
        # Ensure Year is integer
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
        _cache[path] = df
    return _cache[path].copy()


# ---------------------------------------------------------------------------
# 2. filter_data
# ---------------------------------------------------------------------------
def filter_data(
    df: pd.DataFrame,
    *,
    state:     Optional[Union[str, list]] = None,
    year:      Optional[Union[int, list]] = None,
    gender:    Optional[Union[str, list]] = None,
    area_type: Optional[Union[str, list]] = None,
    education: Optional[Union[str, list]] = None,
) -> pd.DataFrame:
    """
    Apply one or more equality filters on dimension columns.

    Parameters
    ----------
    df        : DataFrame from load() or a previous filter/analyse call.
    state     : one value or list of values for the State column.
    year      : one value or list of values for the Year column.
    gender    : one value or list of values for the Gender column.
    area_type : one value or list of values for the Area_Type column.
    education : one value or list of values for the Education column.

    Returns
    -------
    Filtered DataFrame (copy; original unchanged).
    """
    out = df.copy()
    mapping = {
        "State":     state,
        "Year":      year,
        "Gender":    gender,
        "Area_Type": area_type,
        "Education": education,
    }
    for col, val in mapping.items():
        if val is None:
            continue
        vals = [val] if isinstance(val, (str, int, float)) else list(val)
        out = out[out[col].isin(vals)]
    return out.reset_index(drop=True)


# ---------------------------------------------------------------------------
# 3. analyse
# ---------------------------------------------------------------------------
def analyse(
    df: pd.DataFrame,
    indicators: Union[str, list],
    dimensions: Union[str, list],
    *,
    round_to: int = 3,
) -> pd.DataFrame:
    """
    Group df by one or more dimensions and aggregate indicators with the
    unweighted arithmetic mean (NaN-aware; zeros are valid observations).

    Parameters
    ----------
    df         : Source DataFrame (typically filtered first).
    indicators : One indicator name or list. Any subset of LFPR, WPR,
                 Unemployment_Rate.
    dimensions : One dimension name or list. Any subset of the five dimensions.
    round_to   : Decimal places to round indicator values (default 3).

    Returns
    -------
    DataFrame with selected dimensions as columns plus aggregated indicators.
    """
    inds = [indicators] if isinstance(indicators, str) else list(indicators)
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)

    # Validate
    bad_ind = [i for i in inds if i not in INDICATORS]
    bad_dim = [d for d in dims if d not in DIMENSIONS]
    if bad_ind:
        raise ValueError(f"Unknown indicator(s): {bad_ind}. Choose from {INDICATORS}.")
    if bad_dim:
        raise ValueError(f"Unknown dimension(s): {bad_dim}. Choose from {DIMENSIONS}.")

    available_inds = [i for i in inds if i in df.columns]
    agg_dict = {ind: "mean" for ind in available_inds}
    result = (
        df.groupby(dims, as_index=False, observed=True, dropna=False)
          .agg(agg_dict)
    )
    for ind in available_inds:
        result[ind] = result[ind].round(round_to)
    return result.sort_values(dims).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 4. compare
# ---------------------------------------------------------------------------
def compare(
    df: pd.DataFrame,
    indicator: str,
    compare_col: str,
    group_a: str,
    group_b: str,
    dimensions: Union[str, list],
    *,
    gap_label: Optional[str] = None,
    round_to: int = 3,
) -> pd.DataFrame:
    """
    Side-by-side comparison of two group values for one indicator,
    pivoted into wide format with a derived gap column.

    Parameters
    ----------
    df          : Source DataFrame.
    indicator   : One indicator, e.g. 'LFPR'.
    compare_col : Dimension used to define the two groups, e.g. 'Gender'.
    group_a     : First group value, e.g. 'Female'.
    group_b     : Second group value, e.g. 'Male'.
    dimensions  : Dimension(s) to retain in the output (besides compare_col).
    gap_label   : Name for the gap column. Defaults to '{group_a}−{group_b}'.
    round_to    : Decimal places.

    Returns
    -------
    Wide DataFrame: dimensions + {indicator}_{group_a} + {indicator}_{group_b}
                    + gap column = group_a value − group_b value.
    """
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)
    all_dims = dims + [compare_col]

    sub = filter_data(df, **{compare_col.lower().replace(" ", "_").replace("+", ""): [group_a, group_b]})
    # Use filter_data kwarg mapping
    col_kwarg = {
        "State":     "state",
        "Year":      "year",
        "Gender":    "gender",
        "Area_Type": "area_type",
        "Education": "education",
    }
    kwarg = col_kwarg[compare_col]
    sub = filter_data(df, **{kwarg: [group_a, group_b]})

    agg = analyse(sub, indicator, all_dims, round_to=round_to)

    pivoted = agg.pivot_table(
        index=dims, columns=compare_col, values=indicator, aggfunc="first"
    ).reset_index()
    pivoted.columns.name = None

    col_a = f"{indicator}_{group_a}"
    col_b = f"{indicator}_{group_b}"
    if group_a in pivoted.columns:
        pivoted.rename(columns={group_a: col_a}, inplace=True)
    if group_b in pivoted.columns:
        pivoted.rename(columns={group_b: col_b}, inplace=True)

    gap = gap_label or f"{group_a}−{group_b}_Gap"
    if col_a in pivoted.columns and col_b in pivoted.columns:
        pivoted[gap] = (pivoted[col_a] - pivoted[col_b]).round(round_to)

    return pivoted.sort_values(dims).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 5. trend
# ---------------------------------------------------------------------------
def trend(
    df: pd.DataFrame,
    indicator: str,
    dimensions: Union[str, list],
    *,
    yoy: bool = False,
    round_to: int = 3,
) -> pd.DataFrame:
    """
    Time-series view; Year must be one of the dimensions.

    Parameters
    ----------
    df         : Source DataFrame (pre-filtered as needed).
    indicator  : One indicator.
    dimensions : Must include 'Year'. May include other dimensions.
    yoy        : If True, add a YoY_Change column (value − previous year value).
    round_to   : Decimal places.

    Returns
    -------
    DataFrame sorted by dimensions with optional YoY_Change column.
    """
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)
    if "Year" not in dims:
        raise ValueError("trend() requires 'Year' to be in dimensions.")

    result = analyse(df, indicator, dims, round_to=round_to)
    result = result.sort_values(dims).reset_index(drop=True)

    if yoy:
        key_dims = [d for d in dims if d != "Year"]
        if key_dims:
            result["YoY_Change"] = (
                result.groupby(key_dims, observed=True)[indicator]
                      .diff()
                      .round(round_to)
            )
        else:
            result["YoY_Change"] = result[indicator].diff().round(round_to)

    return result


# ---------------------------------------------------------------------------
# 6. year_vs_year
# ---------------------------------------------------------------------------
def year_vs_year(
    df: pd.DataFrame,
    indicator: str,
    year_a: int,
    year_b: int,
    dimensions: Union[str, list],
    *,
    round_to: int = 3,
) -> pd.DataFrame:
    """
    Pivot two years side by side with absolute and percentage change.

    Parameters
    ----------
    df         : Source DataFrame (pre-filtered as needed).
    indicator  : One indicator.
    year_a     : First year (baseline).
    year_b     : Second year (comparison).
    dimensions : Grouping dimension(s) BESIDES Year.
    round_to   : Decimal places.

    Returns
    -------
    Wide DataFrame with:
        dimensions + {indicator}_{year_a} + {indicator}_{year_b}
        + Absolute_Change + Percentage_Change
    """
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)

    sub = filter_data(df, year=[year_a, year_b])
    agg = analyse(sub, indicator, dims + ["Year"], round_to=round_to)

    pivoted = agg.pivot_table(
        index=dims, columns="Year", values=indicator, aggfunc="first"
    ).reset_index()
    pivoted.columns.name = None

    col_a = f"{indicator}_{year_a}"
    col_b = f"{indicator}_{year_b}"
    if year_a in pivoted.columns:
        pivoted.rename(columns={year_a: col_a}, inplace=True)
    if year_b in pivoted.columns:
        pivoted.rename(columns={year_b: col_b}, inplace=True)

    if col_a in pivoted.columns and col_b in pivoted.columns:
        pivoted["Absolute_Change"] = (pivoted[col_b] - pivoted[col_a]).round(round_to)
        pivoted["Percentage_Change"] = np.where(
            pivoted[col_a].notna() & (pivoted[col_a] != 0),
            ((pivoted["Absolute_Change"] / pivoted[col_a]) * 100).round(round_to),
            np.nan,
        )

    return pivoted.sort_values(dims).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 7. change
# ---------------------------------------------------------------------------
def change(
    df: pd.DataFrame,
    indicator: str,
    from_year: int,
    to_year: int,
    dimensions: Union[str, list],
    *,
    round_to: int = 3,
) -> pd.DataFrame:
    """
    Convenience wrapper around year_vs_year for absolute + pct change.
    Returns the same output as year_vs_year(from_year, to_year).
    """
    return year_vs_year(df, indicator, from_year, to_year, dimensions, round_to=round_to)
