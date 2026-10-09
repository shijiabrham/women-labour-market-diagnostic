# Dataset 2 Feature‑Engineering Inspection Report

**Overall validation result:** PASS

---

## 1. Column Structure (21 columns)

| # | Column | Origin | Intended dtype | Actual dtype(s) | Description |
|---|--------|--------|----------------|----------------|-------------|
| 1 | Country | original | object | string | (original column) |
| 2 | State | original | object | string | (original column) |
| 3 | Year | original | object | string | (original column) |
| 4 | Type Of Areas | original | object | string | (original column) |
| 5 | Industry Division Type | original | object | string | (original column) |
| 6 | Gender | original | object | string | (original column) |
| 7 | Enterprise Type | original | object | string | (original column) |
| 8 | Persons Engaged In The Industry Groups By Enterprise Type (%) (UOM:%(Percentage)), Scaling Factor:1 | original | object | float | (original column) |
| 9 | Estimated Persons (UOM:Number), Scaling Factor:100 | original | object | float | (original column) |
| 10 | Sample Number Of Workers In The Enterprise (UOM:Number), Scaling Factor:1 | original | object | float | (original column) |
| 11 | Year_Numeric | engineered | int64 | int | engineered feature |
| 12 | Female_Flag | engineered | int64 | int | engineered feature |
| 13 | Industry_Division_Count | engineered | Int64 | int | engineered feature |
| 14 | Industry_Is_MultiDivision | engineered | int64 | int | engineered feature |
| 15 | Industry_Group_Type | engineered | object | string | engineered feature |
| 16 | Rural_Flag | engineered | int64 | int | engineered feature |
| 17 | Persons_Engaged_Percentage_Numeric | engineered | float64 | float | engineered feature |
| 18 | Industry_Percentage_Availability_Flag | engineered | int64 | int | engineered feature |
| 19 | Estimated_Persons_Availability_Flag | engineered | int64 | int | engineered feature |
| 20 | Sample_Number_Of_Workers_Availability_Flag | engineered | int64 | int | engineered feature |
| 21 | Structural_Missingness_Flag | engineered | int64 | int | engineered feature |

---

## 2. Row‑Count Validation
Rows: 31080 (expected 31080)
---

## 3. Original‑Column Integrity
All original columns unchanged
---

## 4. Year_Numeric Validation
Unique values: 2017, 2018, 2019, 2020, 2021, 2022, 2023
Missing: 0
Mismatched rows: 0
---

## 5. Female_Flag Validation
Counts: 0: 20720 | 1: 10360
---

## 6. Rural_Flag Validation
Counts: 0: 20736 | 1: 10344
---

## 7. Industry Division Values (unique)
(014, 016, 017 , 02-99), (05-99)
---

## 8. Multiple Industry Division Examples
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
- (014, 016, 017 , 02-99) | Count=4 | Multi=1 | Group=Multiple
---

## 9. Industry_Division_Count Distribution
| Count | Rows | Percent |
|------|------|---------|
| 1 | 18120 | 58.30% |
| 4 | 12960 | 41.70% |

Missing Industry_Division_Count: 0
---

## 10. Single vs Multiple Classification Consistency
Inconsistent rows: 0
---

## 11. Primary Percentage Indicator Summary
Count: 31080 non‑missing, Missing: 0
Min: 0.00, Max: 100.00, Mean: 12.50, Median: 1.80
---

## 12. Availability Flag Counts
Industry_Percentage_Availability_Flag: 1=31080
Estimated_Persons_Availability_Flag: 0=10344, 1=20736
Sample_Number_Of_Workers_Availability_Flag: 0=5184, 1=25896
Structural_Missingness_Flag: 0=25896, 1=5184

---

## 13. Structural Missingness Validation
Total Structural_Missingness_Flag=1 rows: 5184
Both missing: 5184
Estimated missing only: 0
Sample missing only: 0
---

## 14. Missingness Reconciliation with Cleaned Dataset
Cleaned missing Estimated Persons: 10344 (expected 10344)
Cleaned missing Sample Number: 5184 (expected 5184)
Engineered missing Estimated Persons: 10344
Engineered missing Sample Number: 5184
---

## 15. Representative Rows (15)
| Country | State | Year | Type Of Areas | Industry Division Type | Gender | Enterprise Type | Persons Engaged In The Industry Groups By Enterprise Type (%) (UOM:%(Percentage)), Scaling Factor:1 | Estimated Persons (UOM:Number), Scaling Factor:100 | Sample Number Of Workers In The Enterprise (UOM:Number), Scaling Factor:1 | Year_Numeric | Female_Flag | Industry_Division_Count | Industry_Is_MultiDivision | Industry_Group_Type | Rural_Flag | Persons_Engaged_Percentage_Numeric | Industry_Percentage_Availability_Flag | Estimated_Persons_Availability_Flag | Sample_Number_Of_Workers_Availability_Flag | Structural_Missingness_Flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| India | Andaman and Nicobar Islands | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Male | Proprietary and Partnership | 72.5 |  | 29805.0 | 2023 | 0 | 1 | 0 | Single | 1 | 72.5 | 1 | 0 | 1 | 0 |
| India | Andaman and Nicobar Islands | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Female | Proprietary and Partnership | 42.9 |  | 7049.0 | 2023 | 1 | 1 | 0 | Single | 1 | 42.9 | 1 | 0 | 1 | 0 |
| India | Andaman and Nicobar Islands | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Male | Proprietary and Partnership | 58.3 |  | 32811.0 | 2023 | 0 | 1 | 0 | Single | 0 | 58.3 | 1 | 0 | 1 | 0 |
| India | Andaman and Nicobar Islands | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Female | Proprietary and Partnership | 46.3 |  | 9067.0 | 2023 | 1 | 1 | 0 | Single | 0 | 46.3 | 1 | 0 | 1 | 0 |
| India | Andhra Pradesh | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Male | Proprietary and Partnership | 80.9 |  | 29805.0 | 2023 | 0 | 1 | 0 | Single | 1 | 80.9 | 1 | 0 | 1 | 0 |
| India | Andhra Pradesh | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Female | Proprietary and Partnership | 62.3 |  | 7049.0 | 2023 | 1 | 1 | 0 | Single | 1 | 62.3 | 1 | 0 | 1 | 0 |
| India | Andhra Pradesh | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Male | Proprietary and Partnership | 71.1 |  | 32811.0 | 2023 | 0 | 1 | 0 | Single | 0 | 71.1 | 1 | 0 | 1 | 0 |
| India | Andhra Pradesh | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Female | Proprietary and Partnership | 65.1 |  | 9067.0 | 2023 | 1 | 1 | 0 | Single | 0 | 65.1 | 1 | 0 | 1 | 0 |
| India | Arunachal Pradesh | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Male | Proprietary and Partnership | 53.8 |  | 29805.0 | 2023 | 0 | 1 | 0 | Single | 1 | 53.8 | 1 | 0 | 1 | 0 |
| India | Arunachal Pradesh | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Female | Proprietary and Partnership | 69.9 |  | 7049.0 | 2023 | 1 | 1 | 0 | Single | 1 | 69.9 | 1 | 0 | 1 | 0 |
| India | Arunachal Pradesh | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Male | Proprietary and Partnership | 51.3 |  | 32811.0 | 2023 | 0 | 1 | 0 | Single | 0 | 51.3 | 1 | 0 | 1 | 0 |
| India | Arunachal Pradesh | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Female | Proprietary and Partnership | 51.2 |  | 9067.0 | 2023 | 1 | 1 | 0 | Single | 0 | 51.2 | 1 | 0 | 1 | 0 |
| India | Assam | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Male | Proprietary and Partnership | 80.5 |  | 29805.0 | 2023 | 0 | 1 | 0 | Single | 1 | 80.5 | 1 | 0 | 1 | 0 |
| India | Assam | PLFS Year (Jul - Jun), 2023 | Rural | (05-99) | Female | Proprietary and Partnership | 65.8 |  | 7049.0 | 2023 | 1 | 1 | 0 | Single | 1 | 65.8 | 1 | 0 | 1 | 0 |
| India | Assam | PLFS Year (Jul - Jun), 2023 | Urban | (05-99) | Male | Proprietary and Partnership | 73.6 |  | 32811.0 | 2023 | 0 | 1 | 0 | Single | 0 | 73.6 | 1 | 0 | 1 | 0 |

---

## 16. Errors / Inconsistencies Found
None.