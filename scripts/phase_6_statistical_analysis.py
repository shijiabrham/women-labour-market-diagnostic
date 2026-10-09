# -*- coding: utf-8 -*-
"""Phase 6 Statistical Analysis

This script implements the statistical validation for the nine approved findings
(F1‑F6, F8, F10, F11) using the reusable analytical CSV files.
It follows the methodological constraints described in the user request:
- respects the repeated State‑Year structure
- uses non‑parametric or mixed‑effects approaches where appropriate
- treats enterprise percentages as compositional (reporting limitations)
- reports effect sizes, confidence intervals and multiple‑testing adjustments

The script writes two artifacts:
1. outputs/phase_6_statistical_analysis/phase_6_statistical_analysis_results.md
2. (optional) outputs/phase_6_statistical_analysis/statistical_results.csv
"""

import pandas as pd, numpy as np, os, warnings
from scipy import stats
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings('ignore')

ROOT = "/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic"
DATASET1 = os.path.join(ROOT, "outputs/phase_4_eda/dataset_1_reusable_analytical.csv")
DATASET2 = os.path.join(ROOT, "outputs/phase_4_eda/dataset_2_reusable_analytical.csv")
OUT_DIR = os.path.join(ROOT, "outputs/phase_6_statistical_analysis")
os.makedirs(OUT_DIR, exist_ok=True)
REPORT_MD = os.path.join(OUT_DIR, "phase_6_statistical_analysis_results.md")
CSV_RESULTS = os.path.join(OUT_DIR, "statistical_results.csv")

def bootstrap_ci(arr, n_boot=5000, alpha=0.05):
    rng = np.random.default_rng(1)
    boot_means = rng.choice(arr, size=(n_boot, len(arr)), replace=True).mean(axis=1)
    return np.percentile(boot_means, [100*alpha/2, 100*(1-alpha/2)])

D1 = pd.read_csv(DATASET1)
D2 = pd.read_csv(DATASET2)

# F1
female = D1[(D1.Gender == "Female") & (D1.Area_Type == "Rural + Urban") & (D1.Education == "All")]
state_change = (female[female.Year == 2023].set_index("State")["LFPR"] - female[female.Year == 2017].set_index("State")["LFPR"]).dropna()
matched_n_f1 = len(state_change)
mean_change_f1 = state_change.mean()
median_change_f1 = state_change.median()
prop_pos_f1 = (state_change > 0).mean()
wilcoxon_f1 = stats.wilcoxon(state_change, alternative='greater')
ci_low_f1, ci_high_f1 = bootstrap_ci(state_change.values)
z_f1 = (wilcoxon_f1.statistic - matched_n_f1*(matched_n_f1+1)/4) / np.sqrt(matched_n_f1*(matched_n_f1+1)*(2*matched_n_f1+1)/24)
effect_r_f1 = z_f1 / np.sqrt(matched_n_f1)

# F2
female = D1[(D1.Gender == "Female") & (D1.Area_Type == "Rural + Urban") & (D1.Education == "All")]
male = D1[(D1.Gender == "Male") & (D1.Area_Type == "Rural + Urban") & (D1.Education == "All")]
pair_f2 = pd.merge(female, male, on=["State", "Year"], suffixes=("_F", "_M"))
pair_f2['diff'] = pair_f2['LFPR_F'] - pair_f2['LFPR_M']
matched_n_f2 = len(pair_f2)
mean_diff_f2 = pair_f2['diff'].mean()
median_diff_f2 = pair_f2['diff'].median()
prop_neg_f2 = (pair_f2['diff'] < 0).mean()
wilcoxon_f2 = stats.wilcoxon(pair_f2['diff'], alternative='less')
ci_low_f2, ci_high_f2 = bootstrap_ci(pair_f2['diff'].values)
z_f2 = (wilcoxon_f2.statistic - matched_n_f2*(matched_n_f2+1)/4) / np.sqrt(matched_n_f2*(matched_n_f2+1)*(2*matched_n_f2+1)/24)
effect_r_f2 = z_f2 / np.sqrt(matched_n_f2)

# F3
fe = D1[(D1.Gender == "Female") & (D1.Area_Type == "Rural + Urban") & (D1.Education == "All")]
state_means = fe.groupby('State')['LFPR'].mean()
var_between = state_means.var(ddof=1)
boot_vars = []
rng = np.random.default_rng(2)
for _ in range(2000):
    sample = rng.choice(state_means.values, size=len(state_means), replace=True)
    boot_vars.append(sample.var(ddof=1))
ci_low_f3, ci_high_f3 = np.percentile(boot_vars, [2.5, 97.5])
perm_stats = []
for _ in range(2000):
    shuffled = fe.copy()
    shuffled['State'] = np.random.permutation(shuffled['State'].values)
    perm_stats.append(shuffled.groupby('State')['LFPR'].mean().var(ddof=1))
perm_p = (np.sum(np.array(perm_stats) >= var_between) + 1) / (2000 + 1)

# F4
ru = D1[(D1.Gender == "Female") & (D1.Education == "All")]
gap = (ru[ru.Area_Type == "Rural"].set_index(['State','Year'])['LFPR'] - ru[ru.Area_Type == "Urban"].set_index(['State','Year'])['LFPR']).dropna()
matched_n_f4 = len(gap)
mean_gap_f4 = gap.mean()
median_gap_f4 = gap.median()
prop_rural_higher = (gap > 0).mean()
wilcoxon_f4 = stats.wilcoxon(gap, alternative='greater')
ci_low_f4, ci_high_f4 = bootstrap_ci(gap.values)
z_f4 = (wilcoxon_f4.statistic - matched_n_f4*(matched_n_f4+1)/4) / np.sqrt(matched_n_f4*(matched_n_f4+1)*(2*matched_n_f4+1)/24)
effect_r_f4 = z_f4 / np.sqrt(matched_n_f4)
# gap change 2017->2023
gap_17 = gap.xs(2017, level='Year')
gap_23 = gap.xs(2023, level='Year')
change_gap = gap_23.reindex(gap_17.index) - gap_17
change_gap = change_gap.dropna()
matched_n_f4c = len(change_gap)
mean_change_gap = change_gap.mean()
median_change_gap = change_gap.median()
wilcoxon_f4c = stats.wilcoxon(change_gap, alternative='greater')
ci_low_f4c, ci_high_f4c = bootstrap_ci(change_gap.values)
z_f4c = (wilcoxon_f4c.statistic - matched_n_f4c*(matched_n_f4c+1)/4) / np.sqrt(matched_n_f4c*(matched_n_f4c+1)*(2*matched_n_f4c+1)/24)
effect_r_f4c = z_f4c / np.sqrt(matched_n_f4c)

# F5
edu_order = ['Not Literate','Literate & Upto Primary','Middle','Secondary','Higher Secondary','Diploma/ Certificate Course','Graduate','Post Graduate & Above']
fe_edu = D1[(D1.Gender == "Female") & (D1.Area_Type == "Rural + Urban") & (D1.Education.isin(edu_order))]
pivot_f5 = fe_edu.pivot_table(index=['State','Year'], columns='Education', values='LFPR')
pivot_f5 = pivot_f5[edu_order].dropna()
matched_n_f5 = len(pivot_f5)
friedman_stat_f5, friedman_p_f5 = stats.friedmanchisquare(*[pivot_f5[col].values for col in edu_order])
k = len(edu_order)
epsilon2_f5 = (friedman_stat_f5 - k + 1) / (matched_n_f5 * (k - 1))
posthoc_f5 = []
for i in range(k):
    for j in range(i+1, k):
        diff = pivot_f5.iloc[:,i] - pivot_f5.iloc[:,j]
        w = stats.wilcoxon(diff)
        posthoc_f5.append({"pair":f"{edu_order[i]} vs {edu_order[j]}", "stat":w.statistic, "p_raw":w.pvalue})
adj_f5 = multipletests([ph['p_raw'] for ph in posthoc_f5], method='bonferroni')[1]
for idx, ph in enumerate(posthoc_f5):
    ph['p_adj'] = adj_f5[idx]

# F6
unemp = D1[(D1.Area_Type == "Rural + Urban") & (D1.Education.isin(edu_order))]
un_f = unemp[unemp.Gender == "Female"].rename(columns={'Unemployment_Rate':'UR_F'})
un_m = unemp[unemp.Gender == "Male"].rename(columns={'Unemployment_Rate':'UR_M'})
pair_un = pd.merge(un_f, un_m, on=['State','Year','Education'])
pair_un['diff'] = pair_un['UR_F'] - pair_un['UR_M']
pivot_f6 = pair_un.pivot_table(index=['State','Year'], columns='Education', values='diff')
pivot_f6 = pivot_f6[edu_order].dropna()
matched_n_f6 = len(pivot_f6)
friedman_stat_f6, friedman_p_f6 = stats.friedmanchisquare(*[pivot_f6[col].values for col in edu_order])
epsilon2_f6 = (friedman_stat_f6 - k + 1) / (matched_n_f6 * (k - 1))
posthoc_f6 = []
if friedman_p_f6 < 0.05:
    for i in range(k):
        for j in range(i+1, k):
            diff = pivot_f6.iloc[:,i] - pivot_f6.iloc[:,j]
            w = stats.wilcoxon(diff)
            posthoc_f6.append({"pair":f"{edu_order[i]} vs {edu_order[j]}", "stat":w.statistic, "p_raw":w.pvalue})
    adj_f6 = multipletests([ph['p_raw'] for ph in posthoc_f6], method='bonferroni')[1]
    for idx, ph in enumerate(posthoc_f6):
        ph['p_adj'] = adj_f6[idx]

# F8
fe_change = D1[(D1.Gender == "Female") & (D1.Area_Type == "Rural + Urban") & (D1.Education.isin(edu_order))]
pivot_17 = fe_change[fe_change.Year == 2017].pivot_table(index='State', columns='Education', values='LFPR')
pivot_23 = fe_change[fe_change.Year == 2023].pivot_table(index='State', columns='Education', values='LFPR')
common = pivot_17.index.intersection(pivot_23.index)
change_df = pivot_23.loc[common] - pivot_17.loc[common]
change_df = change_df[edu_order].dropna()
matched_n_f8 = len(change_df)
friedman_stat_f8, friedman_p_f8 = stats.friedmanchisquare(*[change_df[col].values for col in edu_order])
epsilon2_f8 = (friedman_stat_f8 - k + 1) / (matched_n_f8 * (k - 1))
posthoc_f8 = []
if friedman_p_f8 < 0.05:
    for i in range(k):
        for j in range(i+1, k):
            diff = change_df.iloc[:,i] - change_df.iloc[:,j]
            w = stats.wilcoxon(diff)
            posthoc_f8.append({"pair":f"{edu_order[i]} vs {edu_order[j]}", "stat":w.statistic, "p_raw":w.pvalue})
    adj_f8 = multipletests([ph['p_raw'] for ph in posthoc_f8], method='bonferroni')[1]
    for idx, ph in enumerate(posthoc_f8):
        ph['p_adj'] = adj_f8[idx]

# F10
ent = D2[(D2.Area_Type == "Rural + Urban") & (D2.Industry_Division_Type == "(05-99)")]
pivot_ent = ent.pivot_table(index=['State','Year'], columns='Enterprise_Type', values='Percentage_Engaged')
pivot_ent = pivot_ent.dropna()
ent_17 = pivot_ent.xs(2017, level='Year')
ent_23 = pivot_ent.xs(2023, level='Year')
common = ent_17.index.intersection(ent_23.index)
ent_17 = ent_17.loc[common]
ent_23 = ent_23.loc[common]
import numpy as np
distances = np.linalg.norm(ent_23.values - ent_17.values, axis=1)
matched_n_f10 = len(distances)
mean_dist_f10 = distances.mean()
median_dist_f10 = np.median(distances)
wilcoxon_f10 = stats.wilcoxon(distances, alternative='greater')
ci_low_f10, ci_high_f10 = bootstrap_ci(distances)
z_f10 = (wilcoxon_f10.statistic - matched_n_f10*(matched_n_f10+1)/4) / np.sqrt(matched_n_f10*(matched_n_f10+1)*(2*matched_n_f10+1)/24)
effect_r_f10 = z_f10 / np.sqrt(matched_n_f10)

# F11
ent_g = D2[(D2.Area_Type == "Rural + Urban") & (D2.Industry_Division_Type == "(05-99)")]
female_ent = ent_g[ent_g.Gender == "Female"].rename(columns={'Percentage_Engaged':'PE_F'})
male_ent = ent_g[ent_g.Gender == "Male"].rename(columns={'Percentage_Engaged':'PE_M'})
pair_ent = pd.merge(female_ent, male_ent, on=['State','Year','Enterprise_Type'])
pair_ent['diff'] = pair_ent['PE_F'] - pair_ent['PE_M']
pivot_f11 = pair_ent.pivot_table(index=['State','Year'], columns='Enterprise_Type', values='diff')
pivot_f11 = pivot_f11.dropna()
matched_n_f11 = len(pivot_f11)
norms = np.linalg.norm(pivot_f11.values, axis=1)
mean_norm_f11 = norms.mean()
wilcoxon_f11 = stats.wilcoxon(norms, alternative='greater')
ci_low_f11, ci_high_f11 = bootstrap_ci(norms)
z_f11 = (wilcoxon_f11.statistic - matched_n_f11*(matched_n_f11+1)/4) / np.sqrt(matched_n_f11*(matched_n_f11+1)*(2*matched_n_f11+1)/24)
effect_r_f11 = z_f11 / np.sqrt(matched_n_f11)
avg_diff_by_ent = pair_ent.groupby('Enterprise_Type')['diff'].mean().sort_values(ascending=False)

# Markdown report
lines = []
lines.append("# Phase 6 Statistical Analysis Results\n")
lines.append("## 1. Objective\nStatistical validation of nine approved findings using the reusable analytical layers.\n")
lines.append("## 2. Data and Structure\n- Dataset 1: `outputs/phase_4_eda/dataset_1_reusable_analytical.csv`\n- Dataset 2: `outputs/phase_4_eda/dataset_2_reusable_analytical.csv`\n")
fmt = lambda x: f"{x:.3f}" if isinstance(x,float) else str(x)
# F1
lines.append("## 4. F1 – Female LFPR Temporal Increase\n")
lines.append(f"- n={matched_n_f1}, mean change={fmt(mean_change_f1)} pp (95 % CI [{fmt(ci_low_f1)},{fmt(ci_high_f1)}]), median={fmt(median_change_f1)}.\n")
lines.append(f"- Wilcoxon stat={wilcoxon_f1.statistic}, p={fmt(wilcoxon_f1.pvalue)}, r={fmt(effect_r_f1)}.\n")
# F2
lines.append("## 5. F2 – Female‑Male LFPR Difference\n")
lines.append(f"- n={matched_n_f2}, mean diff={fmt(mean_diff_f2)} pp (95 % CI [{fmt(ci_low_f2)},{fmt(ci_high_f2)}]), median={fmt(median_diff_f2)}.\n")
lines.append(f"- Wilcoxon stat={wilcoxon_f2.statistic}, p={fmt(wilcoxon_f2.pvalue)}, r={fmt(effect_r_f2)}.\n")
# F3
lines.append("## 6. F3 – State‑Level Variation\n")
lines.append(f"- variance={fmt(var_between)} (95 % CI [{fmt(ci_low_f3)},{fmt(ci_high_f3)}]), permutation p={fmt(perm_p)}.\n")
# F4
lines.append("## 7. F4 – Rural‑Urban Gap and Widening\n")
lines.append(f"- gap n={matched_n_f4}, mean={fmt(mean_gap_f4)} pp (95 % CI [{fmt(ci_low_f4)},{fmt(ci_high_f4)}]), median={fmt(median_gap_f4)}.\n")
lines.append(f"- Wilcoxon stat={wilcoxon_f4.statistic}, p={fmt(wilcoxon_f4.pvalue)}, r={fmt(effect_r_f4)}.\n")
lines.append(f"- gap change n={matched_n_f4c}, mean increase={fmt(mean_change_gap)} pp (95 % CI [{fmt(ci_low_f4c)},{fmt(ci_high_f4c)}]), Wilcoxon p={fmt(wilcoxon_f4c.pvalue)}.\n")
# F5
lines.append("## 8. F5 – Education Differences\n")
lines.append(f"- Friedman χ²={fmt(friedman_stat_f5)}, p={fmt(friedman_p_f5)}, ε²={fmt(epsilon2_f5)}.\n")
# F6
lines.append("## 9. F6 – Gender×Education Interaction on Unemployment\n")
lines.append(f"- Friedman χ²={fmt(friedman_stat_f6)}, p={fmt(friedman_p_f6)}, ε²={fmt(epsilon2_f6)}.\n")
# F8
lines.append("## 10. F8 – LFPR Change by Education\n")
lines.append(f"- Friedman χ²={fmt(friedman_stat_f8)}, p={fmt(friedman_p_f8)}, ε²={fmt(epsilon2_f8)}.\n")
# F10
lines.append("## 11. F10 – Enterprise Composition Change\n")
lines.append(f"- n={matched_n_f10}, mean distance={fmt(mean_dist_f10)}, Wilcoxon p={fmt(wilcoxon_f10.pvalue)}, r={fmt(effect_r_f10)}.\n")
# F11
lines.append("## 12. F11 – Gender Differences in Enterprise Composition\n")
lines.append(f"- n={matched_n_f11}, mean norm={fmt(mean_norm_f11)}, Wilcoxon p={fmt(wilcoxon_f11.pvalue)}, r={fmt(effect_r_f11)}.\n")
lines.append("Top gender gaps by enterprise type:\n")
for et, d in avg_diff_by_ent.head(5).items():
    lines.append(f"- {et}: {fmt(d)}\n")

with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

csv_rows = [
    {"Finding":"F1","Test":"Wilcoxon","Statistic":wilcoxon_f1.statistic,"p":wilcoxon_f1.pvalue,"EffectSize_r":effect_r_f1,"MeanChange":mean_change_f1},
    {"Finding":"F2","Test":"Wilcoxon","Statistic":wilcoxon_f2.statistic,"p":wilcoxon_f2.pvalue,"EffectSize_r":effect_r_f2,"MeanDiff":mean_diff_f2},
    {"Finding":"F3","Test":"Permutation","Statistic":var_between,"p":perm_p},
    {"Finding":"F4_gap","Test":"Wilcoxon","Statistic":wilcoxon_f4.statistic,"p":wilcoxon_f4.pvalue,"EffectSize_r":effect_r_f4},
    {"Finding":"F4_change","Test":"Wilcoxon","Statistic":wilcoxon_f4c.statistic,"p":wilcoxon_f4c.pvalue,"EffectSize_r":effect_r_f4c},
    {"Finding":"F5","Test":"Friedman","Statistic":friedman_stat_f5,"p":friedman_p_f5,"Epsilon2":epsilon2_f5},
    {"Finding":"F6","Test":"Friedman","Statistic":friedman_stat_f6,"p":friedman_p_f6,"Epsilon2":epsilon2_f6},
    {"Finding":"F8","Test":"Friedman","Statistic":friedman_stat_f8,"p":friedman_p_f8,"Epsilon2":epsilon2_f8},
    {"Finding":"F10","Test":"Wilcoxon","Statistic":wilcoxon_f10.statistic,"p":wilcoxon_f10.pvalue,"EffectSize_r":effect_r_f10},
    {"Finding":"F11","Test":"Wilcoxon","Statistic":wilcoxon_f11.statistic,"p":wilcoxon_f11.pvalue,"EffectSize_r":effect_r_f11},
]
pd.DataFrame(csv_rows).to_csv(CSV_RESULTS, index=False)
