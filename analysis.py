import pandas as pd

# Load source data
# Column names are on the second row of the source Excel file.
df = pd.read_excel(
    "data/raw/default of credit card clients.xls",
    header=1
)


# Inspect dataset structure
print("\n=== Dataset Structure ===")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape (rows, columns):", df.shape)

print("\nColumn types and non-null counts:")
df.info()


# Check age range and client IDs
print("\n=== Age range and client IDs ===")

print("Minimum age:", df["AGE"].min())
print("Maximum age:", df["AGE"].max())
print("Unique client IDs:", df["ID"].nunique())
print("Total records:", len(df))


# Check default labels and calculate default rate
print("\n=== Default labels and default rate ===")

print("\nDefault label counts:")
print(df["default payment next month"].value_counts().sort_index())

default_rate_pct = (
    df["default payment next month"].sum() / len(df) * 100
)

print(f"Default rate: {default_rate_pct:.2f}%")


# Check education codes against documentation
print("\n=== Education codes ===")

print("\nObserved code counts:")
print(df["EDUCATION"].value_counts().sort_index())

documented_education = df["EDUCATION"].isin([1, 2, 3, 4])
undocumented_education = ~documented_education

undocumented_education_pct = (
    undocumented_education.sum() / len(df) * 100
)

print("\nClients with undocumented education codes:",
      undocumented_education.sum())
print(f"Share of all clients: {undocumented_education_pct:.2f}%")


# Check marital status codes against documentation
print("\n=== Marital status codes ===")

print("\nObserved code counts:")
print(df["MARRIAGE"].value_counts().sort_index())

documented_marriage = df["MARRIAGE"].isin([1, 2, 3])
undocumented_marriage = ~documented_marriage

undocumented_marriage_pct = (
    undocumented_marriage.sum() / len(df) * 100
)

print("\nClients with undocumented marital status codes:",
      undocumented_marriage.sum())
print(f"Share of all clients: {undocumented_marriage_pct:.2f}%")


# Count clients with any undocumented demographic code
print("\n=== Combined education and marital status findings ===")

any_undocumented = undocumented_education | undocumented_marriage
any_undocumented_pct = any_undocumented.sum() / len(df) * 100

print("Clients with at least one undocumented code:",
      any_undocumented.sum())
print(f"Share of all clients: {any_undocumented_pct:.2f}%")


# Inspect September repayment status codes
print("\n=== September repayment status: PAY_0 ===")

print("\nObserved code counts:")
print(df["PAY_0"].value_counts().sort_index())

# Codes explicitly described in the reviewed UCI documentation.
documented_pay_0 = df["PAY_0"].isin([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9])
undocumented_pay_0 = ~documented_pay_0

undocumented_pay_0_pct = (
    undocumented_pay_0.sum() / len(df) * 100
)

print("\nClients with undocumented codes:", undocumented_pay_0.sum())
print(f"Share of all clients: {undocumented_pay_0_pct:.2f}%")


# Assess the impact of excluding undocumented PAY_0 codes
# Create subsets for comparison; keep the original dataset unchanged.
print("\n=== Impact of excluding undocumented PAY_0 codes ===")

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
print("Clients:", len(df))
print(f"Default rate: {default_rate_pct:.2f}%")

print("\nClients with undocumented PAY_0 codes:")
print("Clients:", len(undocumented_pay_0_clients))
print(f"Default rate: {undocumented_pay_0_default_rate_pct:.2f}%")

print("\nClients with documented PAY_0 codes:")
print("Clients:", len(documented_pay_0_clients))
print(f"Default rate: {documented_pay_0_default_rate_pct:.2f}%")

# Inspect repayment status codes across all six months
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
    print(f"\n--- {repayment_col} ---")

    print("Observed code counts:")
    print(df[repayment_col].value_counts().sort_index())

    # Identify values outside the documented code list
    documented_repayment = df[repayment_col].isin(
        documented_repayment_codes
    )
    undocumented_repayment = ~documented_repayment

    undocumented_repayment_count = undocumented_repayment.sum()
    undocumented_repayment_pct = (
        undocumented_repayment_count / len(df) * 100
    )

    print(
        "Clients with undocumented codes:",
        undocumented_repayment_count,
    )
    print(f"Share of all clients: {undocumented_repayment_pct:.2f}%")

    # Store the results for this column
    result = {
        "column": repayment_col,
        "undocumented_count": undocumented_repayment_count,
        "undocumented_pct": undocumented_repayment_pct,
    }
    repayment_check_results.append(result)

# Build and export the summary after checking all columns
repayment_summary = pd.DataFrame(repayment_check_results)

print("\n=== Repayment status summary ===")
print(repayment_summary.round(2).to_string(index=False))

repayment_summary.to_csv(
    "reports/repayment_status_summary.csv",
    index=False,
    float_format="%.2f",
)


# Inspect credit limit distribution
print("\n=== Credit limit distribution ===")

print("\nDescriptive statistics:")
print(df["LIMIT_BAL"].describe().round(2))

print("\nTen largest credit limits:")
print(df["LIMIT_BAL"].nlargest(10))


# Inspect September bill amount distribution
print("\n=== September bill amount distribution ===")

print("\nDescriptive statistics:")
print(df["BILL_AMT1"].describe().round(2))


# Check negative bill amounts across all six months
print("\n=== Negative bill amount checks ===")

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
    print(f"\n--- {bill_col} ---")

    # Calculate the minimum and the share of negative values
    min_amount = df[bill_col].min()
    negative_bill = df[bill_col] < 0
    negative_bill_count = negative_bill.sum()
    negative_bill_pct = negative_bill_count / len(df) * 100

    print("Minimum bill amount:", min_amount)
    print("Clients with negative bill amounts:", negative_bill_count)
    print(f"Share of all clients: {negative_bill_pct:.2f}%")

    # Store the results for this column
    result = {
        "column": bill_col,
        "min_amount": min_amount,
        "negative_count": negative_bill_count,
        "negative_pct": negative_bill_pct,
    }
    bill_check_results.append(result)

# Build and export the summary after checking all columns
bill_summary = pd.DataFrame(bill_check_results)

print("\n=== Bill amount summary ===")
print(bill_summary.round(2).to_string(index=False))

bill_summary.to_csv(
    "reports/bill_amount_summary.csv",
    index=False,
    float_format="%.2f",
)