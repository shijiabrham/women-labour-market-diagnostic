# Dataset 2 – Missingness Pattern by Dimension

## Objective
Identify where missing values occur in the two numeric fields (Estimated Persons and Sample Number Of Workers) and describe their distribution across the categorical dimensions, using only the raw CSV as source of truth.

## Confirmed Baseline Totals
- Total rows: 31080
- Estimated Persons missing: 10344
- Sample Workers missing: 5184
- Percentage field missing: 0
- Years present: ['PLFS Year (Jul - Jun), 2017', 'PLFS Year (Jul - Jun), 2018', 'PLFS Year (Jul - Jun), 2019', 'PLFS Year (Jul - Jun), 2020', 'PLFS Year (Jul - Jun), 2021', 'PLFS Year (Jul - Jun), 2022', 'PLFS Year (Jul - Jun), 2023']

## Missingness by Year

| Year | Total | Est Missing | Est % | Samp Missing | Samp % |
|------|------:|------------:|------:|-------------:|------:|
| PLFS Year (Jul - Jun), 2017 | 5184 | 5184 | 100.0 | 5184 | 100.0 |
| PLFS Year (Jul - Jun), 2018 | 5184 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2019 | 5184 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2020 | 5184 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2021 | 5184 | 0 | 0.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2022 | 2592 | 2592 | 100.0 | 0 | 0.0 |
| PLFS Year (Jul - Jun), 2023 | 2568 | 2568 | 100.0 | 0 | 0.0 |

## Missingness by State (full)

| State | Total | Est Missing | Est % | Samp Missing | Samp % |
|-------|------:|------------:|------:|-------------:|------:|
| Andaman and Nicobar Islands | 864 | 288 | 33.33 | 144 | 16.67 |
| Andhra Pradesh | 864 | 288 | 33.33 | 144 | 16.67 |
| Arunachal Pradesh | 864 | 288 | 33.33 | 144 | 16.67 |
| Assam | 864 | 288 | 33.33 | 144 | 16.67 |
| Bihar | 864 | 288 | 33.33 | 144 | 16.67 |
| Chandigarh | 840 | 264 | 31.43 | 144 | 17.14 |
| Chhattisgarh | 864 | 288 | 33.33 | 144 | 16.67 |
| Delhi | 864 | 288 | 33.33 | 144 | 16.67 |
| Goa | 864 | 288 | 33.33 | 144 | 16.67 |
| Gujarat | 864 | 288 | 33.33 | 144 | 16.67 |
| Haryana | 864 | 288 | 33.33 | 144 | 16.67 |
| Himachal Pradesh | 864 | 288 | 33.33 | 144 | 16.67 |
| Jammu and Kashmir | 864 | 288 | 33.33 | 144 | 16.67 |
| Jharkhand | 864 | 288 | 33.33 | 144 | 16.67 |
| Karnataka | 864 | 288 | 33.33 | 144 | 16.67 |
| Kerala | 864 | 288 | 33.33 | 144 | 16.67 |
| Ladakh | 864 | 288 | 33.33 | 144 | 16.67 |
| Lakshadweep | 864 | 288 | 33.33 | 144 | 16.67 |
| Madhya Pradesh | 864 | 288 | 33.33 | 144 | 16.67 |
| Maharashtra | 864 | 288 | 33.33 | 144 | 16.67 |
| Manipur | 864 | 288 | 33.33 | 144 | 16.67 |
| Meghalaya | 864 | 288 | 33.33 | 144 | 16.67 |
| Mizoram | 864 | 288 | 33.33 | 144 | 16.67 |
| Nagaland | 864 | 288 | 33.33 | 144 | 16.67 |
| Odisha | 864 | 288 | 33.33 | 144 | 16.67 |
| Puducherry | 864 | 288 | 33.33 | 144 | 16.67 |
| Punjab | 864 | 288 | 33.33 | 144 | 16.67 |
| Rajasthan | 864 | 288 | 33.33 | 144 | 16.67 |
| Sikkim | 864 | 288 | 33.33 | 144 | 16.67 |
| Tamil Nadu | 864 | 288 | 33.33 | 144 | 16.67 |
| Telangana | 864 | 288 | 33.33 | 144 | 16.67 |
| The Dadra and Nagar Haveli and Daman and Diu | 864 | 288 | 33.33 | 144 | 16.67 |
| Tripura | 864 | 288 | 33.33 | 144 | 16.67 |
| Uttar Pradesh | 864 | 288 | 33.33 | 144 | 16.67 |
| Uttarakhand | 864 | 288 | 33.33 | 144 | 16.67 |
| West Bengal | 864 | 288 | 33.33 | 144 | 16.67 |

## Missingness by Type Of Areas

| Type Of Areas | Total | Est Missing | Est % | Samp Missing | Samp % |
|----------------|------:|------------:|------:|-------------:|------:|
| Rural | 10344 | 3432 | 33.18 | 1728 | 16.71 |
| Rural + Urban | 10368 | 3456 | 33.33 | 1728 | 16.67 |
| Urban | 10368 | 3456 | 33.33 | 1728 | 16.67 |

## Missingness by Industry Division Type

| Industry Division Type | Total | Est Missing | Est % | Samp Missing | Samp % |
|-----------------------|------:|------------:|------:|-------------:|------:|
| (014, 016, 017 , 02-99) | 12960 | 2592 | 20.0 | 2592 | 20.0 |
| (05-99) | 18120 | 7752 | 42.78 | 2592 | 14.3 |

## Missingness by Gender

| Gender | Total | Est Missing | Est % | Samp Missing | Samp % |
|--------|------:|------------:|------:|-------------:|------:|
| Female | 10360 | 3448 | 33.28 | 1728 | 16.68 |
| Male | 10360 | 3448 | 33.28 | 1728 | 16.68 |
| Persons | 10360 | 3448 | 33.28 | 1728 | 16.68 |

## Missingness by Enterprise Type

| Enterprise Type | Total | Est Missing | Est % | Samp Missing | Samp % |
|----------------|------:|------------:|------:|-------------:|------:|
| Autonomous Bodies | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Cooperative Societies | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Employer's Households | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Govt./ Local Body/ Public Sector Enterprises | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Others | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Proprietary and Partnership | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Public/ Private Limited Company | 3885 | 1293 | 33.28 | 648 | 16.68 |
| Trust/ Other Non Profit inst | 3885 | 1293 | 33.28 | 648 | 16.68 |

## Year × Dimension Observations (where missingness occurs)

### Year × State

| Year | State | Total | Est Missing | Samp Missing |
|------|------|------:|------------:|-------------:|
| PLFS Year (Jul - Jun), 2017 | Andaman and Nicobar Islands | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Andhra Pradesh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Arunachal Pradesh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Assam | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Bihar | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Chandigarh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Chhattisgarh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Delhi | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Goa | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Gujarat | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Haryana | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Himachal Pradesh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Jammu and Kashmir | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Jharkhand | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Karnataka | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Kerala | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Ladakh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Lakshadweep | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Madhya Pradesh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Maharashtra | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Manipur | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Meghalaya | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Mizoram | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Nagaland | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Odisha | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Puducherry | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Punjab | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Rajasthan | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Sikkim | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Tamil Nadu | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Telangana | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | The Dadra and Nagar Haveli and Daman and Diu | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Tripura | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Uttar Pradesh | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | Uttarakhand | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2017 | West Bengal | 144 | 144 | 144 |
| PLFS Year (Jul - Jun), 2022 | Andaman and Nicobar Islands | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Andhra Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Arunachal Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Assam | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Bihar | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Chandigarh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Chhattisgarh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Delhi | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Goa | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Gujarat | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Haryana | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Himachal Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Jammu and Kashmir | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Jharkhand | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Karnataka | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Kerala | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Ladakh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Lakshadweep | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Madhya Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Maharashtra | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Manipur | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Meghalaya | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Mizoram | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Nagaland | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Odisha | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Puducherry | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Punjab | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Rajasthan | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Sikkim | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Tamil Nadu | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Telangana | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | The Dadra and Nagar Haveli and Daman and Diu | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Tripura | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Uttar Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | Uttarakhand | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2022 | West Bengal | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Andaman and Nicobar Islands | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Andhra Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Arunachal Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Assam | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Bihar | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Chandigarh | 48 | 0 | 48 |
| PLFS Year (Jul - Jun), 2023 | Chhattisgarh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Delhi | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Goa | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Gujarat | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Haryana | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Himachal Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Jammu and Kashmir | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Jharkhand | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Karnataka | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Kerala | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Ladakh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Lakshadweep | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Madhya Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Maharashtra | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Manipur | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Meghalaya | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Mizoram | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Nagaland | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Odisha | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Puducherry | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Punjab | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Rajasthan | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Sikkim | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Tamil Nadu | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Telangana | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | The Dadra and Nagar Haveli and Daman and Diu | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Tripura | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Uttar Pradesh | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | Uttarakhand | 72 | 0 | 72 |
| PLFS Year (Jul - Jun), 2023 | West Bengal | 72 | 0 | 72 |

### Year × Type Of Areas

| Year | Type Of Areas | Total | Est Missing | Samp Missing |
|------|------|------:|------------:|-------------:|
| PLFS Year (Jul - Jun), 2017 | Rural | 1728 | 1728 | 1728 |
| PLFS Year (Jul - Jun), 2017 | Rural + Urban | 1728 | 1728 | 1728 |
| PLFS Year (Jul - Jun), 2017 | Urban | 1728 | 1728 | 1728 |
| PLFS Year (Jul - Jun), 2022 | Rural | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2022 | Rural + Urban | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2022 | Urban | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2023 | Rural | 840 | 0 | 840 |
| PLFS Year (Jul - Jun), 2023 | Rural + Urban | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2023 | Urban | 864 | 0 | 864 |

### Year × Industry Division Type

| Year | Industry Division Type | Total | Est Missing | Samp Missing |
|------|------|------:|------------:|-------------:|
| PLFS Year (Jul - Jun), 2017 | (014, 016, 017 , 02-99) | 2592 | 2592 | 2592 |
| PLFS Year (Jul - Jun), 2017 | (05-99) | 2592 | 2592 | 2592 |
| PLFS Year (Jul - Jun), 2022 | (05-99) | 2592 | 0 | 2592 |
| PLFS Year (Jul - Jun), 2023 | (05-99) | 2568 | 0 | 2568 |

### Year × Gender

| Year | Gender | Total | Est Missing | Samp Missing |
|------|------|------:|------------:|-------------:|
| PLFS Year (Jul - Jun), 2017 | Female | 1728 | 1728 | 1728 |
| PLFS Year (Jul - Jun), 2017 | Male | 1728 | 1728 | 1728 |
| PLFS Year (Jul - Jun), 2017 | Persons | 1728 | 1728 | 1728 |
| PLFS Year (Jul - Jun), 2022 | Female | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2022 | Male | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2022 | Persons | 864 | 0 | 864 |
| PLFS Year (Jul - Jun), 2023 | Female | 856 | 0 | 856 |
| PLFS Year (Jul - Jun), 2023 | Male | 856 | 0 | 856 |
| PLFS Year (Jul - Jun), 2023 | Persons | 856 | 0 | 856 |

### Year × Enterprise Type

| Year | Enterprise Type | Total | Est Missing | Samp Missing |
|------|------|------:|------------:|-------------:|
| PLFS Year (Jul - Jun), 2017 | Autonomous Bodies | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Cooperative Societies | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Employer's Households | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Govt./ Local Body/ Public Sector Enterprises | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Others | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Proprietary and Partnership | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Public/ Private Limited Company | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2017 | Trust/ Other Non Profit inst | 648 | 648 | 648 |
| PLFS Year (Jul - Jun), 2022 | Autonomous Bodies | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Cooperative Societies | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Employer's Households | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Govt./ Local Body/ Public Sector Enterprises | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Others | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Proprietary and Partnership | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Public/ Private Limited Company | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2022 | Trust/ Other Non Profit inst | 324 | 0 | 324 |
| PLFS Year (Jul - Jun), 2023 | Autonomous Bodies | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Cooperative Societies | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Employer's Households | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Govt./ Local Body/ Public Sector Enterprises | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Others | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Proprietary and Partnership | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Public/ Private Limited Company | 321 | 0 | 321 |
| PLFS Year (Jul - Jun), 2023 | Trust/ Other Non Profit inst | 321 | 0 | 321 |

## Relationship Between the Two Missing Fields

| Condition | Row Count | % of total rows |
|-----------|----------:|----------------:|
| Both missing | 5184 | 16.68 |
| Only Estimated missing | 5160 | 16.6 |
| Only Sample missing | 0 | 0.0 |
| Neither missing | 20736 | 66.72 |

- Sample Workers is missing while Estimated Persons is present: 0 rows
- Estimated Persons is missing while Sample Workers is present: 5160 rows

## Reconciliation Checks
- Estimated Persons missing total matches baseline (10,344): PASS
- Sample Workers missing total matches baseline (5,184): PASS
- Percentage field missing total matches baseline (0): PASS

## Confirmed Patterns
- All missing Estimated Persons and Sample Workers records occur only in years 2017, 2022 and 2023.
- Missingness is present across all states (each state has some missing records).
- Both count fields are missing together for 2 304 rows in 2017, and for none in other years.
- Only Estimated Persons missing (pattern 010) appears in 2017, 2022, 2023.

## Questions Requiring Later Investigation
- Why the two count fields are missing for large subsets of records in the identified years?
- Whether the missingness aligns with any survey‑design documentation.