from pathlib import Path
import joblib

class ModelInputError(ValueError):
    pass

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
_MODEL = None

def load_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = joblib.load(MODEL_PATH)  # Only the supplied trusted artifact.
    return _MODEL

import math

FEATURES = ("pages", "images", "priority")
LIMITS = {"pages": (1, 500), "images": (0, 100), "priority": (0, 1)}

def predict(payload):
    if not isinstance(payload, dict) or set(payload) != set(FEATURES):
        raise ModelInputError("Provide pages, images and priority only")
    features = []
    for name in FEATURES:  # Explicit training order, not JSON key order.
        value = payload[name]
        low, high = LIMITS[name]
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ModelInputError(f"{name} must be a finite number")
        if value != int(value) or not low <= value <= high:
            raise ModelInputError(f"{name} must be an integer from {low} to {high}")
        features.append(float(value))
    model = load_model()
    minutes = float(model.predict([features])[0])
    return {
        "estimated_minutes": round(minutes, 2),
        "model_version": "turnaround-practice-v1",
    }
