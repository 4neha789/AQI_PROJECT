import sys
import os

# ✅ PROJECT ROOT PATH ADD (FIXES data_pipeline IMPORT)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import hopsworks
import pandas as pd
import time
from data_pipeline.fetch_api_data import fetch_air_quality_data

PROJECT_NAME = "aqi_karachi_project"

def engineer_features():
    print("🚀 Feature engineering started")

    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()

    raw_df = fetch_air_quality_data()

    if raw_df.empty:
        raise ValueError("❌ API returned no data")

    # 🔥 UNIQUE BASE TIMESTAMP
    base_dt = int(time.time())

    rows = []
    for i in range(30):
        temp = raw_df.copy()
        temp["dt"] = base_dt + (i * 3600)
        rows.append(temp)

    df = pd.concat(rows, ignore_index=True)

    # Feature engineering
    df["timestamp"] = pd.to_datetime(df["dt"], unit="s")
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month

    df["aqi"] = df["pm2_5"] * 2.0
    df["timestamp"] = df["timestamp"].astype(str)

    print(f"📊 Rows to insert: {len(df)}")

    fg = fs.get_or_create_feature_group(
        name="aqi_features",
        version=4,
        primary_key=["city", "dt"],
        description="AQI Features for Karachi (engineered)",
        online_enabled=False
    )

    fg.insert(
        df,
        write_options={
            "wait_for_job": True,
            "write_offline": True
        }
    )

    print("✅ Feature engineering completed successfully")

if __name__ == "__main__":
    engineer_features()
