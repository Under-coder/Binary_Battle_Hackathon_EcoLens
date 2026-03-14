from fastapi import APIRouter
from app.services.ai_analysis import detect_degradation_cause
from app.services.recommendation_engine import get_restoration_plan, estimate_recovery_time
from app.services.geocoding_service import get_coordinates
from app.services.earth_engine_service import get_environmental_data

router = APIRouter()


@router.get("/ecosystem-analysis")
def ecosystem_analysis(city: str):
    # 1️⃣ Convert city to coordinates
    coordinates = get_coordinates(city)
    if "error" in coordinates:
        return coordinates

    lat = coordinates["latitude"]
    lon = coordinates["longitude"]

    # 2️⃣ Fetch real environmental data
    env_data = get_environmental_data(lat, lon)
    if "error" in env_data:
        return env_data

    # 3️⃣ NDVI vegetation status
    latest_ndvi = env_data["average_ndvi"]
    if latest_ndvi > 0.6:
        veg_status = "Healthy Vegetation"
    elif latest_ndvi > 0.3:
        veg_status = "Moderate Vegetation"
    else:
        veg_status = "Degraded Vegetation"

    # 4️⃣ AI cause prediction    # Passing parameters to the model (excluding temperature)
    try:
        cause, confidence = detect_degradation_cause(
            ndvi=latest_ndvi,
            rainfall=env_data["rainfall"],
            urban_index=env_data["urban_index"]
        )
    except Exception as e:
        cause = "unknown"
        confidence = 0.0

    # 5️⃣ Recommendations
    recommendations = get_restoration_plan(cause)

    # 6️⃣ Recovery estimate
    recovery = estimate_recovery_time(veg_status)

    return {
        "city": city,
        "coordinates": coordinates,
        "ndvi_analysis": {
            "average_ndvi": round(latest_ndvi, 3),
            "ndvi_change": round(env_data["ndvi_change"], 3),
            "vegetation_status": veg_status
        },
        "environmental_indicators": {
            "rainfall": round(env_data["rainfall"], 2),
            "temperature": round(env_data["temperature"], 2) if env_data["temperature"] is not None else "N/A",
            "urban_index": round(env_data["urban_index"], 2)
        },
        "predicted_cause": cause,
        "confidence": round(confidence, 2),
        "restoration_recommendations": recommendations,
        "recovery_estimate": recovery
    }