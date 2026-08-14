# MODEL TRAINING - RETAIL SALES FORECASTING
# ============================================================

import pandas as pd
import numpy as np
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# 1. LOAD FEATURE-ENGINEERED DATA
# ============================================================

input_file = "../data/retail_sales_features.csv"

df = pd.read_csv(input_file)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

print("Dataset Loaded Successfully")
print("Shape:", df.shape)


# ============================================================
# 2. DEFINE TARGET
# ============================================================

target = "Sales"


# ============================================================
# 3. SELECT FEATURES
# ============================================================

features = [
    "Store_ID",
    "Category",
    "Units_Sold",
    "Unit_Price",
    "Discount_Percent",
    "Promotion",
    "Holiday",

    "Year",
    "Month",
    "Day",
    "DayOfWeek",
    "Quarter",
    "WeekOfYear",
    "DayOfYear",

    "IsWeekend",
    "IsMonthStart",
    "IsMonthEnd",

    "Lag_1_Sales",
    "Lag_7_Sales",
    "Lag_30_Sales",

    "Rolling_7_Sales",
    "Rolling_30_Sales",
    "Rolling_7_Std",

    "Sales_Growth_1D",
    "Sales_Growth_7D",

    "Gross_Sales",
    "Discount_Amount",
    "Promotion_Discount",

    "Month_Sin",
    "Month_Cos",
    "DayOfWeek_Sin",
    "DayOfWeek_Cos"
]


X = df[features]
y = df[target]


# ============================================================
# 4. TIME-BASED TRAIN TEST SPLIT
# ============================================================

split_date = df["Date"].quantile(0.80)

train = df[df["Date"] <= split_date]
test = df[df["Date"] > split_date]

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

print("\nTraining Data:", X_train.shape)
print("Testing Data:", X_test.shape)
print("Split Date:", split_date)


# ============================================================
# 5. DEFINE CATEGORICAL AND NUMERICAL FEATURES
# ============================================================

categorical_features = [
    "Store_ID",
    "Category"
]

numeric_features = [
    feature
    for feature in features
    if feature not in categorical_features
]


# ============================================================
# 6. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ============================================================
# 7. DEFINE MODELS
# ============================================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Decision Tree":
        DecisionTreeRegressor(
            max_depth=15,
            random_state=42
        ),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
}


# ============================================================
# 8. TRAIN AND EVALUATE MODELS
# ============================================================

results = {}

trained_models = {}

for name, model in models.items():

    print("\nTraining:", name)

    pipeline = Pipeline([
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ])

    # Train model
    pipeline.fit(
        X_train,
        y_train
    )

    # Prediction
    predictions = pipeline.predict(
        X_test
    )

    # Evaluation
    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    results[name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    trained_models[name] = pipeline

    print("MAE :", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R²  :", round(r2, 4))


# ============================================================
# 9. MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(results).T

results_df = results_df.sort_values(
    by="RMSE"
)

print("\n========================================")
print("MODEL COMPARISON")
print("========================================")

print(results_df)


# ============================================================
# 10. SELECT BEST MODEL
# ============================================================

best_model_name = results_df.index[0]

best_model = trained_models[
    best_model_name
]

print(
    "\nBest Model:",
    best_model_name
)


# ============================================================
# 11. BEST MODEL PERFORMANCE
# ============================================================

best_mae = results_df.loc[
    best_model_name,
    "MAE"
]

best_rmse = results_df.loc[
    best_model_name,
    "RMSE"
]

best_r2 = results_df.loc[
    best_model_name,
    "R2"
]

print("\nBest Model Performance")
print("----------------------")

print(
    "MAE :",
    round(best_mae, 2)
)

print(
    "RMSE:",
    round(best_rmse, 2)
)

print(
    "R²  :",
    round(best_r2, 4)
)


# ============================================================
# 12. CREATE PREDICTION DATASET
# ============================================================

predictions = best_model.predict(
    X_test
)

forecast_results = test[
    [
        "Date",
        "Store_ID",
        "Category",
        "Sales"
    ]
].copy()

forecast_results[
    "Predicted_Sales"
] = predictions

forecast_results[
    "Error"
] = (
    forecast_results["Sales"]
    - forecast_results["Predicted_Sales"]
)


# ============================================================
# 13. SAVE MODEL RESULTS
# ============================================================

results_df.to_csv(
    "../data/model_comparison.csv"
)

forecast_results.to_csv(
    "../data/sales_forecast_results.csv",
    index=False
)


# ============================================================
# 14. SAVE BEST MODEL
# ============================================================

model_file = "../data/best_sales_forecasting_model.pkl"

joblib.dump(
    best_model,
    model_file
)

print(
    "\nBest model saved at:",
    model_file
)


# ============================================================
# 15. SAVE FEATURE LIST
# ============================================================

with open(
    "../data/model_features.txt",
    "w"
) as file:

    for feature in features:
        file.write(
            feature + "\n"
        )


# ============================================================
# 16. FINAL OUTPUT
# ============================================================

print("\n========================================")
print("MODEL TRAINING COMPLETED")
print("========================================")

print(
    "Best Model:",
    best_model_name
)

print(
    "RMSE:",
    round(best_rmse, 2)
)

print(
    "MAE:",
    round(best_mae, 2)
)

print(
    "R² Score:",
    round(best_r2, 4)
)

print(
    "\nForecast results saved successfully."
)
