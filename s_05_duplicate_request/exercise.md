# Duplicate request detection

**Scenario:** Identify whether a newly submitted request resembles an open request. This is a fictional practice exercise inspired by Williams Lea service areas, not a company assessment or real company model. The artifact was trained on synthetic examples.

**Supplied model:** TF IDF vectorizer plus nearest neighbours index in `model.joblib`. Do not retrain it. Complete only `inference.py` and, if necessary, deployment behavior in `server.py`.

**Input:** JSON object with `inputs`, a list of 1–32 records. Example: `{"inputs": [{"text": "Please update the Acme pitch deck for Thursday"}]}`

**Output:** JSON object with `predictions` (same order and count), each containing matched_request_id, similarity, potential_duplicate, plus `model_version`.

**Consider:** Nearest-neighbour similarity is not calibrated probability; retain corpus alignment and never auto-close requests. Validate payloads and return 400 for bad data. Model loads relative to the script, independent of working directory. `GET /health` and `POST /predict` are provided. Reject oversized bodies. Handle batches and deterministic feature ordering.

**Run:** `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python server.py --port 8000`, then POST the sample JSON to `/predict`. Never load a model file supplied by a request.

**Interview discussion:** Describe request schema, validation, artifact version, readiness versus liveness, metrics, logging without sensitive content, security, rollout, rollback and when to route uncertain outputs to human review. This server binds localhost for practice, not a production network service.
