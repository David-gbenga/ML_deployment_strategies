# Production turnaround estimate

**Scenario:** Predict hours to complete a presentation or document production request. This is a fictional practice exercise inspired by Williams Lea service areas, not a company assessment or real company model. The artifact was trained on synthetic examples.

**Supplied model:** Random forest regressor in `model.joblib`. Do not retrain it. Complete only `inference.py` and, if necessary, deployment behavior in `server.py`.

**Input:** JSON object with `inputs`, a list of 1–32 records. Example: `{"inputs": [{"page_count": 45, "asset_count": 18, "complexity": 3, "queue_depth": 8, "urgent": 1}]}`

**Output:** JSON object with `predictions` (same order and count), each containing predicted_hours, estimated_completion_utc, plus `model_version`.

**Consider:** Validate nonnegative quantities; return UTC timestamp and do not imply a contractual SLA guarantee. Validate payloads and return 400 for bad data. Model loads relative to the script, independent of working directory. `GET /health` and `POST /predict` are provided. Reject oversized bodies. Handle batches and deterministic feature ordering.

**Run:** `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python server.py --port 8000`, then POST the sample JSON to `/predict`. Never load a model file supplied by a request.

**Interview discussion:** Describe request schema, validation, artifact version, readiness versus liveness, metrics, logging without sensitive content, security, rollout, rollback and when to route uncertain outputs to human review. This server binds localhost for practice, not a production network service.
