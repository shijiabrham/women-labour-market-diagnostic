"""
dataset_2_analytics.py
=======================
Reusable analytical engine for Dataset 2.

Architecture rule
-----------------
Reads ONLY:
    outputs/phase_4_eda/dataset_2_reusable_analytical.csv

Columns available:
    State, Year (int), Gender, Area_Type,
    Industry_Division_Type, Enterprise_Type, Percentage_Engaged

All analytical operations (filtering, grouping, aggregation, comparison,
trend, change) are performed dynamically from this single source.

No Q-specific datasets are created or written.

Aggregation note
----------------
When dimensions are collapsed, the engine uses an UNWEIGHTED ARITHMETIC MEAN
of Percentage_Engaged. This is labelled explicitly in every result.

Structural missingness
-----------------------
NaN values arising from structural source absence (e.g. Industry Division Type
`(014, 016, 017, 02-99)` absent from 2022 and 2023) are PRESERVED as NaN.
They are NEVER converted to zero or estimated.

Aggregation interpretation warning
------------------------------------
When a caller aggregates across Enterprise_Type without filtering it,
Percentage_Engaged values across all 8 enterprise categories sum to
approximately 100% per combination. Collapsing (mean across enterprise types)
therefore always produces ~12.5% (= 100 / 8). The engine flags this
explicitly via AGGREGATION_WARNING so the caller is not misled into treating
the result as a substantive industry or area employment share.
"""

from __future__ import annotations
import os
import functools
from typing import Optional, Union, List

import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_CSV = os.path.join(
    _BASE, "outputs", "phase_4_eda", "dataset_2_reusable_analytical.csv"
)

MEASURE = "Percentage_Engaged"
ALL_DIMS = ["State", "Year", "Gender", "Area_Type",
            "Industry_Division_Type", "Enterprise_Type"]

# Conditions that trigger the aggregation interpretation warning
_ENT_SUMMING_DIMS = {"Enterprise_Type"}

AGGREGATION_WARNING = (
    "AGGREGATION INTERPRETATION WARNING: The result was produced by collapsing "
    "across Enterprise_Type without filtering it. Because Percentage_Engaged "
    "values across the 8 enterprise categories sum to ~100% per source combination, "
    "the unweighted mean across all enterprise types converges to ~12.5% "
    "(= 100 / 8). This value does not represent a substantive employment share "
    "for the selected dimension — it is a mathematical artefact of the "
    "enterprise-share structure. Use Enterprise_Type-level results for "
    "substantive analysis."
)

STRUCTURAL_ABSENCE_LABEL = "STRUCTURAL ABSENCE"


# ── 1. Load (cached) ──────────────────────────────────────────────────────────
@functools.lru_cache(maxsize=1)
def load(path: str = _DEFAULT_CSV) -> pd.DataFrame:
    """Load the reusable Dataset 2 analytical CSV. Result is cached."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Reusable analytical CSV not found: {path}")
    df = pd.read_csv(path)
    df["Year"] = df["Year"].astype(int)
    return df


# ── 2. Filter ─────────────────────────────────────────────────────────────────
def filter_data(
    df: pd.DataFrame,
    *,
    state: Optional[Union[str, List[str]]] = None,
    year: Optional[Union[int, List[int]]] = None,
    gender: Optional[Union[str, List[str]]] = None,
    area_type: Optional[Union[str, List[str]]] = None,
    industry: Optional[Union[str, List[str]]] = None,
    enterprise: Optional[Union[str, List[str]]] = None,
) -> pd.DataFrame:
    """
    Filter the DataFrame by any combination of dimension values.

    Parameters accept either a single value (str/int) or a list.
    None means 'no filter applied for that dimension'.
    """
    mask = pd.Series(True, index=df.index)
    if state is not None:
        vals = [state] if isinstance(state, str) else list(state)
        mask &= df["State"].isin(vals)
    if year is not None:
        vals = [year] if isinstance(year, int) else [int(y) for y in year]
        mask &= df["Year"].isin(vals)
    if gender is not None:
        vals = [gender] if isinstance(gender, str) else list(gender)
        mask &= df["Gender"].isin(vals)
    if area_type is not None:
        vals = [area_type] if isinstance(area_type, str) else list(area_type)
        mask &= df["Area_Type"].isin(vals)
    if industry is not None:
        vals = [industry] if isinstance(industry, str) else list(industry)
        mask &= df["Industry_Division_Type"].isin(vals)
    if enterprise is not None:
        vals = [enterprise] if isinstance(enterprise, str) else list(enterprise)
        mask &= df["Enterprise_Type"].isin(vals)
    return df[mask].copy()


def _should_warn(group_dims: List[str], filtered_df: pd.DataFrame) -> bool:
    """Return True if Enterprise_Type is being collapsed without explicit filtering."""
    # Warn when Enterprise_Type is not in group_dims and has more than one unique value
    if "Enterprise_Type" in group_dims:
        return False
    if filtered_df["Enterprise_Type"].nunique() > 1:
        return True
    return False


# ── 3. Analyse — group and aggregate ─────────────────────────────────────────
def analyse(
    df: pd.DataFrame,
    dimensions: Union[str, List[str]],
    *,
    include_count: bool = True,
    round_to: int = 3,
) -> dict:
    """
    Group by `dimensions` and compute unweighted mean of Percentage_Engaged.

    Returns
    -------
    {
        "result":               pd.DataFrame,
        "aggregation_note":     str,
        "aggregation_warning":  str | None,
        "dimensions":           list[str],
        "measure":              "Percentage_Engaged",
    }
    """
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)
    warn = _should_warn(dims, df)

    agg_dict = {MEASURE: "mean"}
    if include_count:
        agg_dict["Observations"] = (MEASURE, "count")
    result = (
        df.groupby(dims, observed=True)
        .agg(**{MEASURE: (MEASURE, "mean"),
                **({"Observations": (MEASURE, "count")} if include_count else {})})
        .round(round_to)
        .reset_index()
    )
    return {
        "result": result,
        "aggregation_note": "Unweighted arithmetic mean of Percentage_Engaged",
        "aggregation_warning": AGGREGATION_WARNING if warn else None,
        "dimensions": dims,
        "measure": MEASURE,
    }


# ── 4. Pivot — wide format ────────────────────────────────────────────────────
def pivot(
    df: pd.DataFrame,
    index: Union[str, List[str]],
    columns: str,
    *,
    round_to: int = 3,
) -> dict:
    """
    Produce a pivot table: mean Percentage_Engaged with `index` as rows
    and `columns` as columns. Structural NaN is preserved.
    """
    all_dims = ([index] if isinstance(index, str) else list(index)) + [columns]
    warn = _should_warn(all_dims, df)

    result = (
        df.groupby(all_dims, observed=True)[MEASURE]
        .mean()
        .round(round_to)
        .unstack(columns)
    )
    return {
        "result": result,
        "aggregation_note": "Unweighted arithmetic mean of Percentage_Engaged",
        "aggregation_warning": AGGREGATION_WARNING if warn else None,
        "index": index,
        "pivot_column": columns,
        "measure": MEASURE,
        "structural_absence_note": (
            "NaN in the result represents structural source absence — "
            "the source contains no observations for that combination. "
            "NaN is NOT zero."
        ),
    }


# ── 5. Compare — gap between two groups ──────────────────────────────────────
def compare(
    df: pd.DataFrame,
    compare_col: str,
    group_a: str,
    group_b: str,
    dimensions: Union[str, List[str]],
    *,
    gap_label: Optional[str] = None,
    round_to: int = 3,
    exclude_other_values: bool = True,
) -> dict:
    """
    Compare group_a vs group_b on compare_col across `dimensions`.

    group_a and group_b values are filtered; all other values of compare_col
    are excluded when exclude_other_values=True.

    Returns wide DataFrame with columns:
        dimensions... | {group_a} | {group_b} | gap_label
    """
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)
    if exclude_other_values:
        df = df[df[compare_col].isin([group_a, group_b])].copy()

    wide = (
        df.groupby(dims + [compare_col], observed=True)[MEASURE]
        .mean()
        .round(round_to)
        .unstack(compare_col)
        .reset_index()
    )
    glabel = gap_label or f"{group_a}_minus_{group_b}"
    if group_a in wide.columns and group_b in wide.columns:
        wide[glabel] = (wide[group_a] - wide[group_b]).round(round_to)
    else:
        wide[glabel] = np.nan

    return {
        "result": wide,
        "aggregation_note": "Unweighted arithmetic mean of Percentage_Engaged",
        "aggregation_warning": AGGREGATION_WARNING if _should_warn(dims + [compare_col], df) else None,
        "compare_col": compare_col,
        "group_a": group_a,
        "group_b": group_b,
        "gap_label": glabel,
        "measure": MEASURE,
        "structural_absence_note": (
            "NaN in the result represents structural source absence. NaN is NOT zero."
        ),
    }


# ── 6. Trend — year-wise series ───────────────────────────────────────────────
def trend(
    df: pd.DataFrame,
    dimensions: Union[str, List[str]],
    *,
    round_to: int = 3,
) -> dict:
    """
    Pivot result so Years are columns. Structural NaN preserved.
    Convenience wrapper around pivot() with Year as the column axis.
    """
    return pivot(df, index=dimensions, columns="Year", round_to=round_to)


# ── 7. Year-vs-year endpoint change ──────────────────────────────────────────
def year_vs_year(
    df: pd.DataFrame,
    year_a: int,
    year_b: int,
    dimensions: Union[str, List[str]],
    *,
    round_to: int = 3,
) -> dict:
    """
    Compare two endpoint years across `dimensions`.

    Returns DataFrame:
        dimensions... | {year_a} | {year_b} | Absolute_Change | Percentage_Change | year_b_available
    """
    dims = [dimensions] if isinstance(dimensions, str) else list(dimensions)
    warn = _should_warn(dims, df)

    sub_a = (
        df[df["Year"] == year_a]
        .groupby(dims, observed=True)[MEASURE]
        .mean()
        .round(round_to)
        .rename(year_a)
    )
    sub_b = (
        df[df["Year"] == year_b]
        .groupby(dims, observed=True)[MEASURE]
        .mean()
        .round(round_to)
        .rename(year_b)
    )
    result = pd.concat([sub_a, sub_b], axis=1).reset_index()
    result["Absolute_Change"] = (result[year_b] - result[year_a]).round(round_to)
    result["Percentage_Change"] = (
        (result["Absolute_Change"] / result[year_a]) * 100
    ).round(2)
    result["year_b_available"] = result[year_b].notna()

    return {
        "result": result,
        "aggregation_note": "Unweighted arithmetic mean of Percentage_Engaged",
        "aggregation_warning": AGGREGATION_WARNING if warn else None,
        "year_a": year_a,
        "year_b": year_b,
        "measure": MEASURE,
        "structural_absence_note": (
            f"NaN in {year_b} column indicates structural source absence — "
            f"no observations for that combination in {year_b}. NaN is NOT zero."
        ),
    }
