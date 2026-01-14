import hopsworks
import os

PROJECT_NAME = "aqi_karachi_project"

def get_or_create_feature_group():
    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()

    fg = fs.get_or_create_feature_group(
        name="aqi_features",
        version=2,   # 🔥 IMPORTANT CHANGE
        primary_key=["city", "dt"],
        description="AQI Features for Karachi",
        online_enabled=False
    )

    return fg
