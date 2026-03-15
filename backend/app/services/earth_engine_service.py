import ee
import datetime
import os
import json


# creds_json = os.environ.get("EE_SERVICE_ACCOUNT")
# if creds_json:
#     service_account_info = json.loads(creds_json)
#     credentials = ee.ServiceAccountCredentials(
#         service_account_email=service_account_info['client_email'],
#         key_data=creds_json
#     )
#     ee.Initialize(credentials)
# else:
#     ee.Initialize()  # fallback for local testing

# Initialize Earth Engine for local use
# Authenticate once by running ee.Authenticate() if not done already
ee.Initialize(project="internship-task-470310")

# Simplified India boundary polygon
india_boundary = ee.Geometry.Polygon([
    [[68.7, 8.1], [97.5, 8.1], [97.5, 37.0], [68.7, 37.0], [68.7, 8.1]]
])

def get_environmental_data(lat, lon, start_date="2023-01-01", end_date=None):
    """
    Fetch NDVI, rainfall, and urban index for a location in India.
    Returns a dictionary ready for AI input.
    """

    point = ee.Geometry.Point([lon, lat])

    # 1️⃣ Ensure the point is inside India
    if not point.intersects(india_boundary).getInfo():
        return {"error": "Location outside India boundary - data restricted to India region"}

    if not end_date:
        end_date = datetime.date.today().isoformat()

    # 2️⃣ NDVI - Sentinel-2
    s2_collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(india_boundary)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .filterDate(start_date, end_date)
        .filterBounds(point)
        .map(lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI"))
    )

    ndvi_image = s2_collection.mean()
    ndvi_result = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=10
    ).getInfo()
    avg_ndvi = ndvi_result.get("NDVI")
    if avg_ndvi is None:
        return {"error": "No NDVI data available for this location"}

    # NDVI change compared to 5 years ago (long-term analysis)
    prev_start = (datetime.datetime.strptime(start_date, "%Y-%m-%d") - datetime.timedelta(days=365*5)).date().isoformat()
    prev_end = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.timedelta(days=365*5)).date().isoformat()

    prev_s2_collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(india_boundary)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .filterDate(prev_start, prev_end)
        .filterBounds(point)
        .map(lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI"))
    )

    prev_ndvi_image = prev_s2_collection.mean()
    prev_ndvi_result = prev_ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=10
    ).getInfo()
    prev_avg_ndvi = prev_ndvi_result.get("NDVI", avg_ndvi)
    ndvi_change = avg_ndvi - prev_avg_ndvi

    # 3️⃣ Rainfall - CHIRPS daily (public dataset, India-only)
    try:
        rainfall_collection = (
            ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
            .filterBounds(india_boundary)
            .filterDate(start_date, end_date)
            .filterBounds(point)
        )

        rainfall_result = rainfall_collection.sum().reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=5000
        ).getInfo()

        total_rainfall = rainfall_result.get("precipitation", 0)
    except ee.ee_exception.EEException:
        total_rainfall = 0

    # 4️⃣ Temperature - ERA5 (India-only)
    try:
        temp_collection = (
            ee.ImageCollection("ECMWF/ERA5/DAILY")
            .filterBounds(india_boundary)
            .filterDate(start_date, end_date)
            .filterBounds(point.buffer(10000))
            .select("mean_2m_air_temperature")
        )

        temp_image = temp_collection.mean()
        temp_result = temp_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=30000,
            maxPixels=1e9
        ).getInfo()

        avg_temp = (temp_result.get("mean_2m_air_temperature", 273.15) - 273.15)  # Convert Kelvin to Celsius
    except ee.ee_exception.EEException:
        avg_temp = None  # Use None for unavailable data

    # 5️⃣ Urban Index - GHSL (India-restricted)
    try:
        urban_collection = ee.ImageCollection("JRC/GHSL/P2023A/GHS_BUILT_S")
        # Replace urban section with buffered sampling
        urban_buffer = point.buffer(500)  # 1km² around point
        urban_image = urban_collection.filterDate("2018-01-01").first().select("built_surface")
        urban_result = urban_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=urban_buffer,  # Sample neighborhood, not single pixel
            scale=100,
            maxPixels=1e6
        ).getInfo()

        urban_fraction = urban_result.get("built_surface", 0) / 10000
        if urban_fraction == 0:
            urban_fraction = 0.1  # Reasonable fallback for Indian cities
    except ee.ee_exception.EEException:
        urban_fraction = 0.1  # Fallback if data unavailable

    return {
        "average_ndvi": avg_ndvi,
        "ndvi_change": ndvi_change,
        "rainfall": total_rainfall,
        "temperature": avg_temp,
        "urban_index": urban_fraction
    }