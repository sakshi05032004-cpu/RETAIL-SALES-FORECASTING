# FEATURE ENGINEERING - RETAIL SALES FORECASTING
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

input_file = "../data/retail_sales_cleaned.csv"

df = pd.read_csv(input_file)

print("Dataset Loaded Successfully")
print("Original Shape:", df.shape)


# ============================================================
# 2. CONVERT DATE
# ============================================================

df["Date"] = pd.to_datetime(df["Date"])

# Sort data before creating time-series features
df = df.sort_values(
    ["Store_ID", "Category", "Date"]
).reset_index(drop=True)


# ============================================================
# 3. TIME-BASED FEATURES
# ============================================================

df["Year"] = df["Date"].dt.year

df["Month"] = df["Date"].dt.month

df["Day"] = df["Date"].dt.day

df["DayOfWeek"] = df["Date"].dt.dayofweek

df["Quarter"] = df["Date"].dt.quarter

df["WeekOfYear"] = (
    df["Date"].dt.isocalendar().week.astype(int)
)

df["DayOfYear"] = (
    df["Date"].dt.dayofyear
)


# ============================================================
# 4. WEEKEND FEATURE
# ============================================================

df["IsWeekend"] = (
    df["DayOfWeek"] >= 5
).astype(int)


# ============================================================
# 5. MONTH START / MONTH END FEATURES
# ============================================================

df["IsMonthStart"] = (
    df["Date"].dt.is_month_start.astype(int)
)

df["IsMonthEnd"] = (
    df["Date"].dt.is_month_end.astype(int)
)


# ============================================================
# 6. LAG FEATURES
# ============================================================

group = df.groupby(
    ["Store_ID", "Category"]
)["Sales"]

# Previous day's sales
df["Lag_1_Sales"] = group.shift(1)

# Sales 7 days earlier
df["Lag_7_Sales"] = group.shift(7)

# Sales 30 days earlier
df["Lag_30_Sales"] = group.shift(30)


# ============================================================
# 7. ROLLING SALES FEATURES
# ============================================================

# 7-day moving average
df["Rolling_7_Sales"] = (
    df.groupby(
        ["Store_ID", "Category"]
    )["Sales"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(window=7)
        .mean()
    )
)

# 30-day moving average
df["Rolling_30_Sales"] = (
    df.groupby(
        ["Store_ID", "Category"]
    )["Sales"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(window=30)
        .mean()
    )
)


# ============================================================
# 8. ROLLING SALES STANDARD DEVIATION
# ============================================================

df["Rolling_7_Std"] = (
    df.groupby(
        ["Store_ID", "Category"]
    )["Sales"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(window=7)
        .std()
    )
)


# ============================================================
# 9. SALES GROWTH FEATURES
# ============================================================

df["Sales_Growth_1D"] = (
    df["Sales"] /
    df["Lag_1_Sales"] - 1
)

df["Sales_Growth_7D"] = (
    df["Sales"] /
    df["Lag_7_Sales"] - 1
)


# ============================================================
# 10. PRICE × QUANTITY FEATURE
# ============================================================

df["Gross_Sales"] = (
    df["Units_Sold"] *
    df["Unit_Price"]
)


# ============================================================
# 11. DISCOUNT IMPACT
# ============================================================

df["Discount_Amount"] = (
    df["Gross_Sales"] *
    df["Discount_Percent"] / 100
)


# ============================================================
# 12. PROMOTION × DISCOUNT FEATURE
# ============================================================

df["Promotion_Discount"] = (
    df["Promotion"] *
    df["Discount_Percent"]
)


# ============================================================
# 13. SEASONAL FEATURES
# ============================================================

# Cyclical month encoding
df["Month_Sin"] = np.sin(
    2 * np.pi * df["Month"] / 12
)

df["Month_Cos"] = np.cos(
    2 * np.pi * df["Month"] / 12
)

# Cyclical day-of-week encoding
df["DayOfWeek_Sin"] = np.sin(
    2 * np.pi * df["DayOfWeek"] / 7
)

df["DayOfWeek_Cos"] = np.cos(
    2 * np.pi * df["DayOfWeek"] / 7
)


# ============================================================
# 14. HANDLE INFINITE VALUES
# ============================================================

df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)


# ============================================================
# 15. REMOVE ROWS CREATED BY LAG/ROLLING FEATURES
# ============================================================

df = df.dropna().reset_index(drop=True)


# ============================================================
# 16. FINAL SORTING
# ============================================================

df = df.sort_values(
    ["Date", "Store_ID", "Category"]
).reset_index(drop=True)


# ============================================================
# 17. DISPLAY FEATURE INFORMATION
# ============================================================

print("\nFeature Engineering Completed")

print("Final Shape:", df.shape)

print("\nTotal Features:", len(df.columns))

print("\nFeatures Created:")
print(df.columns.tolist())


# ============================================================
# 18. SAVE FEATURE-ENGINEERED DATASET
# ============================================================

output_file = "../data/retail_sales_features.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    "\nFeature-engineered dataset saved at:"
)

print(output_file)


# ============================================================
# 19. PREVIEW DATA
# ============================================================

print("\nFeature-Engineered Dataset Preview:")

print(df.head())

print("\nFeature Engineering Completed Successfully!")
