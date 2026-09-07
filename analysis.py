import pandas as pd


# 1. Load source data
# Column names are on the second row of the source Excel file.
df = pd.read_excel(
    "data/raw/default of credit card clients.xls",
    header=1,
)


# 2. Inspect dataset structure and missing values
print("\n=== Dataset structure and missing values ===")

print("Dataset shape (rows, columns):", df.shape)

print("\nColumn types and non-null counts:")
df.info()

missing_counts = df.isna().sum()
print("\nTotal missing values:", missing_counts.sum())


# 3. Check age range and client IDs
print("\n=== Age range and client IDs ===")

print("Minimum age:", df["AGE"].min())
print("Maximum age:", df["AGE"].max())
print("Unique client IDs:", df["ID"].nunique())
print("Total records:", len(df))


# 4. Check default labels and calculate the default rate
print("\n=== Default labels and default rate ===")

print("\nObserved label counts:")
print(df["default payment next month"].value_counts().sort_index())

default_rate_pct = (
    df["default payment next month"].sum() / len(df) * 100
)

print(f"\nDefault rate: {default_rate_pct:.2f}%")


# 5. Check SEX codes
print("\n=== SEX codes ===")

print("\nObserved code counts:")
print(df["SEX"].value_counts(dropna=False).sort_index())

documented_sex = df["SEX"].isin([1, 2])
undocumented_sex = ~documented_sex

print(
    "\nRecords with undocumented SEX codes:",
    undocumented_sex.sum(),
)


# 6. Check education codes against documentation
print("\n=== Education codes ===")

print("\nObserved code counts:")
print(df["EDUCATION"].value_counts().sort_index())

documented_education = df["EDUCATION"].isin([1, 2, 3, 4])
undocumented_education = ~documented_education

undocumented_education_pct = (
    undocumented_education.sum() / len(df) * 100
)

print(
    "\nRecords with undocumented education codes:",
    undocumented_education.sum(),
)
print(f"Share of all records: {undocumented_education_pct:.2f}%")


# 7. Check marital status codes against documentation
print("\n=== Marital status codes ===")

print("\nObserved code counts:")
print(df["MARRIAGE"].value_counts().sort_index())

documented_marriage = df["MARRIAGE"].isin([1, 2, 3])
undocumented_marriage = ~documented_marriage

undocumented_marriage_pct = (
    undocumented_marriage.sum() / len(df) * 100
)

print(
    "\nRecords with undocumented marital status codes:",
    undocumented_marriage.sum(),
)
print(f"Share of all records: {undocumented_marriage_pct:.2f}%")


# 8. Count records with either undocumented demographic code
print("\n=== Combined EDUCATION and MARRIAGE findings ===")

any_undocumented = undocumented_education | undocumented_marriage
any_undocumented_pct = any_undocumented.sum() / len(df) * 100

print(
    "Records with at least one undocumented code:",
    any_undocumented.sum(),
)
print(f"Share of all records: {any_undocumented_pct:.2f}%")


# 9. Inspect repayment status codes across all six months
print("\n=== Repayment status code checks ===")

repayment_columns = [
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
]
documented_repayment_codes = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
repayment_check_results = []

for repayment_col in repayment_columns:
    print(f"\nObserved code counts: {repayment_col}")
    print(df[repayment_col].value_counts().sort_index())

    documented_repayment = df[repayment_col].isin(
        documented_repayment_codes
    )
    undocumented_repayment = ~documented_repayment

    undocumented_repayment_count = undocumented_repayment.sum()
    undocumented_repayment_pct = (
        undocumented_repayment_count / len(df) * 100
    )

    result = {
        "column": repayment_col,
        "undocumented_count": undocumented_repayment_count,
        "undocumented_pct": undocumented_repayment_pct,
    }
    repayment_check_results.append(result)

repayment_summary = pd.DataFrame(repayment_check_results)

print("\n=== Repayment status summary ===")
print(repayment_summary.round(2).to_string(index=False))

repayment_summary.to_csv(
    "reports/repayment_status_summary.csv",
    index=False,
    float_format="%.2f",
)


# 10. Assess the impact of excluding undocumented PAY_0 codes
# Create subsets for comparison; keep the original dataset unchanged.
print("\n=== Impact of excluding undocumented PAY_0 codes ===")

documented_pay_0 = df["PAY_0"].isin(documented_repayment_codes)
undocumented_pay_0 = ~documented_pay_0

undocumented_pay_0_clients = df[undocumented_pay_0]
documented_pay_0_clients = df[documented_pay_0]

undocumented_pay_0_default_rate_pct = (
    undocumented_pay_0_clients["default payment next month"].sum()
    / len(undocumented_pay_0_clients)
    * 100
)

documented_pay_0_default_rate_pct = (
    documented_pay_0_clients["default payment next month"].sum()
    / len(documented_pay_0_clients)
    * 100
)

print("\nFull dataset:")
print("Records:", len(df))
print(f"Default rate: {default_rate_pct:.2f}%")

print("\nRecords with undocumented PAY_0 codes:")
print("Records:", len(undocumented_pay_0_clients))
print(f"Default rate: {undocumented_pay_0_default_rate_pct:.2f}%")

print("\nRecords with documented PAY_0 codes:")
print("Records:", len(documented_pay_0_clients))
print(f"Default rate: {documented_pay_0_default_rate_pct:.2f}%")


# 11. Inspect credit limit distribution
print("\n=== Credit limit distribution ===")

print("\nDescriptive statistics:")
print(df["LIMIT_BAL"].describe().round(2))

print("\nTen largest credit limits:")
print(df["LIMIT_BAL"].nlargest(10))


# 12. Inspect September bill amount distribution
print("\n=== September bill amount distribution ===")

print(df["BILL_AMT1"].describe().round(2))


# 13. Check negative bill amounts across all six months
bill_columns = [
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
]
bill_check_results = []

for bill_col in bill_columns:
    min_amount = df[bill_col].min()
    negative_bill = df[bill_col] < 0
    negative_bill_count = negative_bill.sum()
    negative_bill_pct = negative_bill_count / len(df) * 100

    result = {
        "column": bill_col,
        "min_amount": min_amount,
        "negative_count": negative_bill_count,
        "negative_pct": negative_bill_pct,
    }
    bill_check_results.append(result)

bill_summary = pd.DataFrame(bill_check_results)

print("\n=== Bill amount summary ===")
print(bill_summary.round(2).to_string(index=False))

bill_summary.to_csv(
    "reports/bill_amount_summary.csv",
    index=False,
    float_format="%.2f",
)


# 14. Inspect September payment amount distribution
print("\n=== September payment amount distribution ===")

print("\nDescriptive statistics:")
print(df["PAY_AMT1"].describe().round(2))

print("\nTen largest September payments:")
print(df["PAY_AMT1"].nlargest(10))


# 15. Check payment amounts across all six months
payment_columns = [
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6",
]
payment_check_results = []

for payment_col in payment_columns:
    # Check payment ranges, negative counts, and zero-payment shares.
    min_amount = df[payment_col].min()
    max_amount = df[payment_col].max()
    negative_payment = df[payment_col] < 0
    zero_payment = df[payment_col] == 0
    zero_pct = zero_payment.sum() / len(df) * 100

    result = {
        "column": payment_col,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "negative_count": negative_payment.sum(),
        "zero_count": zero_payment.sum(),
        "zero_pct": zero_pct,
    }
    payment_check_results.append(result)

payment_summary = pd.DataFrame(payment_check_results)

print("\n=== Payment amount summary ===")
print(payment_summary.round(2).to_string(index=False))

payment_summary.to_csv(
    "reports/payment_amount_summary.csv",
    index=False,
    float_format="%.2f",
)


# 16. Check matching records excluding ID
# The target remains included in the comparison.
print("\n=== Matching records excluding ID ===")

df_without_id = df.drop(columns=["ID"])
duplicate_records = df_without_id.duplicated()

# Include first occurrences when selecting records for inspection.
all_duplicate_records = df_without_id.duplicated(keep=False)
duplicate_clients = df[all_duplicate_records]

duplicate_clients_pct = len(duplicate_clients) / len(df) * 100

print(
    "Duplicate records beyond the first occurrence:",
    duplicate_records.sum(),
)
print(
    "Records involved in duplicate groups:",
    len(duplicate_clients),
)
print(
    "Share of records involved in duplicate groups:",
    f"{duplicate_clients_pct:.2f}%",
)

duplicate_clients.to_csv(
    "reports/duplicate_records_excluding_id.csv",
    index=False,
)


# 17. Confirm report exports
print("\n=== Reports saved ===")

print("reports/repayment_status_summary.csv")
print("reports/bill_amount_summary.csv")
print("reports/payment_amount_summary.csv")
print("reports/duplicate_records_excluding_id.csv")

print("\nChecks completed. Original data remains unchanged.")