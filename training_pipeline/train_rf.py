import os
import hopsworks
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

project = hopsworks.login(
    project="aqi_karachi_project",
    api_key_value=os.getenv("HOPSWORKS_API_KEY")
)

fs = project.get_feature_store()

df = fs.get_feature_group("aqi_features", version=1).read()

X = df.drop(columns=["aqi", "dt", "city"], errors="ignore")
y = df["aqi"]

# 🔥 TRAIN / TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

# Save model
project.get_model_registry().python.create_model(
    "rf_aqi"
).save(model)

print(f"✅ Random Forest trained | MAE: {mae:.2f}")
