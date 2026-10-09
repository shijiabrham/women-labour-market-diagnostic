# Phase 4 – Methodology

**Data sources**
- `feature_engineered_dataset_1.csv` (22 650 rows, 14 columns)
- `feature_engineered_dataset_2.csv` (31 080 rows, 21 columns)

**Tools**
- Python standard library only (`csv`, `statistics`, `json`, `hashlib`, `pathlib`).
- No graphical libraries were available; all results are tabular.

**Processing steps**
1. Load CSVs with `csv.DictReader`.
2. Apply question‑specific filters (e.g., `Gender == "Female"`).
3. For each numeric variable, missing values (empty strings) are ignored.
4. Descriptive statistics computed: count, mean, median, min, max, population standard deviation.
5. Results are stored as JSON strings in the `Statistics` column of the result CSVs.

**Aggregations**
- Follow the exact aggregation level described in each question (year, state, education level, etc.).
- When a question could not be meaningfully answered (e.g., lacking grouping definitions), a limitation note is recorded.

**Limitations**
- No visual plots because `matplotlib`/`seaborn` are unavailable.
- The script does not perform inferential statistics.
