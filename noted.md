# Data quality notes

## EDUCATION

- Check: Compared the observed values with the codes listed in the UCI documentation: 1, 2, 3, and 4.

- Finding: The column contains three undocumented codes: 0, 5, and 6.

- Affected records: 345 clients (1.15% of the dataset).

- Current treatment: Original values remain unchanged. A Boolean mask named undocumented_education flags records with
codes outside the documented set.

- Follow-up: Review the source documentation and authors' materials for explanations of these codes. If their meaning cannot be verified, consider assigning an "Unknown" category in a separate analysis column while preserving the original values.

## MARRIAGE

- Check: Compared the observed values with the codes listed in the UCI documentation: 1, 2, and 3.

- Finding: The column contains one undocumented code: 0.

- Affected records: 54 clients (0.18% of the dataset).

- Current treatment: Original values remain unchanged. A Boolean mask named undocumented_marriage flags records with codes outside the documented set.

- Follow-up: Review the source documentation and authors' materials to clarify the meaning of code 0. If its meaning cannot be verified, consider assigning an "Unknown" category in a separate analysis column while preserving the original values.

## PAY_0: impact of excluding undocumented codes

- Check: Compared the observed values with the codes listed in the UCI documentation: -1, 1, 2, 3, 4, 5, 6, 7, 8, and 9.

- Finding: The column contains two codes not explained in the reviewed UCI description: -2 and 0.

- Affected records: 17,496 clients (58.32% of the dataset).

- Impact assessment: The default rate is 12.88% among clients with these codes, compared with 22.12% in the full dataset. Excluding these records would leave 12,504 clients with a default rate of 35.05%, an increase of 12.93 percentage points relative to the full dataset. This reflects a change in sample composition, not a change in client behaviour.

- Current treatment: Retain all records and preserve codes -2 and 0 as separate values. Their absence from the reviewed description is not sufficient evidence that the records are incorrect.

- Follow-up: Review the source documentation and authors' materials to clarify the meaning of both codes. Document any verified definitions and their source before deciding whether recoding is appropriate.

## BILL_AMT1–BILL_AMT6: negative bill amounts

- Check: Inspected the minimum bill amount and calculated the count and share of negative values in each of the six bill amount columns.
- Findings: Negative bill amounts occur in all six columns, affecting between 1.97% and 2.29% of records per column. The lowest observed amount is -339,603 in BILL_AMT6.
- Interpretation: Negative bill amounts may represent credit balances, for example due to overpayments. This is a possible explanation, not a confirmed interpretation for this dataset.
- Current treatment: Retain the original values. Negative amounts are not classified as errors solely because they are below zero.
- Follow-up: Review the source documentation to clarify the meaning of negative bill amounts and inspect the corresponding client records, particularly those with the largest negative amounts.
- Output: reports/bill_amount_summary.csv

## PAY_AMT1–PAY_AMT6: payment amounts

- Check: Inspected the minimum and maximum payment amounts, counted negative and zero values, and calculated the share of zero values in each of the six payment amount columns.
- Findings: No negative payment amounts were found. Zero payment amounts occur in all six columns, affecting between 17.50% and 23.91% of records per column. The largest observed payment is 1,684,259 in PAY_AMT2.
- Interpretation: A zero payment amount alone does not establish delinquency or default. Large payment amounts warrant further investigation but are not necessarily data errors.
- Current treatment: Retain all original values. Do not remove zero payments or classify them as defaults. Do not remove or cap large payments without further investigation.
- Follow-up: Inspect the largest payments alongside the corresponding clients' credit limits, bill amounts, and repayment history, taking the timing of each variable into account.
- Output: reports/payment_amount_summary.csv

### Scope of the reported percentages

- All percentages above use the full dataset of 30,000 records as the denominator and are calculated separately for each column.
- The same client may appear in multiple monthly counts. These counts and percentages must not be added together to estimate the number or share of unique clients affected across all six months.

## Combined impact

- Clients affected by at least one issue: 399 (1.33% of the dataset), counted using the union of the two Boolean masks.

- Clients affected by both issues: 0. The combined count equals the sum of the individual counts (345 + 54), indicating no overlap.

- Interpretation: These findings concern undocumented category codes, not missing cells detected by pandas. They do not establish that the records are incorrect.

- Current decision: Retain all affected records while the category definitions are investigated.


## Source

- UCI Machine Learning Repository — Default of Credit Card Clients, section “Additional Variable Information”.