# Phase 6 — Statistical Analysis Plan
## Women's Labour Market Diagnostic in India

**Version:** 1.0  
**Date:** 2026-10-07  
**Status:** AWAITING USER APPROVAL — do not execute  
**Prepared by:** Antigravity analytical engine  

---

## 1. Phase 6 Objective

Phase 6 strengthens the evidence base established in Phases 4 and 5 by applying rigorous statistical methods to the most analytically important existing findings.

**The objective is not to generate new analytical questions.** It is to test whether the patterns already observed and described — gender gaps, education gradients, rural–urban divergence, state variation, enterprise structure differences, and temporal trends — are statistically robust and quantifiable in terms of effect size.

The central research question is:

> *How do labour-market outcomes vary across Indian states, gender, education, and rural–urban contexts, and how are these patterns associated with the structure of employment?*

Statistical testing should directly serve this question by establishing:

1. Whether observed group differences exceed what would be expected from random sampling variation.
2. The magnitude of those differences (effect size).
3. The uncertainty around estimated values (confidence intervals).
4. Whether temporal trends are systematic or driven by year-to-year noise.

Phase 6 does **not** establish causation. All findings remain observational and descriptive.

---

## 2. Existing Analytical Work Reviewed

### 2.1 Dataset 1 — Phases 4 and 5

The following completed analyses were reviewed as inputs to this plan:

| Question block | Content | Source |
|---|---|---|
| Q1–Q4 | National-level female LFPR, WPR, Unemployment Rate overview | Phase 4 scripts + outputs |
| Q5–Q9 | State-level variation in female LFPR, WPR, Unemployment Rate; state clustering | Phase 4 scripts + outputs |
| Q10–Q12 | State × Area_Type: LFPR, WPR, Unemployment Rate | Phase 4 scripts + outputs |
| Q13 | State × Area: change 2017–2023 | Phase 4 script |
| Q14–Q17 | State × Education: LFPR, WPR, Unemployment Rate, change | Phase 4 scripts + outputs |
| Q18–Q20 | Female vs Male LFPR/WPR/UR by Education (national, Rural+Urban) | Q18-Q26 methodological specification |
| Q21 | Gender differences: Rural vs Urban, all three indicators | Q18-Q26 spec |
| Q22–Q24 | Women's LFPR/WPR/UR trend 2017–2023 | Q18-Q26 spec |
| Q25 | Education group changes 2017–2023 | Q18-Q26 spec |
| Q26 | Rural vs Urban temporal patterns (women) | Q18-Q26 spec |

**Key observed patterns** (from reusable layer inspection):
- Female LFPR national mean rose from **25.8% (2017) to 45.0% (2023)** — a 19.2 pp increase.
- Gender gap (Female − Male LFPR): mean **−41.3 pp** across all 251 State × Year observations; all 251 pairs show F < M.
- State variation in female LFPR (Rural+Urban, All edu): range **13.1%–63.1%**, SD **13.3 pp** (2023).
- Rural vs Urban female LFPR gap: widened from **+4.7 pp (2017)** to **+19.8 pp (2023)** — Rural higher than Urban throughout.
- Education gradient (non-monotone): LFPR dips at Secondary and Higher Secondary, rises sharply for Diploma/PG levels.

### 2.2 Dataset 2 — Phase 4

| Question block | Content |
|---|---|
| Q27 | Women's employment distribution across Industry Division Types |
| Q28 | Enterprise type distribution (all genders); gender × enterprise gap |
| Q29 | Rural vs Urban enterprise participation (women) |
| Q30 | Women's enterprise participation: multi-dimensional |
| Q31 | Female vs Male enterprise pattern across industry × enterprise |
| Q32 | Enterprise temporal change 2017–2023; industry temporal coverage |

**Key observed patterns:**
- Enterprise structure is dominated by Proprietary and Partnership (~59% overall) and Govt./Public Sector (~23%).
- Female–Male gaps by enterprise: Female > Male in Govt./Public Sector (+11.1 pp); Female < Male in Proprietary and Partnership (−13.0 pp).
- Proprietary/Partnership share increased 2017→2023 (+8.97 pp); Govt. share declined (−5.72 pp).
- Only 2 broad industry groupings available; `(014, 016, 017, 02-99)` absent 2022–2023 — limits industry temporal testing.
- The aggregated enterprise-type mean converges to ~12.5% due to enterprise-share summation — this is a data structure property, not a substantive finding.

### 2.3 Phase 4 analytical flag

The Phase 4 EDA summary explicitly flagged the following for Phase 6:
- State differences (Q5–Q9) — statistical significance?
- Education-level trends (Q14–Q17) — differ significantly over time?
- Gender gap robustness across education and area (Q18–Q21)
- Rural–urban changes significance (Q26)
- Gender patterns by enterprise type (Q31)

---

## 3. Analytical Principles for Phase 6

### 3.1 Unit-of-analysis discipline

Dataset 1 grain: `State × Year × Gender × Area_Type × Education`.

This means most state-level analyses involve **36 states** observed across **7 years**, giving repeated observations per state. The unit of analysis must be chosen carefully for each test:

- For **cross-sectional state comparisons** at a single year: unit = state (n ≤ 36 per group).
- For **paired gender comparisons** (Female vs Male within the same State × Year cell): unit = State × Year pair (n ≤ 252 after merging).
- For **temporal trend tests**: unit = Year-level aggregate (n = 7 time points).
- For **education gradient tests**: observations per education group = 251 (State × Year cells).

Repeated-state observations across years introduce **temporal dependence** and **within-state correlation**. This must be accounted for in every group-comparison test that pools across years.

### 3.2 Aggregation constraint

No population weights exist in Dataset 1. All collapsed means are **unweighted analytical means**. No test result should be described as a population-weighted estimate.

### 3.3 Distributional assumptions

For each test, normality should be assessed using the Shapiro–Wilk test (for small samples, n ≤ 36) or visual inspection. Given the relatively small number of states (n = 36), non-parametric equivalents are preferred as primary choices where distributional assumptions are uncertain.

### 3.4 Multiple-testing strategy

See Section 8 for the full multiple-testing framework. The minimum set of tests has been selected. Tests are classified as PRIMARY, SECONDARY, or EXPLORATORY. Corrections are applied only within families of tests that share the same confirmatory inference.

---

## 4. Dataset 1 — Analytical Findings Selected for Statistical Testing

The following existing Phase 4 and Phase 5 findings have been selected for statistical testing. Selection criteria: the finding must (a) appear in completed EDA outputs, (b) involve a comparison or temporal pattern of substantive diagnostic importance, and (c) be testable given the data structure without violating the unit-of-analysis or repeated-observation constraints.

### 4.1 Gender gap in LFPR (national, all states)

**From:** Q18, Q21, Q22  
**Observed:** Female LFPR consistently and substantially below Male LFPR across all 251 State × Year pairs. Mean gap −41.3 pp, SD 13.1 pp.  
**Statistical question:** Is the female–male LFPR gap statistically different from zero? Is it consistent across states?

### 4.2 Female LFPR temporal trend 2017–2023 (national)

**From:** Q22, Q8  
**Observed:** National female LFPR (State mean) rose monotonically from 25.8% (2017) to 45.0% (2023).  
**Statistical question:** Is the temporal trend in female LFPR statistically systematic (non-random)?

### 4.3 State variation in female LFPR

**From:** Q5, Q9  
**Observed:** Female LFPR ranges from 13.1% to 63.1% across states (SD = 13.3 pp in 2023).  
**Statistical question:** Does female LFPR differ significantly across states?

### 4.4 Rural vs Urban female LFPR divergence over time

**From:** Q26, Q10  
**Observed:** Rural > Urban female LFPR in every year; gap widened from 4.7 pp (2017) to 19.8 pp (2023).  
**Statistical question:** Is the Rural–Urban female LFPR gap statistically significant? Has it changed significantly over the period?

### 4.5 Education gradient in female LFPR

**From:** Q14, Q18, Q25  
**Observed:** Non-monotone education gradient — LFPR dips at Secondary/Higher Secondary, high at Diploma and Post Graduate levels.  
**Statistical question:** Do female LFPR values differ significantly across education groups?

### 4.6 Female WPR trend 2017–2023

**From:** Q23, Q13  
**Observed:** Female WPR (Rural+Urban, All edu) rose from 23.0% (2017) to 42.5% (2023).  
**Statistical question:** Is the female WPR temporal trend statistically systematic?

### 4.7 Female vs Male WPR and Unemployment Rate gaps

**From:** Q19, Q20, Q21  
**Observed:** Female WPR consistently below Male; Unemployment Rate patterns differ.  
**Statistical question:** Are these gaps statistically robust across the State × Year panel?

---

## 5. Dataset 2 — Analytical Findings Selected for Statistical Testing

### 5.1 Female vs Male enterprise participation gap

**From:** Q28-C, Q31-C  
**Observed:** Female > Male in Govt./Public Sector (+11.1 pp); Female < Male in Proprietary and Partnership (−13.0 pp).  
**Statistical question:** Do enterprise-type participation rates differ significantly between females and males?

### 5.2 Enterprise temporal trend 2017–2023

**From:** Q32-A  
**Observed:** Proprietary/Partnership share increased +8.97 pp; Govt. share declined −5.72 pp; Others declined −4.93 pp.  
**Statistical question:** Are these enterprise-level temporal trends statistically systematic?

### 5.3 Enterprise-type variation across states

**From:** Q28, Q30  
**Observed:** Substantial variation in Percentage_Engaged across enterprise types (sd = 17.28 for Proprietary).  
**Statistical question:** Do participation rates differ significantly across enterprise types?

---

## 6. Statistical Analysis Matrix

> [!IMPORTANT]
> All tests must use `outputs/phase_4_eda/dataset_1_reusable_analytical.csv` and `outputs/phase_4_eda/dataset_2_reusable_analytical.csv` as the only data sources. No test should access raw data, feature-engineered files, or diagnostic outputs.

| ID | Existing Question / Finding | Dataset | Indicator | Dimensions | Comparison / Relationship | Unit of Analysis | Recommended Method | Why Appropriate | Key Assumptions | Assumptions Checkable? | Effect Size | Confidence Interval | Priority | Limitations |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S1** | Gender gap in LFPR (Q18, Q21, Q22) | D1 | LFPR | Gender × [State × Year collapsed] | Female vs Male within same State × Year | State × Year pair (n = 251 matched pairs) | **Wilcoxon signed-rank test** (paired) | Paired design exploits within-State×Year matching; non-parametric avoids normality assumption for n = 36 states; gap is one-directional (all pairs F < M) | Pairs are matched on State × Year; independence across state-year pairs is an approximation given temporal structure | Partially — normality of gap distribution checkable; full independence not achievable | **Median absolute gap** (pp) + median gap with 95% CI via bootstrap | Yes (bootstrap CI on median gap) | **PRIMARY** | Temporal dependence across years within same state; unweighted means; not a population-weighted test |
| **S2** | Female LFPR temporal trend 2017–2023 (Q22, Q8) | D1 | LFPR | Year | Monotonic increasing trend in national mean | Year (n = 7 time points) | **Mann-Kendall trend test** | Designed for monotonic trend in time series; non-parametric; does not require normality; appropriate for small n time series (n = 7) | Observations are independent year means (state-collapsed); no serial autocorrelation required | Partially — serial correlation in annual means should be checked; n = 7 is very small | **Kendall's τ** (−1 to +1 scale) + **Sen's slope** (pp per year) | Yes (Sen's slope with CI) | **PRIMARY** | Only 7 time points — low power; state-collapsing discards within-state variation; unweighted mean |
| **S3** | State variation in female LFPR (Q5, Q9) | D1 | LFPR | State × Year | Differences across 36 states | State (using single-year cross-section; test repeated for 2017 and 2023 separately) | **Kruskal-Wallis H test** (non-parametric one-way ANOVA equivalent) | 36 groups (states); non-parametric suitable given unknown distributional form; appropriate when groups have ≥ 5 observations each | Observations within each state group are independent (states are the groups); homogeneity of variance is not required | Yes — group sizes are fixed at 7 years per state (n = 7 per group); normality of group distributions checkable | **η² (eta squared)** derived from H statistic as effect size for overall test; **IQR and range** to quantify spread | Not standard for Kruskal-Wallis overall; pairwise CIs if post-hoc needed | **PRIMARY** | Small within-group n (7 per state); temporal dependence across years within a state; unweighted mean |
| **S4** | Rural vs Urban female LFPR gap (Q26, Q10) | D1 | LFPR | Area_Type × Year × State | Rural − Urban gap per State × Year; gap trend over time | State × Year pair (n matched Rural–Urban pairs per year; n = 36 per year × 7 years = up to 252 pairs) | **Wilcoxon signed-rank test** (paired, per year endpoint) + **Mann-Kendall** on annual mean gap series | Paired design (same state, Rural vs Urban in same year); Mann-Kendall for trend in gap magnitude | Rural and Urban are observed independently per state × year combination | Partially — independence of states is reasonable; temporal independence across years is an approximation | **Median Rural–Urban gap** (pp) with bootstrap CI; **Sen's slope** for gap trend | Yes (bootstrap CI; Sen's slope CI) | **PRIMARY** | Unweighted means; Rural has 24 fewer rows (structural source absence); n = 7 for trend test is very small |
| **S5** | Education gradient in female LFPR (Q14, Q18, Q25) | D1 | LFPR | Education (8 categories) × State × Year | Differences across 8 education groups | State × Year cell within each education group (n = 251 per group) | **Kruskal-Wallis H test** across 8 education groups | Non-parametric; appropriate for comparing distributions across multiple groups; avoids normality assumption; n = 251 per group gives adequate power | Independence of observations within groups; education groups are defined categories, not random samples | Yes — normality of each group distribution checkable; within-group independence requires ignoring within-state temporal correlation | **η²** derived from H + pairwise effect sizes (median differences between key education pairs) | Yes — CI on pairwise median differences if post-hoc conducted | **PRIMARY** | Non-monotone gradient — education categories are nominal not ordinal for statistical purposes; temporal correlation within state-education cells ignored; unweighted mean |
| **S6** | Female WPR temporal trend 2017–2023 (Q23, Q13) | D1 | WPR | Year | Monotonic trend in national female WPR mean | Year (n = 7 time points) | **Mann-Kendall trend test** | Same rationale as S2 | Same as S2 | Same as S2 | **Kendall's τ** + **Sen's slope** (pp per year) | Yes (Sen's slope CI) | **SECONDARY** | Same as S2; WPR and LFPR trends are correlated — results interpreted jointly |
| **S7** | Female Unemployment Rate trend (Q24) | D1 | Unemployment_Rate | Year | Monotonic or directional trend in female UR mean | Year (n = 7 time points) | **Mann-Kendall trend test** | Same rationale as S2 | Same as S2 | Same as S2 | **Kendall's τ** + **Sen's slope** | Yes | **SECONDARY** | Unemployment Rate has different missingness pattern; low values may make trends harder to detect |
| **S8** | Female vs Male WPR gap (Q19, Q21) | D1 | WPR | Gender × [State × Year] | Female − Male WPR within State × Year | State × Year pair (n = 251 matched pairs) | **Wilcoxon signed-rank test** (paired) | Same rationale as S1 | Same as S1 | Same as S1 | **Median gap** (pp) + bootstrap CI | Yes | **SECONDARY** | Same as S1; WPR and LFPR gaps interpreted jointly to avoid redundancy |
| **S9** | Education × Year interaction: change 2017–2023 across education groups (Q25) | D1 | LFPR, WPR | Education × Year endpoint (2017 vs 2023) | Whether LFPR change 2017–2023 differs across education groups | State as unit of replication for each education × year cell (n = 36 per cell) | **Wilcoxon signed-rank test** per education group (paired: 2017 vs 2023 per state) applied within each group; **Friedman test** across groups at each year | Paired design exploits same-state matching; Friedman tests whether 2017→2023 change is uniform or education-group-specific | Paired matching on State; independence across education groups is approximate | Yes — normality checkable; multiple tests require correction | **Median absolute change** (pp per group) + rank correlation between change magnitude and education level | Yes | **SECONDARY** | Multiple-testing: 8 education groups × 2 endpoints = 16 paired tests — correction required; n = 36 per cell |
| **S10** | Enterprise participation variation across types (Q28, D2) | D2 | Percentage_Engaged | Enterprise_Type | Differences across 8 enterprise types | State × Year × Gender cell within enterprise type (n = 1,295 per type for Female) | **Kruskal-Wallis H test** across 8 enterprise types | Large n per group (n = 1,295); non-parametric appropriate given right-skewed distribution (range 0–100%); enterprise types are categories | Independence of observations within groups is an approximation — repeated state observations exist | Partially — enterprise-type independence is definitional; within-state correlation ignored | **η²** from H statistic + pairwise median differences for key pairs | Yes — bootstrap CI on pairwise medians | **PRIMARY** | Enterprise-share structure means values sum to ~100% per combination — observations are not fully independent; the test assesses whether enterprise type explains variance in Percentage_Engaged |
| **S11** | Female vs Male enterprise participation gap (Q31-C, Q28-C) | D2 | Percentage_Engaged | Gender × Enterprise_Type | Female − Male gap per enterprise type | State × Year pair within enterprise type (matched Female–Male on State × Year × Enterprise) | **Wilcoxon signed-rank test** per enterprise type (paired) — applied to the 8 most important types | Non-parametric paired test; matches Female and Male observations from same State × Year × Enterprise combination | Pairs matched on State × Year × Enterprise; enterprise-share structure means pairs are not independent across enterprise types within a combination | Partially — normality checkable per enterprise type | **Median Female–Male gap** (pp) per enterprise type + bootstrap CI | Yes | **PRIMARY** | Enterprise shares sum to ~100% within State × Year combination — Female/Male values are not independent across enterprise types; multiple tests (8 enterprise types) require Bonferroni or FDR correction |
| **S12** | Enterprise participation temporal trend 2017–2023 (Q32-A) | D2 | Percentage_Engaged | Enterprise_Type × Year | Monotonic trend in annual mean per enterprise type | Year (n = 7 time points) per enterprise type | **Mann-Kendall trend test** per enterprise type | Same rationale as S2; applied per enterprise type separately | Annual means are based on collapsing states | Partially — serial correlation in annual means checkable | **Kendall's τ** + **Sen's slope** per enterprise type | Yes | **SECONDARY** | Multiple tests (8 enterprise types) — correction required; `(014, 016, 017, 02-99)` absent 2022–2023 limits industry-stratified temporal analysis; n = 7 time points |

---

## 7. Analyses NOT Recommended for Statistical Testing

The following potential analyses were considered and explicitly rejected. Reasons are documented.

| Analysis | Reason not recommended |
|---|---|
| **State-pair comparisons** (e.g. testing whether State A > State B) | Would produce C(36,2) = 630 pairwise tests. Creates an unmanageable multiple-testing problem. State-level variation is already captured by S3 (Kruskal-Wallis overall test). |
| **Gender × Area × Education triple interaction** | Combines Q18, Q21, and Q25 into a three-way interaction. With unweighted means and no population weights, this would produce an unstable estimate with very small cell sizes per combination. |
| **Q27 — Industry Division Type LFPR distribution test** | Only 2 industry categories present, both with mean ~12.5% (enterprise-share summation artefact). No substantive industry comparison is possible from a statistical perspective. |
| **Q29 — Rural vs Urban enterprise gap test at industry level** | The ~12.5% artefact identified in Phase 4 EDA means that Rural vs Urban differences at the industry level are not substantively informative. Enterprise-level Rural–Urban differences (within the enterprise-level test S11) are more meaningful. |
| **Unemployment Rate state-level variation test** | Phase 4 noted that Unemployment Rate has different missingness patterns and very different distributional properties than LFPR/WPR. Adding a third Kruskal-Wallis on state variation for UR would be largely redundant with S3 and adds to multiple-testing burden. Deferred to exploratory. |
| **Education × Gender interaction test** | The Phase 4 Q18 finding (female LFPR by education) is captured in S5 (education gradient) and S9 (change over time). Adding a formal interaction test would require a factorial design with the repeated-state complication and insufficient within-cell n. |
| **Temporal test for `(014, 016, 017, 02-99)` industry type** | Structurally absent 2022–2023. Only 5 time points available (2017–2021). Too few for meaningful trend detection. Not recommended. |
| **State-level enterprise participation variation** | Would mirror S10 but disaggregated by state. 36 × 8 = 288 cells with repeated observations. Enterprise-share summation further complicates interpretation. Deferred. |
| **Q4, Q9, Q30** | Flagged in Phase 4 EDA summary as "not meaningfully analysable." Phase 6 respects this flag. |

---

## 8. Multiple-Testing Strategy

### 8.1 Test families

Tests are grouped into families based on shared inference scope. Correction applies within families, not across the entire plan.

| Family | Tests | Scope | Correction method |
|---|---|---|---|
| **F1 — Primary gender gap** | S1, S8 | LFPR and WPR paired gender gap | None needed (only 2 tests; both expected significant; directional hypothesis) |
| **F2 — Temporal trends** | S2, S6, S7 | LFPR, WPR, UR trends for females | **Bonferroni** (α/3 = 0.017 per test); three related trend tests on the same unit |
| **F3 — State variation** | S3 | Kruskal-Wallis on state LFPR | Single test; no correction needed |
| **F4 — Rural–Urban gap** | S4 | Paired Rural–Urban test + trend | Two related tests; **Bonferroni** (α/2 = 0.025) |
| **F5 — Education gradient** | S5, S9 | 8-group education test + 8 pairwise change tests | Kruskal-Wallis (S5) as omnibus test; if post-hoc required, use **Dunn's test with Benjamini-Hochberg (FDR) correction** for pairwise comparisons; S9 also uses **Bonferroni** across 8 education groups |
| **F6 — Enterprise structure** | S10, S11, S12 | Enterprise type variation, gender gap, trend | S10: omnibus single test. S11: 8 enterprise types — **Bonferroni** (α/8 = 0.00625). S12: 8 enterprise trend tests — **Bonferroni** (α/8 = 0.00625) |

### 8.2 Significance threshold

- Primary significance level: **α = 0.05** (two-tailed unless a directional hypothesis is stated)
- Directional hypotheses (one-tailed): S1, S4 (Female < Male; Rural > Urban female LFPR) — permitted where the direction is established by all 251 paired observations.
- All p-values reported to 3 decimal places; p < 0.001 reported as such.

### 8.3 Hierarchy

- PRIMARY tests (S1, S2, S3, S4, S5, S10, S11): interpret without needing secondary tests to confirm.
- SECONDARY tests (S6, S7, S8, S9, S12): interpreted as corroborating evidence; not primary claims.
- Any post-hoc pairwise comparisons are EXPLORATORY by default.

---

## 9. Repeated-Observation Considerations

Dataset 1 contains **repeated measurements** over 7 years for the same 36 states. This has the following implications:

| Test | Repeated-observation issue | Mitigation |
|---|---|---|
| S1 (gender gap) | State-year pairs are repeated across years within the same state — not fully independent | State × Year pairs are treated as the unit; within-state correlation across years is acknowledged as a limitation. A robustness check using only the 2023 cross-section (n = 36) is recommended. |
| S2, S6, S7 (trends) | Annual means collapse within-state variation; only 7 time points | Mann-Kendall is appropriate for short non-independent time series; Sen's slope CI accounts for serial dependence approximately |
| S3 (state variation) | 7 observations per state across years introduce within-state temporal correlation | Recommended: **use a single representative year (2023) for primary state comparison**; repeat for 2017 as a sensitivity check. This eliminates the temporal dependence issue within the Kruskal-Wallis |
| S4 (rural-urban) | Same-state repeated across 7 years | Same approach as S1: treat State × Year pair as unit; note limitation; robustness check with single-year comparison |
| S5 (education) | n = 251 per education group includes 7 years per state | High n reduces concern about power; within-group temporal correlation is a limitation; robustness check with single-year cross-section recommended |
| S9 (education change) | Paired 2017 vs 2023 per state — clean paired design, but only 2 endpoints | Paired design is appropriate; n = 36 per group |
| S10–S12 (enterprise) | n = 1,295 per enterprise type includes State × Year × Gender repetitions | High n; acknowledge non-independence of enterprise shares within State × Year combinations |

---

## 10. Missing-Value and Structural-Missingness Treatment

| Dataset | Missing-value pattern | Treatment in Phase 6 |
|---|---|---|
| Dataset 1 | 30 missing values per indicator (0.1%) — all in Year = 2023, Area = Rural | Exclude from calculations; do not impute; note n reduction in affected tests (tests using Rural area in 2023 will have n < 36 per state) |
| Dataset 2 | `(014, 016, 017, 02-99)` absent in 2022–2023 (structural) | Do not impute; do not interpolate; temporal tests on this industry type are limited to 2017–2021 and are not recommended for S12; note explicitly in results |
| Dataset 2 | 3 missing State × Year × Gender × Area combinations for Rural | Treat as missing; exclude from rural-area enterprise tests |

**Never replace structural absence with zero.** All zero values in the source data are valid observations.

---

## 11. Recommended Execution Sequence for Phase 6

The recommended execution sequence minimises repeated computation and allows each result to inform subsequent tests:

```
Step 1 — Assumption checks
│   ├── Shapiro-Wilk normality test per group (small n groups)
│   ├── Serial correlation check for annual means (S2, S6, S7, S12)
│   └── Visual distribution checks (histograms, Q-Q plots via text output)

Step 2 — PRIMARY tests (Dataset 1)
│   ├── S1: Wilcoxon signed-rank — gender gap in LFPR
│   ├── S2: Mann-Kendall + Sen's slope — female LFPR trend
│   ├── S3: Kruskal-Wallis — state variation in female LFPR (2023 cross-section + 2017 sensitivity)
│   ├── S4: Wilcoxon signed-rank (paired) + Mann-Kendall — rural-urban gap and trend
│   └── S5: Kruskal-Wallis — education gradient in female LFPR

Step 3 — PRIMARY tests (Dataset 2)
│   ├── S10: Kruskal-Wallis — enterprise type variation (Female)
│   └── S11: Wilcoxon signed-rank per enterprise type — Female vs Male gaps

Step 4 — SECONDARY tests
│   ├── S6: Mann-Kendall — female WPR trend
│   ├── S7: Mann-Kendall — female UR trend
│   ├── S8: Wilcoxon signed-rank — gender gap in WPR
│   ├── S9: Paired Wilcoxon + Friedman — education change 2017-2023
│   └── S12: Mann-Kendall per enterprise type — enterprise temporal trends

Step 5 — Post-hoc (only if omnibus tests reach significance)
│   ├── Dunn's test with BH correction — education pairwise comparisons (after S5)
│   └── Enterprise pairwise medians — after S10

Step 6 — Robustness checks
│   ├── Repeat S1, S4 using single-year (2023) cross-section
│   └── Repeat S3 for 2017 cross-section
```

---

## 12. Expected Statistical Outputs

Upon execution (not yet started), Phase 6 is expected to produce the following outputs in `outputs/phase_6_statistical_analysis/`:

| Output file | Content |
|---|---|
| `phase_6_assumption_checks.md` | Normality test results, distribution summaries, serial correlation diagnostics |
| `phase_6_primary_results.md` | Results for S1–S5, S10–S11: test statistics, p-values, effect sizes, CIs |
| `phase_6_secondary_results.md` | Results for S6–S9, S12 |
| `phase_6_statistical_summary.md` | Consolidated interpretation of all tests; how results strengthen the diagnostic |

**No Q-specific CSVs will be created.** All results will be documented in markdown reports. No source files will be modified.

---

## 13. Rationale Summary

The twelve proposed tests address the following diagnostic questions:

| Test | Diagnostic question answered |
|---|---|
| S1 | Is the female–male labour-force participation gap real and consistent across India's states? |
| S2 | Is the dramatic rise in female LFPR (2017→2023) a systematic trend or artefact? |
| S3 | Does female LFPR genuinely vary across states, or is the apparent spread within sampling noise? |
| S4 | Has the Rural–Urban divergence in female participation widened significantly, and is Rural consistently higher? |
| S5 | Does education level genuinely differentiate women's labour force participation? |
| S6 | Is the female WPR increase temporally systematic? |
| S7 | Does the female unemployment rate exhibit a directional trend? |
| S8 | Is the female–male WPR gap statistically robust? |
| S9 | Has the education-level change in female participation been uniform, or has one group moved more? |
| S10 | Does enterprise type genuinely explain variance in female participation rates? |
| S11 | Are female–male enterprise participation gaps statistically significant across enterprise types? |
| S12 | Have individual enterprise types experienced statistically systematic shifts 2017–2023? |

---

## 14. Known Methodological Concerns

> [!WARNING]
> **Unweighted means:** All tests on Dataset 1 use unweighted state-level means. Results reflect the average experience across states, not the average experience of the Indian population. Large states (UP, Maharashtra) receive the same weight as small states (Goa, Lakshadweep). This is a fundamental limitation that cannot be resolved without population weights not present in the source data.

> [!WARNING]
> **Enterprise-share constraint (Dataset 2):** Percentage_Engaged values within a State × Year × Gender × Industry combination sum to approximately 100% across enterprise types. This means the 8 enterprise-type observations within any single combination are compositional, not independent. Tests S10 and S11 treat enterprise types as categories and test whether enterprise type explains between-combination variance — this is appropriate but must be stated explicitly in interpretation.

> [!NOTE]
> **Small n for trend tests:** Mann-Kendall tests (S2, S6, S7, S12) are applied to n = 7 annual time points. This gives very low statistical power for detecting anything other than a near-monotonic trend. The large magnitude of the observed trend (+19.2 pp in female LFPR) provides high practical confidence; the statistical test formalises this but cannot compensate for n = 7.

> [!NOTE]
> **Cross-sectional vs panel design:** A full panel model (e.g. fixed-effects regression) would better handle the repeated-observation structure of Dataset 1. Such models are not proposed here because they belong to Phase 7 (Machine Learning / Predictive Analysis) and would require regression infrastructure not yet established. Phase 6 confines itself to non-parametric tests appropriate for the available infrastructure.

---

*Plan prepared 2026-10-07. Awaiting user review and approval before any statistical test is executed.*
