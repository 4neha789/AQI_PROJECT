import sys
import os

# ✅ FIX PROJECT PATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import hopsworks
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

PROJECT_NAME = "aqi_karachi_project"

def evaluate():
    print("📊 Model evaluation started")

    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()

    df = fs.get_feature_group("aqi_features", version=4).read()

    # ❌ REMOVE NON-NUMERIC COLUMNS
    drop_cols = ["aqi", "dt", "city", "timestamp"]
    X = df.drop(columns=drop_cols, errors="ignore")
    y = df["aqi"]

    print("📌 Training features:", list(X.columns))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = {}

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    results["LinearRegression"] = mean_absolute_error(
        y_test, lr.predict(X_test)
    )

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    results["RandomForest"] = mean_absolute_error(
        y_test, rf.predict(X_test)
    )

    xgb_model = xgb.XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    xgb_model.fit(X_train, y_train)
    results["XGBoost"] = mean_absolute_error(
        y_test, xgb_model.predict(X_test)
    )

    results_df = pd.DataFrame(
        results.items(), columns=["Model", "MAE"]
    ).sort_values("MAE")

    print("\n🏆 Model Comparison")
    print(results_df)

    print(f"\n✅ Best Model: {results_df.iloc[0]['Model']}")

if __name__ == "__main__":
    evaluate()
