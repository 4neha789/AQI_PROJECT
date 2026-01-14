import hopsworks
import os

PROJECT_NAME = "aqi_karachi_project"

def create_feature_view():
    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()

    # ✅ IMPORTANT: USE FEATURE GROUP VERSION 3
    fg = fs.get_feature_group(
        name="aqi_features",
        version=3
    )

    fv = fs.get_or_create_feature_view(
        name="aqi_feature_view",
        version=2,  # 🔥 NEW VERSION
        query=fg.select_all(),
        labels=["aqi"]
    )

    print("✅ Feature View v2 created successfully")

if __name__ == "__main__":
    create_feature_view()
