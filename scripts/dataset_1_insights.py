"""
dataset_1_insights.py
=====================
Dynamic, user-selection-aware Insight Framework for Dataset 1.

Architecture
------------
USER SELECTION (AnalyticalContext)
        ↓
ANALYTICAL RESULT  (DataFrame from dataset_1_analytics.py)
        ↓
detect_applicable_insights(ctx, result)
        ↓
STRUCTURED INSIGHT OBJECTS  (list of dicts)

Design principles
-----------------
- Insight types are activated ONLY when the context and result data support them.
- No hard-coded Q1-Q26 logic.
- No narrative prose — structured findings only.
- Values are always traced back to the analytical result.
- Missing values remain missing; zero is valid.
- Source aggregates (Rural + Urban, All, Persons, Secondary & Above) are never
  reconstructed.
- Unweighted analytical means are identified explicitly when used.
- No causal interpretation is introduced.
- No subjective labels ("large", "significant") unless an explicit rule defines them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Union
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# 1.  AnalyticalContext — describes the user's current selection
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AnalyticalContext:
    """
    Represents everything the user has selected for a given analytical view.

    Parameters
    ----------
    indicators      : one or more of LFPR, WPR, Unemployment_Rate
    dimensions      : dimension(s) present in the result DataFrame
    filters         : dict of dimension → value(s) applied before analysis
    analysis_type   : 'profile' | 'comparison' | 'trend' | 'yoy' | 'year_vs_year'
                      | 'multi_dimension'
    compare_col     : dimension used for side-by-side comparison (e.g. 'Gender')
    group_a         : first group in comparison (e.g. 'Female')
    group_b         : second group in comparison (e.g. 'Male')
    year_range      : (start_year, end_year) when a time range was selected
    endpoint_years  : (year_a, year_b) for year-vs-year comparison
    aggregation_note: free-text note about any aggregation applied
    """
    indicators:       list[str]
    dimensions:       list[str]
    filters:          dict[str, Any]             = field(default_factory=dict)
    analysis_type:    str                         = "profile"
    compare_col:      Optional[str]               = None
    group_a:          Optional[str]               = None
    group_b:          Optional[str]               = None
    year_range:       Optional[tuple[int, int]]   = None
    endpoint_years:   Optional[tuple[int, int]]   = None
    aggregation_note: str                         = ""

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def has_dimension(self, dim: str) -> bool:
        return dim in self.dimensions

    def is_comparison(self) -> bool:
        return self.analysis_type == "comparison" and self.compare_col is not None

    def is_trend(self) -> bool:
        return self.analysis_type in ("trend", "yoy") and "Year" in self.dimensions

    def is_year_vs_year(self) -> bool:
        return self.analysis_type == "year_vs_year" and self.endpoint_years is not None

    def to_dict(self) -> dict:
        return asdict(self)


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Individual insight-detection functions
#     Each returns a single structured insight dict or None.
# ─────────────────────────────────────────────────────────────────────────────

def _safe_val(v) -> Optional[float]:
    """Return float or None for NaN / pd.NA."""
    if v is None:
        return None
    try:
        if math.isnan(float(v)):
            return None
        return round(float(v), 3)
    except (TypeError, ValueError):
        return None


def _insight(insight_type: str, ctx: AnalyticalContext,
             indicator: str, finding: dict, **extra) -> dict:
    return {
        "insight_type": insight_type,
        "context": {
            **{k: v for k, v in ctx.filters.items()},
            "indicator":       indicator,
            "dimensions":      ctx.dimensions,
            "analysis_type":   ctx.analysis_type,
            "aggregation_note": ctx.aggregation_note,
        },
        "indicator": indicator,
        "finding":   finding,
        **extra,
    }


# ── 2a. Level insight ────────────────────────────────────────────────────────
def detect_level(ctx: AnalyticalContext, result: pd.DataFrame,
                 indicator: str) -> list[dict]:
    """
    Current indicator value(s) for the selected group(s).
    Applicable when result contains the indicator column directly
    (not in comparison/wide format).
    Triggered by: profile, trend (any row), multi_dimension.
    """
    if indicator not in result.columns:
        return []
    vals = result[indicator].dropna()
    if vals.empty:
        return []
    # Report the full set of values as a level summary
    return [_insight(
        "level", ctx, indicator,
        finding={
            "observation_count": int(len(vals)),
            "mean_value":        _safe_val(vals.mean()),
            "min_value":         _safe_val(vals.min()),
            "max_value":         _safe_val(vals.max()),
            "missing_count":     int(result[indicator].isna().sum()),
        }
    )]


# ── 2b. Variation (highest / lowest / range) ─────────────────────────────────
def detect_variation(ctx: AnalyticalContext, result: pd.DataFrame,
                     indicator: str, dimension: str) -> list[dict]:
    """
    Highest / lowest group and range for one dimension.

    For single-dimension results (one row per group) the indicator value is
    used directly.  For multi-dimension results the indicator is first
    aggregated (unweighted arithmetic mean, NaN-excluded) across all OTHER
    dimensions present in the result, producing one representative value per
    group in the target dimension before highest/lowest are identified.

    This ensures the statistic is always a group-level summary, not the
    value of a single full-grain cell.
    """
    if indicator not in result.columns or dimension not in result.columns:
        return []
    sub = result[[dimension, indicator]].dropna(subset=[indicator])
    if len(sub) < 2:
        return []



    # Aggregate by the target dimension across all other dimensions.
    # For a single-dimension result each group already has one row, so
    # groupby().mean() is a no-op and the result is identical.
    grp = sub.groupby(dimension, observed=True)[indicator].mean()
    grp = grp.dropna()
    if len(grp) < 2:
        return []

    aggregated = grp.reset_index()
    aggregated.columns = [dimension, indicator]

    hi_idx = aggregated[indicator].idxmax()
    lo_idx = aggregated[indicator].idxmin()
    hi_grp = aggregated.loc[hi_idx, dimension]
    lo_grp = aggregated.loc[lo_idx, dimension]
    hi_val = _safe_val(aggregated.loc[hi_idx, indicator])
    lo_val = _safe_val(aggregated.loc[lo_idx, indicator])
    rng    = _safe_val(hi_val - lo_val) if (hi_val is not None and lo_val is not None) else None

    # Record whether aggregation was actually applied (more than one
    # row per group existed in the input).
    rows_per_group   = sub.groupby(dimension, observed=True).size()
    aggregated_flag  = bool((rows_per_group > 1).any())

    return [_insight(
        "variation", ctx, indicator,
        finding={
            "dimension":            dimension,
            "highest_group":        hi_grp,
            "highest_value":        hi_val,
            "lowest_group":         lo_grp,
            "lowest_value":         lo_val,
            "range":                rng,
            "groups_with_data":     int(len(grp)),
            "aggregated_across_other_dimensions": aggregated_flag,
            "aggregation_method":   "unweighted arithmetic mean" if aggregated_flag else "direct (one row per group)",
        }
    )]



# ── 2c. Group comparison (Female vs Male, Rural vs Urban, etc.) ───────────────
def detect_group_comparison(ctx: AnalyticalContext, result: pd.DataFrame,
                             indicator: str) -> list[dict]:
    """
    Side-by-side values and gap for a comparison.
    Triggered when ctx.is_comparison() and the result has wide columns
    {indicator}_{group_a} and {indicator}_{group_b}.
    """
    if not ctx.is_comparison():
        return []
    col_a = f"{indicator}_{ctx.group_a}"
    col_b = f"{indicator}_{ctx.group_b}"
    gap_col = f"{ctx.group_a}\u2212{ctx.group_b}_Gap"  # e.g. Female−Male_Gap

    # Try alternative gap column names produced by compare()
    alt_gap_cols = [c for c in result.columns if "Gap" in c and indicator in c]

    if col_a not in result.columns or col_b not in result.columns:
        return []

    insights = []
    for _, row in result.iterrows():
        a_val   = _safe_val(row.get(col_a))
        b_val   = _safe_val(row.get(col_b))
        gap_val = None
        if gap_col in result.columns:
            gap_val = _safe_val(row.get(gap_col))
        elif alt_gap_cols:
            gap_val = _safe_val(row.get(alt_gap_cols[0]))
        elif a_val is not None and b_val is not None:
            gap_val = round(a_val - b_val, 3)

        dim_vals = {d: row[d] for d in ctx.dimensions
                    if d in result.columns and d != ctx.compare_col}

        insights.append(_insight(
            "group_comparison", ctx, indicator,
            finding={
                "compare_col":   ctx.compare_col,
                "group_a":       ctx.group_a,
                "group_b":       ctx.group_b,
                "value_a":       a_val,
                "value_b":       b_val,
                "gap_a_minus_b": gap_val,
                "gap_direction": ("a_higher" if (gap_val or 0) > 0
                                  else "b_higher" if (gap_val or 0) < 0
                                  else "equal"),
                **{f"dim_{k}": v for k, v in dim_vals.items()},
            }
        ))
    return insights


# ── 2d. Gap summary (across time or groups) ───────────────────────────────────
def detect_gap_summary(ctx: AnalyticalContext, result: pd.DataFrame,
                        indicator: str) -> list[dict]:
    """
    Summarises the gap column: max, min, direction at start/end of time range.
    Triggered when comparison is active and a gap column exists.
    """
    if not ctx.is_comparison():
        return []
    col_a   = f"{indicator}_{ctx.group_a}"
    col_b   = f"{indicator}_{ctx.group_b}"
    alt_gap = [c for c in result.columns if "Gap" in c and indicator in c]
    if not alt_gap and (col_a not in result.columns or col_b not in result.columns):
        return []

    if alt_gap:
        gap_series = result[alt_gap[0]].dropna()
    else:
        gap_series = (result[col_a] - result[col_b]).dropna()

    if len(gap_series) < 2:
        return []

    # Time-indexed gap stats
    gap_by_year: dict = {}
    if "Year" in result.columns:
        for _, row in result.iterrows():
            yr = int(row["Year"]) if not pd.isna(row["Year"]) else None
            if yr is None:
                continue
            g = (row[alt_gap[0]] if alt_gap else row[col_a] - row[col_b])
            if not pd.isna(g):
                gap_by_year[yr] = round(float(g), 3)

    return [_insight(
        "gap_summary", ctx, indicator,
        finding={
            "compare_col":           ctx.compare_col,
            "group_a":               ctx.group_a,
            "group_b":               ctx.group_b,
            "max_gap":               _safe_val(gap_series.max()),
            "min_gap":               _safe_val(gap_series.min()),
            "mean_gap":              _safe_val(gap_series.mean()),
            "gap_direction_overall": ("a_higher" if gap_series.mean() > 0
                                      else "b_higher" if gap_series.mean() < 0
                                      else "equal"),
            "gap_by_year":           gap_by_year if gap_by_year else None,
            "widening": (bool(gap_series.iloc[-1] > gap_series.iloc[0])
                         if len(gap_series) > 1 else None),
        }
    )]


# ── 2e. Trend ──────────────────────────────────────────────────────────────
def detect_trend(ctx: AnalyticalContext, result: pd.DataFrame,
                 indicator: str) -> list[dict]:
    """
    Start/end values, overall direction, YoY statistics.
    Triggered when Year is a dimension and indicator column exists.
    """
    if "Year" not in result.columns or indicator not in result.columns:
        return []
    ts = result[["Year", indicator]].dropna(subset=[indicator]).sort_values("Year")
    if len(ts) < 2:
        return []

    start_yr  = int(ts["Year"].iloc[0])
    end_yr    = int(ts["Year"].iloc[-1])
    start_val = _safe_val(ts[indicator].iloc[0])
    end_val   = _safe_val(ts[indicator].iloc[-1])
    abs_chg   = _safe_val(end_val - start_val) if (start_val is not None and end_val is not None) else None
    pct_chg   = (round(abs_chg / start_val * 100, 3)
                 if abs_chg is not None and start_val and start_val != 0 else None)

    # YoY stats if available
    yoy_stats: dict = {}
    if "YoY_Change" in result.columns:
        yoy = result["YoY_Change"].dropna()
        if not yoy.empty:
            yoy_stats = {
                "max_increase":       _safe_val(yoy.max()),
                "max_increase_year":  int(result.loc[yoy.idxmax(), "Year"]),
                "max_decrease":       _safe_val(yoy.min()),
                "max_decrease_year":  int(result.loc[yoy.idxmin(), "Year"]),
                "years_of_increase":  int((yoy > 0).sum()),
                "years_of_decrease":  int((yoy < 0).sum()),
            }

    return [_insight(
        "trend", ctx, indicator,
        finding={
            "start_year":       start_yr,
            "end_year":         end_yr,
            "start_value":      start_val,
            "end_value":        end_val,
            "absolute_change":  abs_chg,
            "percentage_change": pct_chg,
            "direction":        ("increasing" if (abs_chg or 0) > 0
                                 else "decreasing" if (abs_chg or 0) < 0
                                 else "flat"),
            "years_observed":   int(len(ts)),
            **yoy_stats,
        }
    )]


# ── 2f. Year-on-Year change detail ───────────────────────────────────────────
def detect_yoy(ctx: AnalyticalContext, result: pd.DataFrame,
               indicator: str) -> list[dict]:
    """
    Year-by-year change records.
    Triggered when YoY_Change column is in the result.
    """
    if "YoY_Change" not in result.columns or "Year" not in result.columns:
        return []
    records = []
    for _, row in result.iterrows():
        yr  = row.get("Year")
        val = row.get(indicator)
        yoy = row.get("YoY_Change")
        if pd.isna(yr):
            continue
        records.append({
            "year":       int(yr),
            "value":      _safe_val(val),
            "yoy_change": _safe_val(yoy),
        })
    return [_insight(
        "yoy_change", ctx, indicator,
        finding={"year_records": records}
    )]


# ── 2g. Period change (year_vs_year) ─────────────────────────────────────────
def detect_period_change(ctx: AnalyticalContext, result: pd.DataFrame,
                          indicator: str) -> list[dict]:
    """
    Absolute and percentage change between two selected years, for each group
    in the result (e.g. each Education category).
    Triggered when endpoint_years is set and result contains those columns.
    """
    if not ctx.is_year_vs_year():
        return []
    ya, yb    = ctx.endpoint_years
    col_a     = f"{indicator}_{ya}"
    col_b     = f"{indicator}_{yb}"
    if col_a not in result.columns or col_b not in result.columns:
        return []

    group_dims = [d for d in ctx.dimensions if d in result.columns]
    records    = []
    for _, row in result.iterrows():
        v_a    = _safe_val(row[col_a])
        v_b    = _safe_val(row[col_b])
        abs_c  = _safe_val(row.get("Absolute_Change"))
        pct_c  = _safe_val(row.get("Percentage_Change"))
        if abs_c is None and v_a is not None and v_b is not None:
            abs_c = round(v_b - v_a, 3)
        if pct_c is None and abs_c is not None and v_a and v_a != 0:
            pct_c = round(abs_c / v_a * 100, 3)
        records.append({
            **{d: row[d] for d in group_dims},
            f"value_{ya}":        v_a,
            f"value_{yb}":        v_b,
            "absolute_change":    abs_c,
            "percentage_change":  pct_c,
            "direction":          ("increase" if (abs_c or 0) > 0
                                   else "decrease" if (abs_c or 0) < 0
                                   else "flat"),
        })

    # Summary across groups
    abs_vals = [r["absolute_change"] for r in records if r["absolute_change"] is not None]
    pct_vals = [r["percentage_change"] for r in records if r["percentage_change"] is not None]

    summary: dict = {}
    if abs_vals:
        max_abs   = max(abs_vals)
        min_abs   = min(abs_vals)
        max_rec   = next(r for r in records if r["absolute_change"] == max_abs)
        min_rec   = next(r for r in records if r["absolute_change"] == min_abs)
        summary = {
            "largest_absolute_increase": max_abs,
            "largest_increase_group":    {d: max_rec[d] for d in group_dims},
            "largest_absolute_decrease": min_abs,
            "largest_decrease_group":    {d: min_rec[d] for d in group_dims},
            "mean_absolute_change":      round(sum(abs_vals) / len(abs_vals), 3),
        }
    if pct_vals:
        summary["max_percentage_change"] = max(pct_vals)
        summary["min_percentage_change"] = min(pct_vals)

    return [_insight(
        "period_change", ctx, indicator,
        finding={"group_records": records, "summary": summary}
    )]


# ── 2h. Dimension pattern (variation across a non-primary dimension) ──────────
def detect_dimension_pattern(ctx: AnalyticalContext, result: pd.DataFrame,
                              indicator: str, dimension: str) -> list[dict]:
    """
    Quantifies spread across a specific dimension (std, CV, quartiles).
    Triggered when the dimension is in the result with ≥3 distinct groups.
    """
    if indicator not in result.columns or dimension not in result.columns:
        return []
    grp_vals = result.groupby(dimension)[indicator].mean().dropna()
    if len(grp_vals) < 3:
        return []

    std = grp_vals.std()
    mean = grp_vals.mean()
    cv   = std / mean if mean != 0 else None

    return [_insight(
        "dimension_pattern", ctx, indicator,
        finding={
            "dimension":           dimension,
            "groups_with_data":    int(len(grp_vals)),
            "mean_across_groups":  _safe_val(mean),
            "std_across_groups":   _safe_val(std),
            "cv_across_groups":    _safe_val(cv),
            "q25":                 _safe_val(grp_vals.quantile(0.25)),
            "median":              _safe_val(grp_vals.median()),
            "q75":                 _safe_val(grp_vals.quantile(0.75)),
        }
    )]


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Master dispatcher — detect_applicable_insights
# ─────────────────────────────────────────────────────────────────────────────

def detect_applicable_insights(
    ctx: AnalyticalContext,
    result: pd.DataFrame,
) -> list[dict]:
    """
    Inspect the AnalyticalContext and the analytical result, then activate
    only the insight types that are genuinely supported.

    Returns a list of structured insight dicts.
    """
    all_insights: list[dict] = []

    for indicator in ctx.indicators:

        # ── PROFILE / MULTI-DIMENSION ──────────────────────────────────────
        if ctx.analysis_type in ("profile", "multi_dimension"):
            # Level summary
            all_insights += detect_level(ctx, result, indicator)

            # Variation for each categorical dimension in the result
            for dim in ctx.dimensions:
                if dim == "Year":
                    continue
                if dim in result.columns and result[dim].nunique() >= 2:
                    all_insights += detect_variation(ctx, result, indicator, dim)
                    all_insights += detect_dimension_pattern(ctx, result, indicator, dim)

        # ── COMPARISON ────────────────────────────────────────────────────
        elif ctx.analysis_type == "comparison":
            all_insights += detect_group_comparison(ctx, result, indicator)
            all_insights += detect_gap_summary(ctx, result, indicator)

            # Variation over any non-compare dimension (e.g. Year)
            for dim in ctx.dimensions:
                if dim == ctx.compare_col:
                    continue
                if dim in result.columns and result[dim].nunique() >= 2:
                    # summarise gap direction across that dimension
                    pass  # captured in gap_summary already

        # ── TREND / YOY ───────────────────────────────────────────────────
        elif ctx.analysis_type in ("trend", "yoy"):
            all_insights += detect_trend(ctx, result, indicator)
            if ctx.analysis_type == "yoy":
                all_insights += detect_yoy(ctx, result, indicator)

            # If it's also a comparison (e.g. Rural vs Urban over time)
            if ctx.is_comparison():
                all_insights += detect_group_comparison(ctx, result, indicator)
                all_insights += detect_gap_summary(ctx, result, indicator)

        # ── YEAR VS YEAR ──────────────────────────────────────────────────
        elif ctx.analysis_type == "year_vs_year":
            all_insights += detect_period_change(ctx, result, indicator)

            # Variation over the grouping dimension for each year
            for dim in ctx.dimensions:
                if dim in result.columns and result[dim].nunique() >= 2:
                    for ya, yb in [ctx.endpoint_years]:
                        for yc in [ya, yb]:
                            col = f"{indicator}_{yc}"
                            if col in result.columns:
                                sub = result.rename(columns={col: indicator})
                                all_insights += detect_variation(ctx, sub, indicator, dim)

    return all_insights


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Pretty-print helper (for inspection; not part of the production API)
# ─────────────────────────────────────────────────────────────────────────────

def print_insights(insights: list[dict], title: str = "") -> None:
    import json
    if title:
        print(f"\n{'═'*66}")
        print(f"  {title}")
        print(f"{'═'*66}")
    for i, ins in enumerate(insights, 1):
        print(f"\n[Insight {i}]  type={ins['insight_type']}  "
              f"indicator={ins.get('indicator','')}")
        print(json.dumps(ins["finding"], indent=4, default=str))
    if not insights:
        print("  (no insights generated)")
