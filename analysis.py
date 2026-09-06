import pandas as pd

df = pd.read_excel("data/raw/default of credit card clients.xls", header=1)
print(df.head())
print(df.shape)
df.info()
print(df["AGE"].min(), df["AGE"].max())
print(df["ID"].nunique())
print(df["default payment next month"].value_counts())
default_rate_pct = df["default payment next month"].sum() / len(df) * 100
print(default_rate_pct)
print(df["EDUCATION"].value_counts())
documented_education = df["EDUCATION"].isin([1, 2, 3, 4])
undocumented_education = ~documented_education
print(undocumented_education.sum() / len(df) * 100)
print(df["MARRIAGE"].value_counts())
documented_marriage = df["MARRIAGE"].isin([1, 2, 3])
undocumented_marriage = ~documented_marriage
print(undocumented_marriage.sum() / len(df) * 100)
any_undocumented = undocumented_education | undocumented_marriage
print(any_undocumented.sum())
