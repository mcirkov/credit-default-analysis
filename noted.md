1. Scope and interpretation

These notes document the initial quality review of the loaded dataset: 30,000 records and 25 columns, including `ID` and the target `default payment next month`.

- Findings are based on the analysis outputs recorded during this project. They are not an independent verification of the underlying client information.
- An undocumented code is a value not explained in the reviewed source description. It is not automatically an invalid value or a missing cell.
- No source values have been recoded, capped, imputed, or removed as part of these checks. Boolean masks and filtered tables were created for inspection.
- Unless otherwise stated, record shares use all 30,000 records as the denominator. Default rates use the number of records in the relevant group.
- Monthly counts may include the same records more than once. Do not add them to estimate unique records across months.
- Percentages are rounded to two decimal places for reporting; calculations use unrounded values.

## 2. Dataset structure and completeness

### 2.1 Structure, identifier, and target

- **Check:** Inspected the dataset dimensions, column types, unique IDs, and target frequencies.
- **Findings:** The loaded table has 30,000 records and 25 integer columns. All 30,000 IDs are unique. The target contains 23,364 zeros and 6,636 ones, giving an overall default rate of 22.12%.
- **Current treatment:** Preserve the original table. Retain `ID` for traceability; uniqueness of IDs does not rule out matching values in other columns.

### 2.2 Missing values

- **Check:** Used `isna()` to count missing values in each column and summed the counts across the dataset.
- **Findings:** No pandas-recognized missing values were found.
- **Current treatment:** No missing-value imputation or removal of records due to missing values was performed.
- **Limitation:** This check does not identify numeric codes that may represent unknown information. Category codes were assessed separately.

## 3. Category code checks

The expected code lists below are taken from the UCI source listed in Section 8.

### 3.1 SEX

- **Check:** Inspected value counts, including missing values, and checked for codes outside `[1, 2]`.
- **Findings:** Code `1` occurs in 11,888 records and code `2` in 18,112 records. No missing values or codes outside the expected list were found.
- **Current treatment:** Retain the original values. No corrections are required based on this check.
- **Limitation:** Code-list compliance does not verify the accuracy of the underlying client information or determine whether the variable should be used in a model.

### 3.2 EDUCATION

- **Check:** Compared observed values with the documented codes `[1, 2, 3, 4]`.
- **Findings:** Codes `0`, `5`, and `6` are not explained in the reviewed description. They occur in 14, 280, and 51 records respectively: 345 records in total (1.15%).
- **Current treatment:** Preserve the original values. The Boolean mask `undocumented_education` identifies records outside the documented set.
- **Follow-up:** Seek an authoritative explanation of these codes. If their meanings remain unverified, assess whether an unknown category in a separate analysis column is appropriate; do not overwrite the raw values.

### 3.3 MARRIAGE

- **Check:** Compared observed values with the documented codes `[1, 2, 3]`.
- **Findings:** Code `0` is not explained in the reviewed description and occurs in 54 records (0.18%).
- **Current treatment:** Preserve the original values. The Boolean mask `undocumented_marriage` identifies records outside the documented set.
- **Follow-up:** Seek an authoritative explanation of code `0` before deciding whether to create a separate analysis category.

### 3.4 Combined impact: EDUCATION and MARRIAGE only

- **Check:** Combined the two undocumented-code masks using a Boolean union and checked their overlap.
- **Findings:** 399 records (1.33%) have an undocumented code in at least one of these two columns. No record has an undocumented code in both columns; the union therefore equals 345 + 54.
- **Current treatment:** Retain all flagged records pending clarification.
- **Limitation:** This is not a combined count of all quality findings in the dataset. It excludes repayment codes, bill amounts, and duplicate groups.

## 4. Repayment status codes

### 4.1 Checks across all six months

- **Check:** Compared values in `PAY_0`, `PAY_2`, `PAY_3`, `PAY_4`, `PAY_5`, and `PAY_6` with the documented set `[-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
- **Findings:** Codes `-2` and `0` occur in all six columns but are not explained in the reviewed UCI description.

| Column | Records with undocumented codes | Share of all records (%) |
| --- | ---: | ---: |
| PAY_0 | 17,496 | 58.32 |
| PAY_2 | 19,512 | 65.04 |
| PAY_3 | 19,849 | 66.16 |
| PAY_4 | 20,803 | 69.34 |
| PAY_5 | 21,493 | 71.64 |
| PAY_6 | 21,181 | 70.60 |

- **Current treatment:** Retain all records and preserve `-2` and `0` as separate raw values. Their combined count is used for this documentation check, not as evidence that the codes have the same meaning.
- **Follow-up:** Seek authoritative definitions for both codes. Record the source of any verified interpretation before considering recoding.
- **Output:** `reports/repayment_status_summary.csv`.

### 4.2 PAY_0: sensitivity to excluding undocumented codes

- **Check:** Compared the observed target default rate in the full dataset with rates in the two groups defined by the `PAY_0` code check.

| Group | Records | Default rate (%) |
| --- | ---: | ---: |
| Full dataset | 30,000 | 22.12 |
| PAY_0 is -2 or 0 | 17,496 | 12.88 |
| PAY_0 is in the documented set | 12,504 | 35.05 |

- **Interpretation:** Excluding records with `PAY_0` equal to `-2` or `0` would leave a default rate 12.93 percentage points above the full-dataset rate. This reflects a change in sample composition, not a change in client behaviour or evidence of causation.
- **Current treatment:** Do not exclude these records solely because their codes are undocumented.
- **Limitation:** Each default rate uses its own group size as the denominator. This comparison covers `PAY_0` only and does not establish the meanings of `-2` and `0`.

## 5. Numerical value checks

### 5.1 AGE and LIMIT_BAL

- **Check:** Inspected the age range, credit limit descriptive statistics, and ten largest credit limits.
- **Findings:** Recorded ages range from 21 to 79. Credit limits range from 10,000 to 1,000,000, with a median of 140,000 and a mean of 167,484.32.
- **Current treatment:** Retain the observed values. Large credit limits are not classified as errors solely because they are rare.
- **Limitation:** Range checks do not verify individual values against original client records.

### 5.2 BILL_AMT1–BILL_AMT6: negative bill amounts

- **Check:** Inspected the minimum and calculated the count and share of negative values in each bill amount column. Also reviewed descriptive statistics for `BILL_AMT1`.

| Column | Minimum amount | Negative count | Negative share (%) |
| --- | ---: | ---: | ---: |
| BILL_AMT1 | -165,580 | 590 | 1.97 |
| BILL_AMT2 | -69,777 | 669 | 2.23 |
| BILL_AMT3 | -157,264 | 655 | 2.18 |
| BILL_AMT4 | -170,000 | 675 | 2.25 |
| BILL_AMT5 | -81,334 | 655 | 2.18 |
| BILL_AMT6 | -339,603 | 688 | 2.29 |

- **Interpretation:** Negative amounts may represent credit balances, for example from overpayments. This is a hypothesis, not a confirmed explanation for this dataset.
- **Current treatment:** Retain the original values. Do not classify negative amounts as errors solely because they are below zero.
- **Follow-up:** Clarify the meaning of negative amounts using authoritative sources and inspect the corresponding records, particularly the largest negative amounts.
- **Output:** `reports/bill_amount_summary.csv`.

### 5.3 PAY_AMT1–PAY_AMT6: payment amounts

- **Check:** Inspected minima and maxima, counted negative and zero values, and calculated zero-value shares in all six payment amount columns. Also reviewed descriptive statistics and the ten largest values for `PAY_AMT1`.

| Column | Minimum amount | Maximum amount | Negative count | Zero count | Zero share (%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| PAY_AMT1 | 0 | 873,552 | 0 | 5,249 | 17.50 |
| PAY_AMT2 | 0 | 1,684,259 | 0 | 5,396 | 17.99 |
| PAY_AMT3 | 0 | 896,040 | 0 | 5,968 | 19.89 |
| PAY_AMT4 | 0 | 621,000 | 0 | 6,408 | 21.36 |
| PAY_AMT5 | 0 | 426,529 | 0 | 6,703 | 22.34 |
| PAY_AMT6 | 0 | 528,666 | 0 | 7,173 | 23.91 |

- **Interpretation:** A zero payment alone does not establish delinquency or default. Large payments warrant inspection but are not necessarily errors.
- **Current treatment:** Retain all original values. Do not infer the target from zero payments or remove or cap large payments without further investigation.
- **Follow-up:** Inspect the largest payments alongside credit limits, bill amounts, and repayment histories, accounting for the timing of each variable. Do not assume a payment must match the bill amount with the same numeric suffix.
- **Output:** `reports/payment_amount_summary.csv`.

## 6. Matching records excluding ID

- **Check:** Compared all columns except `ID`, including the target. Used `duplicated()` to count repeats beyond the first occurrence and `duplicated(keep=False)` to identify all participating records.
- **Findings:** Found 35 repeats beyond first occurrences and 70 participating records (0.23% of the dataset). The IDs themselves are unique.
- **Current treatment:** Retain all records. Exported the matching records with their IDs for inspection. Matching recorded values do not establish that the records represent the same client.
- **Follow-up:** Inspect the matching records and seek information about data collection to distinguish possible accidental duplication from distinct clients with identical recorded characteristics.
- **Modelling follow-up:** Before model evaluation, also check for identical predictor profiles excluding both `ID` and the target. Assess how matching profiles should be handled when splitting the data; this additional check has not yet been performed.

## 7. Review status and outstanding decisions

The initial checks are documented; unresolved interpretations remain open. Completion of these checks does not establish that every value is accurate or that all modelling preparation is complete.

Before finalising preprocessing and model evaluation:

1. Resolve or explicitly document uncertainty around undocumented category codes.
2. Investigate negative bill amounts and unusually large payments without assuming they are errors.
3. Review matching records and determine an appropriate evaluation split strategy.
4. Record any later transformations separately, with their rationale and affected counts, while preserving the raw data.

## 8. Source and evidence

- **Variable definitions:** [UCI Machine Learning Repository — Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients), section “Additional Variable Information”. Dataset DOI: [10.24432/C55S3H](https://doi.org/10.24432/C55S3H).
- **Units and timing:** The source describes monetary amounts in NT dollars and the six monthly histories from April to September 2005. The monthly column sequences used here run from September back to April.
- **Observed counts and statistics:** Project analysis outputs reviewed during this work, rather than counts quoted from the source description. The restructuring of this document did not rerun the dataset analysis.
- **Generated summaries:** The three CSV summary paths are listed in the relevant sections. A separate export of the 70 matching records was also created; its exact filename should be checked in the project before adding a reference here.
