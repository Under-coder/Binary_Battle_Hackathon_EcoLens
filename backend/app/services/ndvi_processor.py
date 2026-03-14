import pandas as pd

def analyze_ndvi(file_path):
    # file_path = "data/sample_ndvi_data.csv"
    data = pd.read_csv(file_path)

    avg_ndvi = data["ndvi"].mean()

    latest_ndvi = data.iloc[-1]["ndvi"]

    # vegetation classification
    if latest_ndvi > 0.6:
        status = "Healthy Vegetation"

    elif latest_ndvi > 0.3:
        status = "Moderate Vegetation"

    else:
        status = "Degraded Vegetation"

    return {
        "average_ndvi": round(avg_ndvi, 3),
        "latest_ndvi": latest_ndvi,
        "vegetation_status": status
    }