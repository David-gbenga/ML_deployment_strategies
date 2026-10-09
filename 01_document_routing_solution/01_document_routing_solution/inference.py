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

def predict(payload):
    if not isinstance(payload, dict) or set(payload) != {"text"}:
        raise ModelInputError("Provide only a text field")
    text = payload["text"]
    if not isinstance(text, str) or not 1 <= len(text.strip()) <= 4000:
        raise ModelInputError("text must contain 1 to 4000 characters")
    model = load_model()
    probabilities = model.predict_proba([text.strip()])[0]
    index = int(probabilities.argmax())
    confidence = float(probabilities[index])
    return {
        "label": str(model.classes_[index]),
        "confidence": round(confidence, 4),
        "review_required": confidence < 0.55,
        "model_version": "routing-practice-v1",
    }
