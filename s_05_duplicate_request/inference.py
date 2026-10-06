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
    texts = [_text(item) for item in _object(payload)]
    model = load_model()
    vectors = model['vectorizer'].transform(texts)
    distances, positions = model['neighbours'].kneighbors(vectors, n_neighbors=1)
    result = []
    for distance, position in zip(distances[:, 0], positions[:, 0]):
        similarity = max(0.0, min(1.0, 1.0-float(distance)))
        result.append({'matched_request_id': model['request_ids'][int(position)], 'similarity': round(similarity, 4), 'potential_duplicate': similarity >= 0.55})
    return {'predictions': result, 'model_version': 'synthetic-v1'}
