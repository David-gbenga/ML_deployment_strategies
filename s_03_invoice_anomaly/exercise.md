# Invoice anomaly flagging

**Scenario:** Score invoice line items for unusual values before human billing review. This is a fictional practice exercise inspired by Williams Lea service areas, not a company assessment or real company model. The artifact was trained on synthetic examples.

**Supplied model:** Isolation Forest in `model.joblib`. Do not retrain it. Complete only `inference.py` and, if necessary, deployment behavior in `server.py`.

**Input:** JSON object with `inputs`, a list of 1–32 records. Example: `{"inputs": [{"amount_gbp": 8500.0, "hours_billed": 14.0, "rate_gbp": 210.0, "revision_count": 7}]}`

**Output:** JSON object with `predictions` (same order and count), each containing anomaly_score, flagged, review_required, plus `model_version`.

**Consider:** Isolation Forest decision_function is relative; capture fitted threshold and never call the score a probability. Validate payloads and return 400 for bad data. Model loads relative to the script, independent of working directory. `GET /health` and `POST /predict` are provided. Reject oversized bodies. Handle batches and deterministic feature ordering.

**Run:** `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python server.py --port 8000`, then POST the sample JSON to `/predict`. Never load a model file supplied by a request.

**Interview discussion:** Describe request schema, validation, artifact version, readiness versus liveness, metrics, logging without sensitive content, security, rollout, rollback and when to route uncertain outputs to human review. This server binds localhost for practice, not a production network service.
