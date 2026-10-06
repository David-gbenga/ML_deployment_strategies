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

import math
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

FIELDS = [('page_count', 0, 10000, 'int'), ('complexity', 1, 5, 'int'), ('queue_depth', 0, 10000, 'int'), ('hours_to_deadline', 0, 720, 'number'), ('priority', 1, 3, 'int')]

def _record(item):
    if not isinstance(item, dict) or set(item) != {field[0] for field in FIELDS}:
        raise ModelInputError("Record fields do not match schema")
    values = []
    for name, low, high, kind in FIELDS:
        value = item[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ModelInputError(f"{name} must be numeric")
        if kind == "int" and (not isinstance(value, int) or isinstance(value, bool)):
            raise ModelInputError(f"{name} must be an integer")
        if not math.isfinite(value) or not low <= value <= high:
            raise ModelInputError(f"{name} is outside allowed range")
        values.append(float(value))
    return values

def predict(payload):
    records = [_record(item) for item in _object(payload)]
    probabilities = load_model().predict_proba(records)[:, 1]
    result = []
    for probability in probabilities:
        p = float(probability)
        result.append({'breach_probability': round(p, 4), 'risk_level': 'high' if p >= 0.65 else 'medium' if p >= 0.35 else 'low', 'manual_review': p >= 0.65})
    return {'predictions': result, 'model_version': 'synthetic-v1'}
