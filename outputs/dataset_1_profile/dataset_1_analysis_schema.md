# Dataset 1 Analysis Schema

When loading the CSV into pandas, use the following dtype specifications:

```python
dtype = {
    'Country': 'string',
    'State': 'string',
    'Year': 'string',
    'Type Of Areas': 'string',
    'Gender': 'string',
    'Education Level': 'string',
    'Labor Force Participation Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1': 'float64',
    'Working Population Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1': 'float64',
    'Unemployment Rate According To Usual Status Based On Different General Education Level (UOM:%(Percentage)), Scaling Factor:1': 'float64',
    'Year_Numeric': 'int64',
    'Female_Flag': 'int64',
    'Education_Level_Order': 'Int64',  # pandas nullable integer
    'Education_Category_Type': 'string',
    'Indicator_Availability_Flag': 'int64'
}
```