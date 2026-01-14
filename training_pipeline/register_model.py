import sys
import os
import joblib
import hopsworks
import pandas as pd
from sklearn.linear_model import LinearRegression

PROJECT_NAME = "aqi_karachi_project"
MODEL_DIR = "models"
MODEL_NAME = "aqi_lr_model"

def register_model():
    print("🚀 Model registration started")

    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()
    mr = project.get_model_registry()

    df = fs.get_feature_group("aqi_features", version=4).read()

    X = df.drop(columns=["aqi", "dt", "city", "timestamp"], errors="ignore")
    y = df["aqi"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = f"{MODEL_DIR}/{MODEL_NAME}.pkl"
    joblib.dump(model, model_path)

    model_reg = mr.python.create_model(
        name=MODEL_NAME,
        description="Linear Regression AQI Predictor"
    )

    model_reg.save(model_path)

    print("✅ Model registered successfully in Hopsworks")

if __name__ == "__main__":
    register_model()
