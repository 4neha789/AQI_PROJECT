import hopsworks
import os
import shap
import joblib
import pandas as pd

PROJECT_NAME = "aqi_karachi_project"

print("🔍 SHAP analysis started")

# login
project = hopsworks.login(
    project=PROJECT_NAME,
    api_key_value=os.getenv("HOPSWORKS_API_KEY")
)

fs = project.get_feature_store()

# read features
df = fs.get_feature_group("aqi_features", version=4).read()

# drop non-feature columns
X = df.drop(
    columns=["aqi", "dt", "city", "timestamp"],
    errors="ignore"
)

# load trained model
model = joblib.load("models/aqi_lr_model.pkl")

# SHAP
explainer = shap.Explainer(model, X)
shap_values = explainer(X)

# print importance
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": abs(shap_values.values).mean(axis=0)
}).sort_values("importance", ascending=False)

print("\n📌 Feature Importance (SHAP):")
print(importance_df)

# visualization
shap.summary_plot(shap_values, X)

print("✅ SHAP analysis completed")
