"""Complete the inference function. The supplied artifact is trusted and local."""
from pathlib import Path
import joblib

ARTIFACT = Path(__file__).resolve().parent / 'model.joblib'

class ModelInputError(ValueError):
    pass

_MODEL = None

def load_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = joblib.load(ARTIFACT)
    return _MODEL

def _object(payload):
    if not isinstance(payload, dict) or set(payload) != {'inputs'}:
        raise ModelInputError('Expected only an inputs object')
    inputs = payload['inputs']
    if not isinstance(inputs, list) or not 1 <= len(inputs) <= 32:
        raise ModelInputError('inputs must be a list of 1 to 32 records')
    return inputs


def _text(item):
    if not isinstance(item, dict) or set(item) != {'text'}:
        raise ModelInputError('Each record requires only text')
    value = item['text']
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 4000:
        raise ModelInputError('text must contain 1 to 4000 characters')
    return value.strip()

def predict(payload):
    items = _object(payload)
    texts = [_text(item) for item in items]
    model = load_model()
    probs = model.predict_proba(texts)
    result = []
    for row in probs:
        index = int(row.argmax())
        confidence = float(row[index])
        result.append({'label': str(model.classes_[index]), 'confidence': round(confidence, 4), 'review_required': confidence < 0.55})
    return {'predictions': result, 'model_version': 'synthetic-v1'}
