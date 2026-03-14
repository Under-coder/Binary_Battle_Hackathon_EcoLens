import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
data = pd.read_csv("data/environmental_dataset.csv")

# Features (excluding temperature)
X = data[["ndvi", "rainfall", "urban_index"]]

# Target
y = data["cause"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train model
model.fit(X_train, y_train)

# Accuracy check
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, "models/cause_model.pkl")

print("Model saved to models/cause_model.pkl")