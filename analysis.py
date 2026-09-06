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
