# 🌍 Karachi AQI Prediction System

## README.md
 Project Overview

This project is an **end-to-end Air Quality Index (AQI) prediction system for Karachi**, built according to the guidelines provided in the assignment PDF. The system fetches real-time and historical air quality & weather data using external APIs, performs feature engineering, stores data in a **Feature Store (Hopsworks)**, trains ML models, and serves **3‑day AQI forecasts** via a **Streamlit dashboard**.

The solution follows **MLOps best practices** with clear separation of:

* Data / Feature Pipeline
* Training Pipeline
* Prediction Pipeline
* Web Application

---

### 🧱 Project Structure

```
AQI_PROJECT/
│
├── app/
│   ├── dashboard.py               # Streamlit dashboard     
│   └── backend.py
│
│── configs/
│   ├── api_config.yaml                 
│   └── hopsworks_config.yaml
│
├── data_pipeline/
│   └── fetch_api_data.py          # Fetch AQI & weather data from API
│
│── exploration/
│   └── eda_analysis.py             # Eda+ Shap Analysis
│    └── shap_analysis.py     
│
├── feature_pipeline/
│   └── feature_engineering.py       # Feature engineering + feature store
│   └── feature_store.py
│
├── training_pipeline/
│   ├── train_linear.py               # Model training
│   └── evaluate.py                   # Model evaluation
│   ├── train_rf.py                   # Model training
│   └── tarin_xgboost.py              # Model training
│   └── register_model.py             # model registory
│
├── prediction_pipeline/
│   ├── __init__.py
│   └── predict_aqi.py              # 3‑day AQI forecast logic
│
├── test_hopsworks_login.py         # Connection test
├── requirements.txt
└── README.md
```

---

### ⚙️ Tech Stack

* **Python 3.10+**
* **Hopsworks Feature Store & Model Registry**
* **Scikit‑learn (Linear Regression / Tree models)**
* **Pandas, NumPy**
* **Streamlit** (Dashboard)
* **External APIs** (OpenWeather)

---

### 🔑 Setup Instructions

1. **Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Hopsworks API key (PowerShell)**

```powershell
$env:HOPSWORKS_API_KEY="<your_api_key>"
```

4. **Test connection**

```bash
python test_hopsworks_login.py
```

5. **Run feature pipeline (backfill)**

```bash
python feature_pipeline/feature_engineering.py
```

6. **Train model**

```bash
python training_pipeline/evaluate.py
```

7. **Run dashboard** (from project root)

```bash
streamlit run app/dashboard.py
```

---

### 📊 Dashboard Features

* Latest AQI value from Feature Store
* AQI health status (Good / Moderate / Unhealthy)
* **3‑day AQI forecast** using trained ML model
* Interactive charts
* Raw feature data viewer

---

# ScreenShots
<img width="1366" height="589" alt="5" src="https://github.com/user-attachments/assets/15ce8231-d679-47fa-b33a-64556f1f3593" />
<img width="1366" height="610" alt="4" src="https://github.com/user-attachments/assets/da0e823f-f585-4a51-a260-6149b76a3acc" />
<img width="1366" height="545" alt="3" src="https://github.com/user-attachments/assets/48aed97f-08b5-4d87-ba95-0003394fdc55" />
<img width="1366" height="542" alt="2" src="https://github.com/user-attachments/assets/ef34cfaf-ed7b-4045-a569-e6755f7ec386" />
<img width="1364" height="618" alt="1" src="https://github.com/user-attachments/assets/82c08295-ab1b-44e3-addc-f48d8db01164" />




