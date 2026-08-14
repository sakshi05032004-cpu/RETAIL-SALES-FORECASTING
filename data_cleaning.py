# DATA CLEANING - RETAIL SALES FORECASTING PROJECT
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD DATASET
# ============================================================

input_file = "../data/retail_sales.csv"

df = pd.read_csv(input_file)

print("Original Dataset Shape:", df.shape)


# ============================================================
# 2. CHECK DATASET INFORMATION
# ============================================================

print("\nDataset Information:")
print(df.info())

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# 3. CONVERT DATE COLUMN
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)


# ============================================================
# 4. CHECK MISSING VALUES
# ============================================================

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())


# ============================================================
# 5. HANDLE MISSING VALUES
# ============================================================

# Numerical columns
numeric_columns = [
    "Units_Sold",
    "Unit_Price",
    "Discount_Percent",
    "Promotion",
    "Holiday",
    "Sales"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    df[column] = df[column].fillna(
        df[column].median()
    )


# Categorical columns
categorical_columns = [
    "Store_ID",
    "Category"
]

for column in categorical_columns:
    df[column] = df[column].fillna(
        df[column].mode()[0]
    )


# ============================================================
# 6. REMOVE DUPLICATE RECORDS
# ============================================================

duplicate_count = df.duplicated().sum()

print(
    "\nDuplicate Rows Found:",
    duplicate_count
)

df = df.drop_duplicates()


# ============================================================
# 7. HANDLE INVALID VALUES
# ============================================================

# Units sold cannot be negative
df.loc[
    df["Units_Sold"] < 0,
    "Units_Sold"
] = np.nan

# Unit price cannot be negative
df.loc[
    df["Unit_Price"] < 0,
    "Unit_Price"
] = np.nan

# Discount should be between 0 and 100
df.loc[
    (df["Discount_Percent"] < 0) |
    (df["Discount_Percent"] > 100),
    "Discount_Percent"
] = np.nan

# Sales cannot be negative
df.loc[
    df["Sales"] < 0,
    "Sales"
] = np.nan


# Fill values created above
df["Units_Sold"] = df["Units_Sold"].fillna(
    df["Units_Sold"].median()
)

df["Unit_Price"] = df["Unit_Price"].fillna(
    df["Unit_Price"].median()
)

df["Discount_Percent"] = df["Discount_Percent"].fillna(
    df["Discount_Percent"].median()
)

df["Sales"] = df["Sales"].fillna(
    df["Sales"].median()
)


# ============================================================
# 8. REMOVE INVALID DATES
# ============================================================

df = df.dropna(subset=["Date"])


# ============================================================
# 9. STANDARDIZE TEXT COLUMNS
# ============================================================

df["Store_ID"] = (
    df["Store_ID"]
    .astype(str)
    .str.strip()
)

df["Category"] = (
    df["Category"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 10. CONVERT DATA TYPES
# ============================================================

df["Units_Sold"] = df["Units_Sold"].astype(int)

df["Promotion"] = df["Promotion"].astype(int)

df["Holiday"] = df["Holiday"].astype(int)

df["Discount_Percent"] = (
    df["Discount_Percent"].astype(float)
)

df["Unit_Price"] = (
    df["Unit_Price"].astype(float)
)

df["Sales"] = (
    df["Sales"].astype(float)
)


# ============================================================
# 11. SORT DATA BY DATE
# ============================================================

df = df.sort_values(
    by=["Date", "Store_ID", "Category"]
).reset_index(drop=True)


# ============================================================
# 12. FINAL CHECK
# ============================================================

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print(
    "\nDuplicate Rows After Cleaning:",
    df.duplicated().sum()
)

print(
    "\nCleaned Dataset Shape:",
    df.shape
)


# ============================================================
# 13. SAVE CLEANED DATASET
# ============================================================

output_file = "../data/retail_sales_cleaned.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    "\nCleaned dataset saved successfully at:",
    output_file
)


# ============================================================
# 14. DISPLAY SAMPLE DATA
# ============================================================

print("\nCleaned Dataset Preview:")
print(df.head())

print("\nCleaning completed successfully!")
