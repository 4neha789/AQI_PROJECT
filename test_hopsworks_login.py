import os
import hopsworks

project = hopsworks.login(
    project="aqi_karachi_project",
    api_key_value=os.getenv("HOPSWORKS_API_KEY")
)

print("✅ Connected to project:", project.name)
