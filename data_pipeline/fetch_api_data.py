import pandas as pd

def fetch_air_quality_data():
    data = {
        "city": ["Karachi"],
        "dt": [1700000000],
        "pm2_5": [55.2],
        "pm10": [110.5],
        "co": [0.8],
        "no2": [22.1],
        "so2": [5.3],
        "o3": [18.6],
        "temp": [29.5],
        "humidity": [65],
        "pressure": [1008]
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    print(fetch_air_quality_data())
