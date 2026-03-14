import joblib
import pandas as pd

# Load trained RandomForest model
model = joblib.load("models/cause_model.pkl")


def detect_degradation_cause(ndvi, rainfall, urban_index):
    """
    Predict the cause of vegetation loss using trained model.
    Parameters:
    - ndvi: Normalized Difference Vegetation Index
    - rainfall: Total rainfall in mm
    - urban_index: Urbanization fraction
    Returns: predicted cause (str), confidence (float)
    """

    # Use DataFrame with the same column names as training
    features = pd.DataFrame([{
        "ndvi": ndvi,
        "rainfall": rainfall,
        "urban_index": urban_index
    }])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)
    confidence = float(probabilities.max())

    return prediction, confidence