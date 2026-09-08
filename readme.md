# Credit Default Analysis

**Status: Work in progress — initial data quality review completed; exploratory analysis started.**

A learning and portfolio project exploring credit card default data with Python and pandas.

The project currently focuses on understanding the dataset, identifying data quality concerns, and documenting decisions before modelling. Later stages will cover exploratory analysis, a baseline classification model, and model evaluation.

## Objectives

- Review the structure, completeness, and consistency of the dataset.
- Investigate undocumented category codes and unusual numerical values.
- Assess how data exclusion decisions can change the analysed sample.
- Explore relationships between client characteristics, repayment history, and subsequent default.
- Build and evaluate a baseline model in a later stage.

## Dataset

The project uses **Default of Credit Card Clients** from the UCI Machine Learning Repository.

- **Records:** 30,000
- **Predictors:** 23
- **Additional columns:** client ID and the target variable
- **Payment history:** April–September 2005
- **Target:** `default payment next month`
- **Target values:** `1` = default; `0` = no default
- **Monetary units:** New Taiwan dollars (NT$)

Source: [UCI — Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)

Citation: Yeh, I. (2009). *Default of Credit Card Clients* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.

This is a public historical dataset, not data from a prospective employer or a current lending portfolio.

## Work Completed

### Data quality checks

- Inspected dataset dimensions, data types, age range, and ID uniqueness.
- Checked for missing values across all columns.
- Reviewed the target distribution.
- Compared demographic and repayment status codes with the reviewed documentation.
- Inspected credit limits, negative bill amounts, and zero or negative payments.
- Identified matching records after excluding ID from the comparison.
- Exported inspection reports and documented findings and treatment decisions.

### Initial findings

| Check | Result |
| --- | --- |
| Missing values | No pandas-recognized missing values |
| Client IDs | 30,000 unique IDs |
| Overall default rate | 22.12% |
| EDUCATION | 345 records with undocumented codes (1.15%) |
| MARRIAGE | 54 records with an undocumented code (0.18%) |
| EDUCATION or MARRIAGE | 399 records flagged (1.33%); no overlap |
| SEX | Only expected codes 1 and 2 observed |
| Repayment status | Codes -2 and 0 are not explained in the reviewed UCI description |
| Negative bill amounts | Present in all six monthly columns: 1.97%–2.29% per column |
| Negative payments | None found |
| Zero payments | 17.50%–23.91% of records per monthly column |
| Matching records excluding ID | 35 repeats beyond first occurrences; 70 participating records (0.23%) |

Monthly percentages are calculated separately and must not be added to estimate unique clients across months.

### Sensitivity to excluding undocumented PAY_0 codes

The observed default rate differs substantially between groups defined by the documentation check:

| Group | Records | Default rate |
| --- | ---: | ---: |
| Full dataset | 30,000 | 22.12% |
| PAY_0 equal to -2 or 0 | 17,496 | 12.88% |
| PAY_0 in the documented code set | 12,504 | 35.05% |

Excluding records with `PAY_0` equal to `-2` or `0` would increase the remaining sample's default rate by **12.93 percentage points** relative to the full dataset.

This is a change in sample composition, not evidence of a causal effect. No records were removed for this comparison.

## Data Treatment

Original values are retained at the current stage.

- Undocumented codes are not automatically treated as errors.
- Negative bill amounts are not automatically removed or replaced.
- Zero payments are not used on their own to infer delinquency or default.
- Large amounts are flagged for investigation rather than automatically capped.
- Matching values under different IDs do not establish that records represent the same client.
- No imputation, recoding, capping, or record removal has been applied.

Detailed findings, limitations, and follow-up actions are recorded in [noted.md](noted.md).

## Repository Structure

```text
.
├── analysis.py
├── noted.md
├── README.md
├── data/
│   └── raw/
│       └── default of credit card clients.xls
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
└── reports/
    ├── repayment_status_summary.csv
    ├── bill_amount_summary.csv
    ├── payment_amount_summary.csv
    └── duplicate_records_excluding_id.csv
```

- **analysis.py:** data quality checks and CSV report generation.
- **noted.md:** findings, interpretations, and data treatment decisions.
- **notebooks/:** exploratory analysis, currently in development.
- **reports/:** generated summaries and records exported for inspection.
- **data/raw/:** original source file.

## Running the Project

### 1. Prepare the data

Download the original Excel file from the UCI dataset page and place it at:

```text
data/raw/default of credit card clients.xls
```

Keep the original filename. The script uses the second Excel row as column headers.

### 2. Prepare a Python environment

Create and activate a virtual environment.

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the packages used by the project:

```bash
python -m pip install pandas xlrd ipykernel
```

An exact, tested dependency specification will be added as the project develops.

### 3. Run the data quality checks

Ensure that the `reports` folder exists, then run the script **from the repository root**:

```bash
python analysis.py
```

The script prints the findings and writes four CSV reports to `reports/`.

Running it again replaces these generated CSV files. The original Excel file is not modified.

### 4. Open the notebook

Open `notebooks/01_exploratory_analysis.ipynb` in VS Code with notebook support and select the project's `.venv` as the kernel.

The notebook currently uses a data path beginning with `../data/`, which assumes its working directory is `notebooks/`.

Run cells from top to bottom. Exploratory analysis is still in progress.

## Planned Work

- [x] Initial data quality checks
- [x] CSV inspection reports
- [x] Documentation of findings and current treatment decisions
- [ ] Exploratory analysis of default rates across repayment status groups
- [ ] Visualisation of distributions and relationships
- [ ] Review of matching predictor profiles before data splitting
- [ ] Documented preprocessing and feature selection decisions
- [ ] Baseline classification model
- [ ] Evaluation of discrimination and calibration
- [ ] Discussion of limitations and final conclusions
- [ ] Tested dependency specification and reproducibility review

## Limitations

- The data represents a historical population and does not establish performance on current borrowers or other markets.
- Some category meanings remain unresolved.
- Valid-looking values have not been verified against original client records.
- Observed associations do not establish causation.
- No predictive model has been trained or evaluated in this project yet.
- This project is an educational analysis, not a production credit decision system.