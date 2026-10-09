"""
dataset_1_narratives.py
=======================
Reusable Narrative Engine for Dataset 1.

Architecture
------------
AnalyticalContext
        ↓
Structured insights (from dataset_1_insights.py)
        ↓
generate_narratives(ctx, insights)
        ↓
List of Narrative objects

Design principles
-----------------
- Does NOT perform analysis. All values come from structured insight objects.
- Generates narratives ONLY for insight types that actually exist in the
  current analytical result.
- Every narrative retains a reference to the source insight (traceability).
- Every narrative retains the analytical context (indicator, year, gender, etc.)
- Deterministic template-based language; no external LLM dependency.
- No causal interpretation.
- Distinguishes percentage (%) from percentage-point (pp) change explicitly.
- Uses precise numbers; no subjective labels unless an explicit rule exists.
- Respects missing values and incomplete coverage.
- Source-provided aggregates (Rural + Urban, All, Persons) are described
  as source-provided, never reconstructed.

Narrative object schema
-----------------------
{
    "narrative_type":       str,        # mirrors insight_type
    "insight_ref":          int,        # index into insights list (traceability)
    "indicator":            str,
    "context_summary":      str,        # one-line context description
    "context_metadata":     dict,       # full context for downstream use
    "headline":             str,        # short declarative statement
    "key_finding":          str,        # primary finding with numbers
    "supporting_evidence":  str | None, # secondary evidence
    "comparison":           str | None, # comparison statement (gaps, sides)
    "change_statement":     str | None, # change / trend statement
    "methodological_note":  str | None, # aggregation, missing values, etc.
}
"""

from __future__ import annotations
from typing import Optional
import math


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _fmt(v, decimals: int = 1) -> str:
    """Format a numeric value to `decimals` decimal places; return 'N/A' for None/NaN."""
    if v is None:
        return "N/A"
    try:
        if math.isnan(float(v)):
            return "N/A"
        return f"{float(v):.{decimals}f}"
    except (TypeError, ValueError):
        return str(v)


def _direction(val, zero_label: str = "no change") -> str:
    """Return 'increased', 'decreased', or the zero label."""
    if val is None:
        return zero_label
    try:
        f = float(val)
        if f > 0:
            return "increased"
        if f < 0:
            return "decreased"
        return zero_label
    except (TypeError, ValueError):
        return zero_label


def _gap_direction(gap_direction_str: str, group_a: str, group_b: str) -> str:
    """Convert 'a_higher' / 'b_higher' / 'equal' to a readable phrase."""
    if gap_direction_str == "a_higher":
        return f"{group_a} recorded higher values than {group_b}"
    if gap_direction_str == "b_higher":
        return f"{group_b} recorded higher values than {group_a}"
    return f"{group_a} and {group_b} recorded similar values"


def _ctx_label(ctx_meta: dict) -> str:
    """Build a concise one-line context description from context metadata."""
    parts = []
    if ctx_meta.get("Gender"):
        g = ctx_meta["Gender"]
        parts.append(g if isinstance(g, str) else "/".join(g))
    ind = ctx_meta.get("indicator", "")
    if ind:
        parts.append(ind)
    if ctx_meta.get("Year"):
        yr = ctx_meta["Year"]
        parts.append(str(yr))
    if ctx_meta.get("year_range"):
        yr = ctx_meta["year_range"]
        parts.append(f"{yr[0]}–{yr[1]}")
    if ctx_meta.get("Area_Type"):
        at = ctx_meta["Area_Type"]
        parts.append(at if isinstance(at, str) else "/".join(at))
    if ctx_meta.get("Education"):
        ed = ctx_meta["Education"]
        if isinstance(ed, str):
            parts.append(f"Education = {ed}")
    return " | ".join(parts) if parts else ""


def _base_narrative(narrative_type: str, insight_ref: int,
                    indicator: str, ctx_meta: dict) -> dict:
    """Return a narrative skeleton."""
    return {
        "narrative_type":      narrative_type,
        "insight_ref":         insight_ref,
        "indicator":           indicator,
        "context_summary":     _ctx_label(ctx_meta),
        "context_metadata":    ctx_meta,
        "headline":            "",
        "key_finding":         "",
        "supporting_evidence": None,
        "comparison":          None,
        "change_statement":    None,
        "methodological_note": None,
    }


def _method_note(finding: dict, extra: str = "") -> Optional[str]:
    """Build a methodological note from the finding dict if relevant."""
    notes = []
    agg = finding.get("aggregation_method") or finding.get("aggregation_note")
    if agg and "unweighted" in str(agg).lower():
        notes.append(f"Values are based on an {agg} across the selected groups.")
    agg_flag = finding.get("aggregated_across_other_dimensions")
    if agg_flag:
        notes.append("Group-level means were computed by aggregating across all other "
                     "dimensions present in the result.")
    missing = finding.get("missing_count")
    if missing:
        notes.append(f"{missing} observation(s) had missing values and were excluded "
                     "from calculations.")
    if extra:
        notes.append(extra)
    return " ".join(notes) if notes else None


def _build_ctx_meta(ctx, indicator: str) -> dict:
    """Merge the AnalyticalContext into a flat metadata dict for the narrative."""
    meta = dict(ctx.filters)
    meta["indicator"]          = indicator
    meta["dimensions"]         = ctx.dimensions
    meta["analysis_type"]      = ctx.analysis_type
    meta["aggregation_note"]   = ctx.aggregation_note
    if ctx.year_range:
        meta["year_range"] = ctx.year_range
    if ctx.endpoint_years:
        meta["endpoint_years"] = ctx.endpoint_years
    if ctx.compare_col:
        meta["compare_col"] = ctx.compare_col
        meta["group_a"]     = ctx.group_a
        meta["group_b"]     = ctx.group_b
    return meta


# ─────────────────────────────────────────────────────────────────────────────
# 1. Level narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_level(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes the overall level of the indicator in the selected view.
    """
    ind   = insight["indicator"]
    f     = insight["finding"]
    meta  = _build_ctx_meta(ctx, ind)
    n     = _base_narrative("level", insight_ref, ind, meta)

    ctx_label = _ctx_label(meta)
    obs   = f.get("observation_count", "N/A")
    mean  = _fmt(f.get("mean_value"))
    mn    = _fmt(f.get("min_value"))
    mx    = _fmt(f.get("max_value"))
    miss  = f.get("missing_count", 0)

    n["headline"]    = f"{ind} across the selected analytical view"
    n["key_finding"] = (
        f"The selected view ({ctx_label}) contains {obs} observations. "
        f"The mean {ind} is {mean}%, ranging from {mn}% to {mx}%."
    )
    if miss:
        n["supporting_evidence"] = (
            f"{miss} observation(s) have missing values and are excluded from calculations."
        )
    n["methodological_note"] = ctx.aggregation_note or None
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 2. Variation narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_variation(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes highest/lowest group and range for one dimension.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("variation", insight_ref, ind, meta)

    dim      = f.get("dimension", "group")
    hi_grp   = f.get("highest_group", "N/A")
    hi_val   = _fmt(f.get("highest_value"))
    lo_grp   = f.get("lowest_group", "N/A")
    lo_val   = _fmt(f.get("lowest_value"))
    rng      = _fmt(f.get("range"))
    n_grps   = f.get("groups_with_data", "N/A")
    ctx_lbl  = _ctx_label(meta)

    n["headline"] = (
        f"{ind} varies across {dim} in the selected view"
    )
    n["key_finding"] = (
        f"In the selected view ({ctx_lbl}), {ind} ranged from "
        f"{lo_val}% ({lo_grp}) to {hi_val}% ({hi_grp}), "
        f"a range of {rng} percentage points across {n_grps} {dim} groups."
    )
    n["supporting_evidence"] = (
        f"{hi_grp} recorded the highest observed {ind} ({hi_val}%). "
        f"{lo_grp} recorded the lowest ({lo_val}%)."
    )
    n["methodological_note"] = _method_note(f, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 3. Group comparison narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_group_comparison(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes a side-by-side comparison for one row (one time point / dimension value).
    Returns one narrative per insight record.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("group_comparison", insight_ref, ind, meta)

    grp_a    = f.get("group_a", ctx.group_a or "Group A")
    grp_b    = f.get("group_b", ctx.group_b or "Group B")
    col_name = f.get("compare_col", ctx.compare_col or "group")
    val_a    = _fmt(f.get("value_a"))
    val_b    = _fmt(f.get("value_b"))
    gap      = f.get("gap_a_minus_b")
    gap_dir  = f.get("gap_direction", "")
    ctx_lbl  = _ctx_label(meta)

    # Dim context from the finding
    dim_parts = {k.replace("dim_", ""): v for k, v in f.items() if k.startswith("dim_")}
    dim_str   = ", ".join(f"{k} = {v}" for k, v in dim_parts.items()) if dim_parts else ""
    point_str = f" ({dim_str})" if dim_str else ""

    n["headline"]  = f"{grp_a} vs {grp_b} {ind} comparison{point_str}"
    n["key_finding"] = (
        f"In the selected view ({ctx_lbl}){point_str}, {grp_a} {ind} was {val_a}% "
        f"compared with {val_b}% for {grp_b}."
    )
    if gap is not None:
        abs_gap = abs(float(gap))
        higher  = grp_a if float(gap) > 0 else grp_b if float(gap) < 0 else None
        lower   = grp_b if float(gap) > 0 else grp_a if float(gap) < 0 else None
        n["comparison"] = (
            f"The {grp_a}−{grp_b} {ind} gap was {_fmt(abs_gap)} percentage points"
            + (f", with {higher} recording the higher value." if higher else ".")
        )
    n["methodological_note"] = _method_note({}, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 4. Gap summary narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_gap_summary(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes the overall gap pattern, including change over time where available.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("gap_summary", insight_ref, ind, meta)

    grp_a    = f.get("group_a", ctx.group_a or "Group A")
    grp_b    = f.get("group_b", ctx.group_b or "Group B")
    max_gap  = _fmt(f.get("max_gap"))
    min_gap  = _fmt(f.get("min_gap"))
    mean_gap = _fmt(f.get("mean_gap"))
    gap_dir  = f.get("gap_direction_overall", "")
    widening = f.get("widening")
    gap_yr   = f.get("gap_by_year") or {}
    ctx_lbl  = _ctx_label(meta)

    direction_str = _gap_direction(gap_dir, grp_a, grp_b)

    n["headline"] = (
        f"{grp_a}−{grp_b} {ind} gap in the selected view"
    )
    n["key_finding"] = (
        f"In the selected view ({ctx_lbl}), {direction_str}. "
        f"The {grp_a}−{grp_b} {ind} gap ranged from {min_gap} to {max_gap} percentage points, "
        f"with a mean gap of {mean_gap} percentage points."
    )

    if gap_yr:
        first_yr = min(gap_yr)
        last_yr  = max(gap_yr)
        first_gap = _fmt(gap_yr[first_yr])
        last_gap  = _fmt(gap_yr[last_yr])
        n["comparison"] = (
            f"The gap was {first_gap} percentage points in {first_yr} "
            f"and {last_gap} percentage points in {last_yr}."
        )
        if widening is not None:
            direction_word = "widened" if widening else "narrowed"
            n["change_statement"] = (
                f"The {grp_a}−{grp_b} {ind} gap {direction_word} over the selected period "
                f"({first_yr}–{last_yr})."
            )

    n["methodological_note"] = _method_note({}, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 5. Trend narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_trend(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes the time trend for an indicator.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("trend", insight_ref, ind, meta)

    start_yr  = f.get("start_year")
    end_yr    = f.get("end_year")
    start_val = _fmt(f.get("start_value"))
    end_val   = _fmt(f.get("end_value"))
    abs_chg   = f.get("absolute_change")
    pct_chg   = f.get("percentage_change")
    direction = f.get("direction", "")
    n_yrs     = f.get("years_observed", "")
    ctx_lbl   = _ctx_label(meta)

    dir_word = {"increasing": "increased", "decreasing": "decreased", "flat": "remained stable"}.get(direction, direction)

    n["headline"] = (
        f"{ind} {dir_word} between {start_yr} and {end_yr} in the selected view"
    )
    n["key_finding"] = (
        f"In the selected view ({ctx_lbl}), {ind} was {start_val}% in {start_yr} "
        f"and {end_val}% in {end_yr}, across {n_yrs} observed years."
    )
    if abs_chg is not None:
        change_word = "increase" if float(abs_chg) >= 0 else "decrease"
        n["change_statement"] = (
            f"This represents a {_fmt(abs(float(abs_chg)))} percentage-point "
            f"{change_word} over the period"
            + (f" ({_fmt(abs(float(pct_chg)))}% change)." if pct_chg is not None else ".")
        )

    # YoY highlights
    yrs_inc = f.get("years_of_increase")
    yrs_dec = f.get("years_of_decrease")
    max_inc = f.get("max_increase")
    max_inc_yr = f.get("max_increase_year")
    max_dec = f.get("max_decrease")
    max_dec_yr = f.get("max_decrease_year")

    parts = []
    if yrs_inc is not None and yrs_dec is not None:
        parts.append(
            f"Year-on-year increases were recorded in {yrs_inc} year(s) and "
            f"decreases in {yrs_dec} year(s)."
        )
    if max_inc is not None and max_inc_yr is not None:
        parts.append(
            f"The largest year-on-year increase was {_fmt(max_inc)} percentage points "
            f"({max_inc_yr})."
        )
    if max_dec is not None and max_dec_yr is not None and float(max_dec) < 0:
        parts.append(
            f"The largest year-on-year decrease was {_fmt(abs(float(max_dec)))} percentage points "
            f"({max_dec_yr})."
        )
    if parts:
        n["supporting_evidence"] = " ".join(parts)

    n["methodological_note"] = _method_note({}, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 6. Year-on-year change narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_yoy_change(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes the year-by-year change record.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("yoy_change", insight_ref, ind, meta)

    records  = f.get("year_records", [])
    ctx_lbl  = _ctx_label(meta)

    if not records:
        n["headline"]    = f"Year-on-year {ind} changes — no data"
        n["key_finding"] = "No year-on-year records were available in the selected view."
        return n

    # Describe the record with largest and smallest YoY change
    with_yoy = [r for r in records if r.get("yoy_change") is not None]
    if with_yoy:
        max_r = max(with_yoy, key=lambda r: float(r["yoy_change"]))
        min_r = min(with_yoy, key=lambda r: float(r["yoy_change"]))

        n["headline"] = f"Year-on-year {ind} changes in the selected view"
        n["key_finding"] = (
            f"In the selected view ({ctx_lbl}), {ind} changed in each year from "
            f"{records[0]['year']} to {records[-1]['year']}."
        )
        n["supporting_evidence"] = (
            f"The largest year-on-year increase was {_fmt(max_r['yoy_change'])} percentage points "
            f"in {max_r['year']} (value: {_fmt(max_r['value'])}%). "
            f"The largest year-on-year decrease was "
            f"{_fmt(abs(float(min_r['yoy_change'])))} percentage points in {min_r['year']} "
            f"(value: {_fmt(min_r['value'])}%)."
        )

    n["methodological_note"] = _method_note({}, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 7. Period change narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_period_change(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes absolute and percentage change between two years across groups.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("period_change", insight_ref, ind, meta)

    records  = f.get("group_records", [])
    summary  = f.get("summary", {})
    ctx_lbl  = _ctx_label(meta)
    ep       = ctx.endpoint_years or (None, None)
    ya, yb   = ep

    dims = ctx.dimensions

    n["headline"] = (
        f"{ind} change between {ya} and {yb} across {' × '.join(dims)} in the selected view"
    )

    # Use summary for key finding
    mean_chg   = _fmt(summary.get("mean_absolute_change"))
    hi_inc_grp = summary.get("largest_increase_group", {})
    hi_inc_val = _fmt(summary.get("largest_absolute_increase"))
    hi_dec_grp = summary.get("largest_decrease_group", {})
    hi_dec_val = _fmt(summary.get("largest_absolute_decrease"))
    max_pct    = _fmt(summary.get("max_percentage_change"))
    min_pct    = _fmt(summary.get("min_percentage_change"))

    n_groups   = len(records)
    # Determine how many increased vs decreased
    n_inc = sum(1 for r in records if (r.get("absolute_change") or 0) > 0)
    n_dec = sum(1 for r in records if (r.get("absolute_change") or 0) < 0)
    n_flat = n_groups - n_inc - n_dec

    n["key_finding"] = (
        f"In the selected view ({ctx_lbl}), {ind} changed between {ya} and {yb} "
        f"across {n_groups} {' × '.join(dims)} group(s). "
        f"The mean absolute change was {mean_chg} percentage points."
    )
    n["supporting_evidence"] = (
        f"{n_inc} group(s) recorded an increase, {n_dec} a decrease, "
        f"and {n_flat} no change."
    )

    change_parts = []
    if summary.get("largest_absolute_increase") is not None:
        grp_str = ", ".join(f"{k} = {v}" for k, v in hi_inc_grp.items())
        change_parts.append(
            f"The largest absolute increase was {hi_inc_val} percentage points "
            f"({grp_str}; percentage change: {max_pct}%)."
        )
    if summary.get("largest_absolute_decrease") is not None:
        grp_str = ", ".join(f"{k} = {v}" for k, v in hi_dec_grp.items())
        change_parts.append(
            f"The smallest absolute increase (or largest decrease) was "
            f"{hi_dec_val} percentage points ({grp_str}; percentage change: {min_pct}%)."
        )
    if change_parts:
        n["change_statement"] = " ".join(change_parts)

    n["methodological_note"] = _method_note({}, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 8. Dimension pattern narrative
# ─────────────────────────────────────────────────────────────────────────────

def narrate_dimension_pattern(ctx, insight: dict, insight_ref: int) -> dict:
    """
    Describes the statistical spread of indicator values across a dimension.
    """
    ind  = insight["indicator"]
    f    = insight["finding"]
    meta = _build_ctx_meta(ctx, ind)
    n    = _base_narrative("dimension_pattern", insight_ref, ind, meta)

    dim      = f.get("dimension", "group")
    mean_v   = _fmt(f.get("mean_across_groups"))
    std_v    = _fmt(f.get("std_across_groups"))
    cv_v     = f.get("cv_across_groups")
    q25      = _fmt(f.get("q25"))
    median_v = _fmt(f.get("median"))
    q75      = _fmt(f.get("q75"))
    n_grps   = f.get("groups_with_data", "N/A")
    ctx_lbl  = _ctx_label(meta)

    n["headline"] = f"{ind} distribution across {dim} groups in the selected view"
    n["key_finding"] = (
        f"In the selected view ({ctx_lbl}), the mean {ind} across {n_grps} {dim} group(s) "
        f"was {mean_v}%, with a standard deviation of {std_v} percentage points."
    )
    n["supporting_evidence"] = (
        f"The distribution shows a median of {median_v}% (Q1: {q25}%, Q3: {q75}%)."
    )
    if cv_v is not None:
        try:
            cv_pct = float(cv_v) * 100
            n["comparison"] = (
                f"The coefficient of variation across {dim} groups was "
                f"{_fmt(cv_pct)}%, indicating the relative spread of {ind} values."
            )
        except (TypeError, ValueError):
            pass

    n["methodological_note"] = _method_note(f, ctx.aggregation_note or "")
    return n


# ─────────────────────────────────────────────────────────────────────────────
# 9. Master dispatcher
# ─────────────────────────────────────────────────────────────────────────────

_NARRATORS = {
    "level":             narrate_level,
    "variation":         narrate_variation,
    "group_comparison":  narrate_group_comparison,
    "gap_summary":       narrate_gap_summary,
    "trend":             narrate_trend,
    "yoy_change":        narrate_yoy_change,
    "period_change":     narrate_period_change,
    "dimension_pattern": narrate_dimension_pattern,
}


def generate_narratives(ctx, insights: list[dict]) -> list[dict]:
    """
    Generate narrative objects for all structured insights.

    Parameters
    ----------
    ctx      : AnalyticalContext
    insights : List of structured insight dicts from detect_applicable_insights()

    Returns
    -------
    List of narrative dicts. Each narrative's 'insight_ref' is the index of the
    source insight in the input list, enabling full traceability:

        insight[n]  →  narrative with insight_ref == n
    """
    narratives = []
    for idx, insight in enumerate(insights):
        itype   = insight.get("insight_type")
        narrator = _NARRATORS.get(itype)
        if narrator is None:
            continue  # unknown type — skip silently
        try:
            narr = narrator(ctx, insight, insight_ref=idx)
            narratives.append(narr)
        except Exception as exc:
            # Do not crash the engine; record the failure transparently
            narratives.append({
                "narrative_type":      itype,
                "insight_ref":         idx,
                "indicator":           insight.get("indicator", ""),
                "context_summary":     "",
                "context_metadata":    {},
                "headline":            f"[Narrative generation error for insight {idx}]",
                "key_finding":         str(exc),
                "supporting_evidence": None,
                "comparison":          None,
                "change_statement":    None,
                "methodological_note": None,
            })
    return narratives


# ─────────────────────────────────────────────────────────────────────────────
# 10. Print helper (inspection; not part of production API)
# ─────────────────────────────────────────────────────────────────────────────

def print_narratives(narratives: list[dict], title: str = "") -> None:
    """Pretty-print narrative objects for review."""
    if title:
        print(f"\n{'═'*66}")
        print(f"  {title}")
        print(f"{'═'*66}")
    for n in narratives:
        print(f"\n[Narrative]  type={n['narrative_type']}  "
              f"indicator={n['indicator']}  insight_ref={n['insight_ref']}")
        print(f"  Context    : {n['context_summary']}")
        print(f"  Headline   : {n['headline']}")
        print(f"  Key finding: {n['key_finding']}")
        if n.get("supporting_evidence"):
            print(f"  Evidence   : {n['supporting_evidence']}")
        if n.get("comparison"):
            print(f"  Comparison : {n['comparison']}")
        if n.get("change_statement"):
            print(f"  Change     : {n['change_statement']}")
        if n.get("methodological_note"):
            print(f"  Method note: {n['methodological_note']}")
    if not narratives:
        print("  (no narratives generated)")
