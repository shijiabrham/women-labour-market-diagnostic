# Phase 6 Finding Review
## Women's Labour Market Diagnostic in India

**Version:** 1.0  
**Date:** 2026-10-07  
**Status:** AWAITING USER REVIEW — no statistical tests have been executed  

---

## 1. Purpose

This document identifies the most important empirical findings emerging from the completed Phase 4 and Phase 5 analysis of the Women's Labour Market Diagnostic in India. For each finding, it assesses whether statistical validation would materially strengthen the evidence, whether descriptive analysis alone is sufficient, or whether data structure and methodological constraints make inferential testing inappropriate.

The document is **finding-driven**. Findings were identified by reviewing the actual analytical results from the reusable analytical layers, Phase 4 EDA outputs, Phase 5 comparative outputs, and the insight and narrative frameworks already built. Q1–Q32 were guiding analytical questions used to produce those results, not the organising framework for Phase 6.

No statistical tests have been conducted. No new CSVs have been created. No existing analytical files have been modified.

---

## 2. Key Empirical Findings

The following table documents all important empirical findings identified from the completed analysis.

| Finding ID | Dataset | Empirical Finding | Evidence from Existing Analysis | Dimensions Involved | Analytical Unit | Magnitude / Pattern | Validation Assessment | Reason |
|---|---|---|---|---|---|---|---|---|
| **F1** | D1 | Female LFPR rose substantially from 2017 to 2023 at the national level | State-mean female LFPR (Rural+Urban, All education) rose from 25.8% (2017) to 45.0% (2023) — a 19.2 pp increase. Increase apparent in every year 2017→2022; slight dip 2020–2021 then continuing rise. WPR rose in parallel (+19.5 pp). | Gender=Female, Area=Rural+Urban, Education=All, Year | Year-level state means (n=7 annual means, each based on 36 states) | +19.2 pp LFPR; +19.5 pp WPR; near-monotonic | **RECOMMENDED** | The trend direction is clear descriptively, but formally testing whether the increase is statistically systematic (rather than year-to-year fluctuation) would add inferential weight to the most headline finding of the diagnostic |
| **F2** | D1 | Female LFPR is substantially lower than male LFPR in every state and every year | All 252 State × Year paired observations show Female < Male. Mean gap: −41.3 pp (SD 13.1 pp). Gap narrowed from −49.5 pp (2017) to −33.1 pp (2023) but remains the dominant feature of the data | Gender, Area=Rural+Urban, Education=All, Year, State | State × Year pairs (n=252 matched female–male pairs) | Gap range: −69.8 pp to −2.8 pp. All 36 states show Female < Male in 2023 (range −57.6 pp to −10.5 pp) | **RECOMMENDED** | The direction is universal; statistical validation would formalise the magnitude and its narrowing over time. The paired within-state design makes this the most structurally clean test in the dataset |
| **F3** | D1 | Female LFPR varies substantially across Indian states | In 2023: min 17.1% (Lakshadweep), max 71.8% (Meghalaya), SD 13.3 pp, range 54.7 pp. CV = 29.6% — high relative dispersion even after the national rise. In 2017 CV was 44.8%. State dispersion has narrowed but remains wide | Gender=Female, Area=Rural+Urban, Education=All, Year=2023 (cross-section) | State (n=36 per year) | Range 54.7 pp in 2023; SD 13.3 pp. Male LFPR SD=4.7 pp by contrast — female dispersion ~3× male | **RECOMMENDED** | State variation is a central diagnostic question. A formal test of whether the observed between-state variation is non-random would support the claim that state context matters. The contrast with male dispersion is itself analytically important |
| **F4** | D1 | Rural female LFPR is consistently higher than urban female LFPR, and the gap has widened substantially | Rural-Urban gap (Rural − Urban) in female LFPR: 4.7 pp in 2017 → 19.8 pp in 2023. Rural > Urban in all 7 years. Across 35 states in 2023: 33 show Rural > Urban; 2 show Urban > Rural | Gender=Female, Education=All, Area=Rural vs Urban, Year | State × Year pairs (Rural vs Urban per state per year, n≤252 pairs) | Gap widened from 4.7 pp to 19.8 pp. State-level SD of the gap (2023) = 12.0 pp | **RECOMMENDED** | Both the direction and the widening are analytically important. Statistical validation would address whether the gap increase is systematic vs driven by a few states, and whether the Rural > Urban direction is consistent across states |
| **F5** | D1 | Female LFPR shows a non-monotone relationship with education level | LFPR dips at Secondary (31.3%) and Higher Secondary (31.6%), well below Not Literate (46.4%) and Literate/Primary (50.4%). Then rises sharply at Diploma (68.3%) and Post Graduate (63.4%). Pattern is present across all years (2017–2023) | Gender=Female, Area=Rural+Urban, Education (8 detailed categories), Year | Education group (8 groups, n=251 State × Year obs per group) | LFPR range across groups: 23.7%–68.3%. The Secondary/Higher Secondary dip is ~20–25 pp below Diploma and PG levels | **RECOMMENDED** | The non-monotone pattern is surprising and diagnostically important — it challenges a simple "more education = more participation" narrative. Testing whether the differences across education groups are statistically robust would strengthen this finding |
| **F6** | D1 | Female unemployment rate is substantially higher than male at higher education levels | At Graduate level: Female UR = 25.5%, Male UR = 13.4% (gap +12.0 pp). At PG level: Female 22.7%, Male 10.2% (gap +12.5 pp). At Not Literate: Female UR = 0.3%, Male UR = 1.0% (female lower). The pattern reverses sharply above Secondary | Gender=Female+Male, Area=Rural+Urban, Education (detailed), Year | Education group × Gender (n=251 per group) | Female-Male UR gap at Graduate level: +12.0 pp; at PG: +12.5 pp. At Not Literate: −0.70 pp (Female lower) | **RECOMMENDED** | This is a distinctive labour-market feature — educated women face higher unemployment than educated men. Statistical validation of the gender × education interaction in unemployment would provide evidence for the 'educated women unemployment trap' pattern |
| **F7** | D1 | Female state-level variation substantially exceeds male state-level variation | Female LFPR CV = 44.8% (2017), 29.6% (2023). Male LFPR CV = 5.7% (2017), 6.1% (2023). Female dispersion across states is roughly 5–8× that of males | Gender=Female+Male, Area=Rural+Urban, Education=All, Year | State (n=36 per year) | Female SD=13.3 pp, Male SD=4.7 pp in 2023. The differential dispersion is consistent in both years | **RECOMMENDED** | This is not merely a descriptive point — it suggests that state-level contextual factors affect women's participation far more than men's, which is a central theme of the diagnostic. Formal testing of whether female variance exceeds male variance would support this |
| **F8** | D1 | Female LFPR gains (2017–2023) were larger among lower-educated women than higher-educated | Not Literate: +20.5 pp; Literate/Primary: +24.6 pp; Middle: +21.6 pp; Secondary: +14.4 pp; Higher Secondary: +12.0 pp; Diploma: +13.5 pp; Graduate: +9.9 pp; PG: +6.1 pp. Larger absolute gains at lower and middle education levels | Gender=Female, Area=Rural+Urban, Education (8 groups), Year 2017 vs 2023 | Education group (n=36 state observations at each endpoint per group) | Change range: +6.1 pp (PG) to +24.6 pp (Literate/Primary). Pattern consistent across most groups | **RECOMMENDED** | Whether the differential in gains across education levels is statistically reliable, or whether it merely reflects sampling variation across states, would materially affect interpretation of the convergence / divergence story |
| **F9** | D1 | Unemployed female graduate pool is large and highly variable across states | Female Graduate UR (2023, Rural+Urban): mean=23.3%, SD=14.3%, range=4.8%–63.1%. High educated female unemployment is both nationally elevated and highly state-variable | Gender=Female, Education=Graduate, Area=Rural+Urban, Year=2023 | State (n=36) | SD=14.3 pp; range 58.3 pp. This exceeds the overall female LFPR range in scale terms | **DESCRIPTIVE SUFFICIENT** | The descriptive picture is already clear and the state variation is itself the finding. A Kruskal-Wallis testing "are graduate UR values different across states" is trivially true given the range. More value from descriptive characterisation than formal testing at this stage |
| **F10** | D2 | Employment is heavily concentrated in Proprietary and Partnership enterprises, with the concentration increasing over time | Proprietary and Partnership share (05-99, Rural+Urban, all genders): 54.6% (2017) → 63.3% (2023), a +8.7 pp increase. Govt./Public Sector share fell from 24.8% to 19.6% (−5.2 pp). 'Others' category nearly eliminated: 6.4% → 1.4% (−5.0 pp) | Enterprise_Type, Year, Industry=(05-99), Area=Rural+Urban | Year (n=7 time points) per enterprise type | Proprietary share +8.7 pp; Govt. share −5.2 pp. Both directional across all years | **RECOMMENDED** | Whether these temporal shifts are statistically systematic trend or driven by specific years (e.g. post-Covid adjustment) would materially affect whether the shift is characterised as structural or temporary |
| **F11** | D2 | Female and male employment are differently structured across enterprise types | Female > Male in Govt./Public Sector (+12.2 pp gap, Rural+Urban, 05-99). Female < Male in Proprietary/Partnership (−14.2 pp gap). Employer's Households: Female 5.6%, Male 0.8% (+4.8 pp). Pattern consistent across most states and years | Gender=Female+Male, Enterprise_Type, Area=Rural+Urban, Industry=05-99 | Enterprise type × State × Year combinations (n=252 paired obs per enterprise type for F vs M) | Gaps range from −14.2 pp (Proprietary) to +12.2 pp (Govt.) across enterprise types. Direction consistent | **RECOMMENDED** | The gender differentiation across enterprise types is a core structural finding. Whether these gaps exceed chance variation across states and years would strengthen the structural interpretation |
| **F12** | D2 | Rural and urban female employment differ by enterprise type | Female Govt./Public Sector: Rural 33.4%, Urban 25.9% (gap +7.5 pp Rural > Urban). Female Proprietary: Rural 51.5%, Urban 48.9% (gap +2.6 pp). Public/Private Ltd: Rural 6.2%, Urban 10.5% (gap −4.3 pp, Urban higher). Employer's Households: Rural 4.2%, Urban 8.1% (−3.8 pp) | Gender=Female, Enterprise_Type, Area=Rural vs Urban, Industry=05-99 | State × Year pairs (Rural vs Urban per enterprise type) | Meaningful directional differences across all 8 enterprise types | **DESCRIPTIVE SUFFICIENT** | The rural-urban enterprise pattern is a useful contextual finding. However, the compositional constraint (values sum to ~100% within each State × Year × Gender × Industry combination) makes the rural-urban comparison within enterprise types analytically complex. Descriptive characterisation is more defensible here |
| **F13** | D1 | The female LFPR trend includes a discernible slowdown or plateau in 2020–2021 | Year-by-year female LFPR: 2019: 33.8%, 2020: 35.9%, 2021: 35.4%. A pause/dip around 2020–2021 before resumption. Male LFPR was stable (75–76% range) in the same period | Gender=Female+Male, Area=Rural+Urban, Education=All, Year | Year (n=7 time points) | 2021 LFPR (35.4%) was below 2020 (35.9%) — a reversal in the upward trend | **DESCRIPTIVE SUFFICIENT** | The pattern is visible and interpretable. Statistically testing a dip in a 7-point series adds little when the overall trend test (F1) already addresses systematic directionality. The 2020–2021 pattern is better addressed descriptively with contextual note |
| **F14** | D2 | Industry-level employment comparison is limited to two broad groupings; structural absence prevents temporal analysis for one of them | Dataset 2 has only two Industry Division Types. `(014, 016, 017, 02-99)` is structurally absent in 2022 and 2023. Only `(05-99)` has full 2017–2023 coverage | Industry_Division_Type, Year | Not applicable — structural data limitation | Single industry available for temporal analysis; two for cross-sectional (2017–2021 only) | **NOT SUITABLE** | Structural source absence in 2022–2023 prevents valid temporal testing for `(014, 016, 017, 02-99)`. Cross-industry comparison at aggregated level produces ~12.5% artefact from enterprise-share summation. No reliable industry-level statistical test is possible |

---

## 3. Findings Recommended for Statistical Validation

### F1 — National female LFPR rise 2017–2023

**What was observed:** Female LFPR (unweighted mean across 36 states, Rural+Urban, All education) rose from 25.8% to 45.0% over 7 years — a 19.2 pp increase. The year-on-year pattern is nearly monotonically increasing, with a brief plateau in 2020–2021.

**Why it matters:** This is the headline finding of the diagnostic — women entered the labour force in substantially larger numbers over this period. The diagnostic narrative rests on this being a real, directional trend rather than noise.

**What uncertainty remains:** With n = 7 annual observations, the trend is visually clear but formally untested. The 2020–2021 plateau introduces slight non-monotonicity. Whether the overall upward trajectory is statistically systematic has not been established.

**What statistical validation would add:** A formal trend test would establish whether the increase is statistically systematic and provide a quantified rate of change (magnitude per year) with uncertainty bounds. This upgrades the headline finding from descriptive to evidence-based.

---

### F2 — Persistent female–male LFPR gap

**What was observed:** Female LFPR is lower than Male LFPR in all 252 State × Year paired observations. Mean gap −41.3 pp (SD 13.1 pp). Gap is narrowing but remains the defining structural feature of the data.

**Why it matters:** The gender gap is the central equity finding. Its universality across all states and years, and its gradual narrowing, are the primary labour-market diagnostic conclusions.

**What uncertainty remains:** While the direction is universal (zero exceptions across 252 pairs), the magnitude and rate of narrowing have not been formally tested. Whether the gap is statistically distinguishable from zero is in practice not in doubt, but the rate of narrowing and confidence around the trend in the gap are not established.

**What statistical validation would add:** A paired test formalises the gap magnitude; a trend test on the annual mean gap establishes whether narrowing is systematic. These would allow the diagnostic to state the gap reduction with inferential confidence.

---

### F3 — Substantial and persistent state-level variation in female LFPR

**What was observed:** Female LFPR ranges from 17.1% to 71.8% across states in 2023. SD = 13.3 pp. CV = 29.6%. The top-bottom range (54.7 pp) is comparable in magnitude to the entire national female LFPR itself (45.0%). Male LFPR variation is far smaller (SD = 4.7 pp, CV = 6.1%).

**Why it matters:** State variation is a core diagnostic theme — it indicates that contextual factors shape women's participation far more than structural factors alone. The contrast with male variation is especially important.

**What uncertainty remains:** Whether the apparent state differences constitute genuine heterogeneity or sampling variation within a more uniform underlying distribution has not been tested. A formal test of between-state variation would establish this.

**What statistical validation would add:** An omnibus test of between-state differences would support the claim that state context genuinely matters. A formal comparison of female vs male variance would provide evidence for the differential contextual sensitivity claim.

---

### F4 — Widening Rural–Urban divergence in female LFPR

**What was observed:** Rural female LFPR exceeded Urban in all 7 years. The Rural–Urban gap widened from 4.7 pp (2017) to 19.8 pp (2023). In 2023, 33 of 35 states with data show Rural > Urban.

**Why it matters:** This is counter-intuitive in development contexts where urbanisation typically correlates with higher female participation. The widening divergence suggests that the forces driving female LFPR growth in this period were predominantly rural. This is a substantive diagnostic claim.

**What uncertainty remains:** Whether the widening gap is statistically systematic, and whether the Rural > Urban direction is consistent enough across states to generalise, has not been formally tested.

**What statistical validation would add:** Paired testing per state (Rural vs Urban) and a trend test on the annual mean gap would establish whether the directional pattern and the widening are statistically robust.

---

### F5 — Non-monotone education gradient in female LFPR

**What was observed:** Female LFPR is lower at Secondary (31.3%) and Higher Secondary (31.6%) than at Not Literate (46.4%) and Literate/Primary (50.4%). It rises sharply only at Diploma (68.3%) and Post Graduate (63.4%) levels. The dip at the secondary education level is pronounced and present across all years.

**Why it matters:** This contradicts a simple 'education raises participation' story. The secondary education dip may reflect a transition period where women with secondary qualifications have higher reservation wages or are awaiting appropriate employment opportunities. This has direct policy relevance.

**What uncertainty remains:** Whether the differences across education groups are statistically significant has not been established. The pattern is present across all 7 years, which suggests it is not an artefact, but formal testing would confirm this.

**What statistical validation would add:** An omnibus test of whether education group membership explains variance in female LFPR, followed by identification of which specific group-level differences are statistically robust.

---

### F6 — Educated women face substantially higher unemployment than educated men

**What was observed:** At Graduate level: Female UR = 25.5%, Male UR = 13.4% (Female−Male gap = +12.0 pp). At Post Graduate level: Female UR = 22.7%, Male UR = 10.2% (gap = +12.5 pp). At Not Literate level, the gap reverses (Female UR 0.3 pp below Male). This reversal of the gender unemployment pattern between low and high education levels is striking.

**Why it matters:** High educated female unemployment is both a waste of human capital and an equity concern. It suggests a structural mismatch between the supply of educated women and the types of employment available.

**What uncertainty remains:** Whether the gender unemployment gap at higher education levels is statistically distinguishable from sampling variation across states has not been confirmed.

**What statistical validation would add:** Paired testing of the Female–Male UR gap per education group would establish which parts of the education spectrum show reliable gender differences in unemployment.

---

### F7 — Female labour-market outcomes are far more state-variable than male outcomes

**What was observed:** Female LFPR CV = 44.8% (2017), 29.6% (2023) vs Male LFPR CV = 5.7% (2017), 6.1% (2023). The female state dispersion is consistently 5–8× that of males.

**Why it matters:** This is not just a description of female variation — it is a comparison that implies female participation is much more sensitive to state-level contextual factors than male participation. This supports the diagnostic theme about state context mattering for women's economic engagement.

**What statistical validation would add:** A formal comparison of female and male variance would provide inferential support for the claim that female labour-market outcomes are contextually determined in a way that male outcomes are not.

---

### F8 — Female LFPR gains 2017–2023 were larger among lower-educated women

**What was observed:** Not Literate (+20.5 pp), Literate/Primary (+24.6 pp), Middle (+21.6 pp) vs Graduate (+9.9 pp) and Post Graduate (+6.1 pp). The gains were largest among women with low to middle education.

**Why it matters:** This finding bears on the nature of the female LFPR increase — it was driven more by lower-educated women than by educated women, which has different policy implications than if the gains were concentrated at higher education levels.

**What uncertainty remains:** Whether the differential in gains across education groups exceeds what would be expected by chance (given within-state variation) has not been tested.

**What statistical validation would add:** Testing whether change magnitudes differ significantly across education groups would establish whether the differential absorption pattern is statistically reliable.

---

### F10 — Enterprise employment is shifting toward private/proprietary and away from government/public sector

**What was observed:** Proprietary and Partnership share: 54.6% (2017) → 63.3% (2023), +8.7 pp. Govt./Public Sector: 24.8% → 19.6%, −5.2 pp. 'Others' category: 6.4% → 1.4%, −5.0 pp. These are large directional shifts visible in every year.

**Why it matters:** The shift from public to private/proprietary employment has implications for job security, social protection, and the nature of work available to women and men in India.

**What uncertainty remains:** Whether the year-on-year shifts constitute a statistically systematic trend (rather than a level shift around a particular year, e.g. post-Covid) has not been tested formally.

**What statistical validation would add:** Trend testing for each enterprise type would establish which shifts are systematic and which represent episodic rather than structural change.

---

### F11 — Female and male employment are structurally differently distributed across enterprise types

**What was observed:** Female Govt./Public Sector share: 30.3%; Male: 18.1% (gap +12.2 pp). Female Proprietary share: 50.1%; Male: 64.3% (gap −14.2 pp). The direction is consistent across states and years.

**Why it matters:** This is the primary structural finding from Dataset 2 — women's employment is more concentrated in government/public sector enterprises relative to men, while men are more concentrated in private/proprietary enterprises. This structural difference has implications for stability, formality, and gender equity in employment.

**What uncertainty remains:** Whether the Female–Male gaps per enterprise type are statistically robust across the state-year observations has not been formally established.

**What statistical validation would add:** Paired testing of Female vs Male Percentage_Engaged within enterprise types would confirm which gaps are reliably above zero. This upgrades the finding from descriptive to inferential.

---

## 4. Findings Where Descriptive Evidence Is Sufficient

### F9 — Female graduate unemployment is high and variable across states

The descriptive picture is unambiguous: mean = 23.3%, range = 4.8%–63.1%, SD = 14.3%. The finding of "high and variable" is itself the finding. A formal test that states differ from each other adds no diagnostic value; the diagnostic question is about the level and variation, both of which are clearly documented. The existing EDA results are adequate for the diagnostic narrative.

### F12 — Rural and urban female employment differ by enterprise type

The rural-urban enterprise pattern (Govt. higher in Rural, Employer's Households higher in Urban) is descriptively useful context. However, the compositional constraint — that values sum to approximately 100% within each State × Year × Gender × Industry combination — means that rural-urban differences within enterprise types are not independent across enterprise types. Interpreting statistical tests on one enterprise type without conditioning on all others is misleading. Descriptive characterisation is more defensible.

### F13 — Female LFPR plateau in 2020–2021

The 2020–2021 pause is visible (2020: 35.9%, 2021: 35.4%) but minor relative to the overall 19.2 pp rise. It falls within the trajectory of the trend. Formally testing a dip of 0.5 pp in a 7-point series adds no inferential value and risks distracting from the primary trend finding (F1).

---

## 5. Findings Not Suitable for Statistical Validation

### F14 — Industry-level analysis is structurally limited

**Finding:** Only two broad industry groupings are available. `(014, 016, 017, 02-99)` is structurally absent in 2022 and 2023.

**Why not suitable:**
- Testing differences between only two categories is trivially simple and provides no useful inferential result for a diagnostic purpose.
- The aggregated enterprise-type mean when collapsed across both industry types converges to ~12.5% (a mathematical artefact of enterprise-share summation), making any industry-level comparison uninformative.
- The structural absence of one industry grouping in 2022–2023 prevents valid temporal analysis covering the full period.
- No imputation, interpolation, or estimation should be applied.

**Assessment:** The industry dimension in Dataset 2 is best used as a stratification filter (e.g. restricting to `(05-99)` for temporal analyses) rather than as a dimension of comparison in its own right.

---

## 6. Cross-Cutting Methodological Considerations

### Repeated observations and the state-year panel structure

Dataset 1 contains 36 states observed across 7 years. Any analysis that pools State × Year observations treats states as if their contributions across years are independent. They are not — the same state appears 7 times, creating within-state temporal correlation. For findings involving comparisons over time or across groups, this repeated structure must be accounted for either by:
- restricting comparisons to single-year cross-sections, or
- using the repeated structure explicitly as part of a paired/matched design (comparing within the same state across conditions), or
- acknowledging the dependence as a stated limitation.

The analysis in Phase 6 should not treat the 252 State × Year observations as 252 independent data points.

### Unweighted analytical means

Dataset 1 does not contain population weights. All collapsed means are unweighted — each state contributes equally regardless of its population. Results should be described as reflecting the average across Indian states rather than the average experience of Indian women. Large states (Uttar Pradesh, Maharashtra) carry the same weight as small states (Goa, Lakshadweep). This is a systematic limitation that cannot be resolved without externally sourced population data.

### Compositional structure in Dataset 2

Within each State × Year × Gender × Industry combination, the eight enterprise-type Percentage_Engaged values sum to approximately 100%. This means they are **compositional**, not independent. A comparison of enterprise types that treats them as eight independent measurements violates this constraint. Statistical tests that test whether enterprise type explains between-combination variance (i.e. using the combination as the unit, not the individual enterprise share) are appropriate. Tests that treat eight enterprise shares as eight data points from the same distribution are not.

### Structural missingness in Dataset 2

The `(014, 016, 017, 02-99)` industry category has no observations in 2022 or 2023. This is a source-level structural absence, not missing at random. Any temporal analysis involving this category is limited to 2017–2021. Statistical methods that require complete temporal coverage across all years cannot be applied to this industry grouping.

### Practical significance vs statistical significance

Several findings are so large in magnitude that statistical significance is practically assured given any reasonable sample size. For example:
- The 19.2 pp female LFPR rise across 7 years
- The universal female < male LFPR gap across all 252 State × Year pairs
- The state range of 54.7 pp in female LFPR

For these, the relevant question is less "is the effect zero?" and more "how large is the effect, and with what precision?" Effect size measures and confidence intervals are therefore at least as important as p-values.

### Very short time series

For temporal trend tests (F1, F10), the analytical unit is a year-level mean — n = 7 time points. This severely limits statistical power for detecting anything other than near-monotonic trends. The large magnitudes observed (19.2 pp for LFPR, 8.7 pp for Proprietary enterprise share) provide high practical confidence, but formal tests should acknowledge low power as a limitation.

---

## 7. Recommended Sequence for Phase 6

The recommended order for moving selected findings into the next statistical analysis task is:

```
Stage 1 — PAIRED GENDER COMPARISON (Dataset 1)
   F2: Female vs Male LFPR gap — paired test across State × Year
   F7: Female vs Male variance comparison (Levene / F-test)

Stage 2 — TEMPORAL TREND ANALYSIS (Dataset 1)
   F1: Female LFPR trend 2017–2023
   F4: Rural–Urban gap trend (widening)

Stage 3 — GROUP DIFFERENCES (Dataset 1)
   F3: State variation in female LFPR (single-year cross-section)
   F5: Education gradient (omnibus group comparison)
   F6: Educated female unemployment: gender gap by education group
   F8: Change in LFPR by education group 2017 vs 2023

Stage 4 — ENTERPRISE STRUCTURE (Dataset 2)
   F11: Female vs Male enterprise participation gap
   F10: Enterprise type temporal trends 2017–2023

Stage 5 — VERIFICATION AND ROBUSTNESS
   Cross-section robustness checks for Stage 2 findings
   Single-year replication for Stage 1 findings
```

This sequence prioritises the most structurally clean and diagnostically important comparisons first, and moves to more complex multi-dimensional tests only after the primary findings are established. Dataset 2 findings (F10, F11) come after Dataset 1 primaries because they require careful handling of the compositional structure.

---

*Document completed 2026-10-07. No statistical tests have been executed. No source files have been modified. No CSVs have been created.*
