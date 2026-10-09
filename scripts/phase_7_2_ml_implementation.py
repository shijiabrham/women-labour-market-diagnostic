# -*- coding: utf-8 -*-
"""Phase 7.2 Machine Learning Implementation
Predicting the Female-Male LFPR Gap using Education, Area_Type, and Year.
Validation via Leave-One-State-Out (LOSO) Cross-Validation across 36 States.
"""

import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = "/Users/shiji/Documents/AG_workfiles/women-labour-market-diagnostic"
DATASET1 = os.path.join(ROOT, "outputs/phase_4_eda/dataset_1_reusable_analytical.csv")
OUT_DIR = os.path.join(ROOT, "outputs/phase_7_ml")
os.makedirs(OUT_DIR, exist_ok=True)

CSV_RESULTS = os.path.join(OUT_DIR, "model_results.csv")
CSV_PREDICTIONS = os.path.join(OUT_DIR, "out_of_fold_predictions.csv")
CSV_IMPORTANCE = os.path.join(OUT_DIR, "model_feature_importance.csv")
CSV_FOLDS = os.path.join(OUT_DIR, "fold_performance.csv")
REPORT_MD = os.path.join(OUT_DIR, "phase_7_2_ml_analysis.md")

# 1. Load Data
d1 = pd.read_csv(DATASET1)

edu_levels = [
    'Not Literate', 'Literate & Upto Primary', 'Middle', 'Secondary',
    'Higher Secondary', 'Diploma/ Certificate Course', 'Graduate', 'Post Graduate & Above'
]

# Filter Female & Male within Rural & Urban for the 8 detailed education levels
f_df = d1[(d1.Gender == 'Female') & (d1.Area_Type.isin(['Rural', 'Urban'])) & (d1.Education.isin(edu_levels))]
m_df = d1[(d1.Gender == 'Male') & (d1.Area_Type.isin(['Rural', 'Urban'])) & (d1.Education.isin(edu_levels))]

# Match pairs
merged = pd.merge(f_df, m_df, on=['State', 'Year', 'Area_Type', 'Education'], suffixes=('_F', '_M'))
merged['target'] = merged['LFPR_F'] - merged['LFPR_M']

# Exclude missing target values (documenting 8 dropped rows)
data = merged.dropna(subset=['target']).copy().reset_index(drop=True)

# Define features and target
X = data[['Education', 'Area_Type', 'Year']].copy()
y = data['target'].values
groups = data['State'].values
states = np.unique(groups)
n_states = len(states)
n_samples = len(data)

# Baseline, Ridge, GBR prediction arrays
baseline_oof = np.zeros(n_samples)
ridge_oof = np.zeros(n_samples)
gbr_oof = np.zeros(n_samples)

cat_cols = ['Education', 'Area_Type']
num_cols = ['Year']

# Reference category for Education is set explicitly: 'Not Literate'
# Reference category for Area_Type is 'Rural'
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_cols),
        ('num', StandardScaler(), num_cols)
    ]
)

ridge_model = Pipeline([
    ('prep', preprocessor),
    ('reg', Ridge(alpha=1.0, random_state=42))
])

gbr_model = Pipeline([
    ('prep', preprocessor),
    ('reg', GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42))
])

fold_records = []

# Leave-One-State-Out (LOSO) Cross-Validation
for fold_idx, state in enumerate(states, 1):
    train_mask = (groups != state)
    test_mask = (groups == state)
    
    X_train, y_train = X.iloc[train_mask], y[train_mask]
    X_test, y_test = X.iloc[test_mask], y[test_mask]
    
    # Baseline: Training mean
    fold_train_mean = np.mean(y_train)
    baseline_oof[test_mask] = fold_train_mean
    
    # Ridge
    ridge_model.fit(X_train, y_train)
    ridge_pred = ridge_model.predict(X_test)
    ridge_oof[test_mask] = ridge_pred
    
    # GBR
    gbr_model.fit(X_train, y_train)
    gbr_pred = gbr_model.predict(X_test)
    gbr_oof[test_mask] = gbr_pred
    
    # Fold-level metrics
    b_mae = mean_absolute_error(y_test, np.full_like(y_test, fold_train_mean))
    b_rmse = np.sqrt(mean_squared_error(y_test, np.full_like(y_test, fold_train_mean)))
    b_r2 = r2_score(y_test, np.full_like(y_test, fold_train_mean))
    
    r_mae = mean_absolute_error(y_test, ridge_pred)
    r_rmse = np.sqrt(mean_squared_error(y_test, ridge_pred))
    r_r2 = r2_score(y_test, ridge_pred)
    
    g_mae = mean_absolute_error(y_test, gbr_pred)
    g_rmse = np.sqrt(mean_squared_error(y_test, gbr_pred))
    g_r2 = r2_score(y_test, gbr_pred)
    
    fold_records.append({
        'Fold': fold_idx,
        'Held_Out_State': state,
        'Test_Samples': int(np.sum(test_mask)),
        'Baseline_MAE': b_mae,
        'Baseline_RMSE': b_rmse,
        'Baseline_R2': b_r2,
        'Ridge_MAE': r_mae,
        'Ridge_RMSE': r_rmse,
        'Ridge_R2': r_r2,
        'GBR_MAE': g_mae,
        'GBR_RMSE': g_rmse,
        'GBR_R2': g_r2
    })

fold_df = pd.DataFrame(fold_records)
fold_df.to_csv(CSV_FOLDS, index=False)

# Aggregated Overall Out-Of-Fold Evaluation
def calc_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2

b_mae, b_rmse, b_r2 = calc_metrics(y, baseline_oof)
r_mae, r_rmse, r_r2 = calc_metrics(y, ridge_oof)
g_mae, g_rmse, g_r2 = calc_metrics(y, gbr_oof)

results_summary = [
    {
        'Model': 'Baseline (Training Mean)',
        'Validation_Method': 'Leave-One-State-Out (LOSO)',
        'Total_Folds': n_states,
        'Total_Observations': n_samples,
        'MAE': b_mae,
        'RMSE': b_rmse,
        'R2': b_r2
    },
    {
        'Model': 'Ridge Regression',
        'Validation_Method': 'Leave-One-State-Out (LOSO)',
        'Total_Folds': n_states,
        'Total_Observations': n_samples,
        'MAE': r_mae,
        'RMSE': r_rmse,
        'R2': r_r2
    },
    {
        'Model': 'Gradient Boosting Regressor',
        'Validation_Method': 'Leave-One-State-Out (LOSO)',
        'Total_Folds': n_states,
        'Total_Observations': n_samples,
        'MAE': g_mae,
        'RMSE': g_rmse,
        'R2': g_r2
    }
]

results_df = pd.DataFrame(results_summary)
results_df.to_csv(CSV_RESULTS, index=False)

# Out-of-fold predictions dataset
oof_df = data[['State', 'Year', 'Area_Type', 'Education', 'LFPR_F', 'LFPR_M', 'target']].copy()
oof_df.rename(columns={'target': 'Actual_Gender_Gap'}, inplace=True)
oof_df['Baseline_Pred'] = baseline_oof
oof_df['Ridge_Pred'] = ridge_oof
oof_df['GBR_Pred'] = gbr_oof
oof_df['Ridge_Error'] = oof_df['Actual_Gender_Gap'] - oof_df['Ridge_Pred']
oof_df['GBR_Error'] = oof_df['Actual_Gender_Gap'] - oof_df['GBR_Pred']
oof_df.to_csv(CSV_PREDICTIONS, index=False)

# Fit full models for interpretation
ridge_model.fit(X, y)
gbr_model.fit(X, y)

cat_feature_names = ridge_model.named_steps['prep'].named_transformers_['cat'].get_feature_names_out(cat_cols)
feature_names = list(cat_feature_names) + ['Year_Standardized']

ridge_coefs = ridge_model.named_steps['reg'].coef_
ridge_intercept = ridge_model.named_steps['reg'].intercept_
gbr_importances = gbr_model.named_steps['reg'].feature_importances_

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Ridge_Coefficient': ridge_coefs,
    'GBR_Feature_Importance': gbr_importances
}).sort_values(by='GBR_Feature_Importance', ascending=False)
importance_df.to_csv(CSV_IMPORTANCE, index=False)

print("Execution finished successfully.")
print("Summary Results:")
print(results_df.to_string(index=False))
