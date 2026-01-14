import sys
import os
import pandas as pd
import hopsworks
import joblib
from datetime import datetime

# Fix project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

PROJECT_NAME = "aqi_karachi_project"
MODEL_NAME = "aqi_lr_model"
MODEL_VERSION = 1

def predict_next_3_days():
    print("🔮 Predicting AQI for next 3 days")

    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()
    mr = project.get_model_registry()

    # Load latest features
    df = fs.get_feature_group("aqi_features", version=4).read()
    latest = df.sort_values("dt").iloc[-1]

    # 🔥 CORRECT MODEL LOADING (FIX)
    model_meta = mr.get_model(MODEL_NAME, version=MODEL_VERSION)
    model_dir = model_meta.download()
    model = joblib.load(os.path.join(model_dir, f"{MODEL_NAME}.pkl"))

    future_rows = []
    base_dt = int(latest["dt"])

    for i in range(1, 73):  # next 72 hours
        future_dt = base_dt + i * 3600
        ts = datetime.fromtimestamp(future_dt)

        row = latest.copy()
        row["dt"] = future_dt
        row["hour"] = ts.hour
        row["day"] = ts.day
        row["month"] = ts.month

        future_rows.append(row)

    future_df = pd.DataFrame(future_rows)

    X_future = future_df.drop(
        columns=["aqi", "dt", "city", "timestamp"],
        errors="ignore"
    )

    future_df["predicted_aqi"] = model.predict(X_future)
    future_df["datetime"] = pd.to_datetime(future_df["dt"], unit="s")
    

    print("\n📈 AQI Forecast (Next 3 Days)")
    print(future_df[["datetime", "predicted_aqi"]].head(10))

    return future_df

if __name__ == "__main__":
    predict_next_3_days()
