import hopsworks
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

PROJECT_NAME = "aqi_karachi_project"

def train_model():
    print("🚀 Training started (Linear Regression)")

    project = hopsworks.login(
        project=PROJECT_NAME,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()

    df = fs.get_feature_group("aqi_features", version=1).read()

    # Features & target
    X = df.drop(columns=["aqi", "dt", "city"], errors="ignore")
    y = df["aqi"]

    # 🔥 TRAIN / TEST SPLIT (80 / 20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    print(f"✅ Linear Regression trained | MAE: {mae:.2f}")

if __name__ == "__main__":
    train_model()
