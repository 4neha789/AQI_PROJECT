def check_aqi_alerts(df):
    alerts = []

    for _, row in df.iterrows():
        aqi = row["predicted_aqi"]

        if aqi > 150:
            alerts.append("🚨 Hazardous AQI detected!")
        elif aqi > 100:
            alerts.append("⚠️ Unhealthy AQI level")
        else:
            alerts.append("✅ AQI is safe")

    df["alert"] = alerts
    return df
