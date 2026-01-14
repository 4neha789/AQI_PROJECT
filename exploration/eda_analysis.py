import hopsworks
import os
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_NAME = "aqi_karachi_project"

project = hopsworks.login(
    project=PROJECT_NAME,
    api_key_value=os.getenv("HOPSWORKS_API_KEY")
)

fs = project.get_feature_store()
df = fs.get_feature_group("aqi_features", version=4).read()

print(df.describe())

# AQI over time
df["datetime"] = pd.to_datetime(df["dt"], unit="s")
plt.figure()
plt.plot(df["datetime"], df["aqi"])
plt.title("AQI Trend Over Time (Karachi)")
plt.xlabel("Time")
plt.ylabel("AQI")
plt.show()

# Correlation
print(df.corr()["aqi"].sort_values(ascending=False))
