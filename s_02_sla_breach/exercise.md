# SLA breach risk

**Scenario:** Estimate probability that a document production job breaches its SLA. This is a fictional practice exercise inspired by Williams Lea service areas, not a company assessment or real company model. The artifact was trained on synthetic examples.

**Supplied model:** Random forest classifier in `model.joblib`. Do not retrain it. Complete only `inference.py` and, if necessary, deployment behavior in `server.py`.

**Input:** JSON object with `inputs`, a list of 1–32 records. Example: `{"inputs": [{"page_count": 120, "complexity": 3, "queue_depth": 18, "hours_to_deadline": 4.0, "priority": 2}]}`

**Output:** JSON object with `predictions` (same order and count), each containing breach_probability, risk_level, manual_review, plus `model_version`.

**Consider:** Validate ranges and exact feature order; use probability threshold as a routing policy, not model accuracy. Validate payloads and return 400 for bad data. Model loads relative to the script, independent of working directory. `GET /health` and `POST /predict` are provided. Reject oversized bodies. Handle batches and deterministic feature ordering.

**Run:** `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python server.py --port 8000`, then POST the sample JSON to `/predict`. Never load a model file supplied by a request.

**Interview discussion:** Describe request schema, validation, artifact version, readiness versus liveness, metrics, logging without sensitive content, security, rollout, rollback and when to route uncertain outputs to human review. This server binds localhost for practice, not a production network service.
