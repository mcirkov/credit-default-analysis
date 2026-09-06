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

## Combined impact

- Clients affected by at least one issue: 399 (1.33% of the dataset), counted using the union of the two Boolean masks.

- Clients affected by both issues: 0. The combined count equals the sum of the individual counts (345 + 54), indicating no overlap.

- Interpretation: These findings concern undocumented category codes, not missing cells detected by pandas. They do not establish that the records are incorrect.

- Current decision: Retain all affected records while the category definitions are investigated.


## Source

- UCI Machine Learning Repository — Default of Credit Card Clients, section “Additional Variable Information”.