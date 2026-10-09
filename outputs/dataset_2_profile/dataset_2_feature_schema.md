# Dataset 2 Feature Schema

| Column | Intended dtype | Description |
|--------|----------------|-------------|
| Country | object | original column |
| State | object | original column |
| Year | object | original column |
| Type Of Areas | object | original column |
| Industry Division Type | object | original column |
| Gender | object | original column |
| Enterprise Type | object | original column |
| Persons Engaged In The Industry Groups By Enterprise Type (%) (UOM:%(Percentage)), Scaling Factor:1 | object | original column |
| Estimated Persons (UOM:Number), Scaling Factor:100 | object | original column |
| Sample Number Of Workers In The Enterprise (UOM:Number), Scaling Factor:1 | object | original column |
| Year_Numeric | int64 | Numeric year extracted from the Year column. |
| Female_Flag | int64 | 1 for Female, 0 otherwise. |
| Industry_Division_Count | Int64 | Count of division codes in Industry Division Type. |
| Industry_Is_MultiDivision | int64 | 1 if more than one division code, else 0. |
| Industry_Group_Type | object | 'Multiple' or 'Single' based on division count. |
| Rural_Flag | int64 | 1 for Rural area type, 0 for Urban. |
| Persons_Engaged_Percentage_Numeric | float64 | Numeric percentage of persons engaged (as provided). |
| Industry_Percentage_Availability_Flag | int64 | 1 if the percentage column is present, else 0. |
| Estimated_Persons_Availability_Flag | int64 | 1 if Estimated Persons column is present, else 0. |
| Sample_Number_Of_Workers_Availability_Flag | int64 | 1 if Sample Number column is present, else 0. |
| Structural_Missingness_Flag | int64 | 1 only when both Estimated Persons and Sample Number are missing. |
