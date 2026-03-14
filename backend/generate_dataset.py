import pandas as pd
import numpy as np

rows = 1500

data = []

for i in range(rows):

    ndvi = np.random.uniform(0.2, 0.8)
    rainfall = np.random.uniform(600, 1500)
    # Temperature parameter for environmental data simulation
    temperature = np.random.uniform(24, 35)
    urban_index = np.random.uniform(0.1, 0.6)

    if ndvi > 0.55:
        cause = "healthy"

    elif ndvi < 0.35 and rainfall < 800:
        cause = "drought"

    elif urban_index > 0.45:
        cause = "urban_expansion"

    elif ndvi < 0.40:
        cause = "deforestation"

    else:
        cause = "soil_degradation"

    data.append([ndvi, rainfall, temperature, urban_index, cause])

df = pd.DataFrame(
    data,
    columns=["ndvi", "rainfall", "temperature", "urban_index", "cause"]
)

df.to_csv("data/environmental_dataset.csv", index=False)

print("Dataset generated successfully")