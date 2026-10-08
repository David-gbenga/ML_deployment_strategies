# Document routing

**Scenario:** Classify incoming service text into legal, finance, marketing, or general operations. This is a fictional practice exercise inspired by Williams Lea service areas, not a company assessment or real company model. The artifact was trained on synthetic examples.

**Supplied model:** TF IDF plus logistic regression in `model.joblib`. Do not retrain it. Complete only `inference.py` and, if necessary, deployment behavior in `server.py`.

**Input:** JSON object with `inputs`, a list of 1–32 records. Example: `{"inputs": [{"text": "Please review the contract clause and redline."}]}`

**Output:** JSON object with `predictions` (same order and count), each containing label, confidence, review_required, plus `model_version`.

**Consider:** Text cleaning is bundled with the model; preserve label mapping and abstain below confidence threshold. Validate payloads and return 400 for bad data. Model loads relative to the script, independent of working directory. `GET /health` and `POST /predict` are provided. Reject oversized bodies. Handle batches and deterministic feature ordering.

**Run:** `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `python server.py --port 8000`, then POST the sample JSON to `/predict`. Never load a model file supplied by a request.

**Interview discussion:** Describe request schema, validation, artifact version, readiness versus liveness, metrics, logging without sensitive content, security, rollout, rollback and when to route uncertain outputs to human review. This server binds localhost for practice, not a production network service.

For your supplied completed code, expect a result containing:
{ 'predictions': [ { 'label': 'legal', 'confidence': 0.5756, 'review_required': False } ], 'model_version': 'synthetic-v1'}

Running python inference.py alone will not display a prediction because that file defines functions but does not call them.
. Start server.py
python server.py --port 8000

Leave this terminal running. It may show no startup message—that is normal for your server.
Open a second PowerShell terminal and check health
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"

Expected response:
status

---

ok

This confirms that the server responds. The next step checks prediction through the server.
POST the sample JSON to /predict
Paste this into the second terminal:
$body = '{"inputs":[{"text":"Please review the contract clause and redline."}]}'

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -ContentType "application/json" -Body $body

Expected response:
{
"predictions": [
{
"label": "legal",
"confidence": 0.5756,
"review_required": false
}
],
"model_version": "synthetic-v1"
}

Here, PowerShell acts as the client: it sends your text to server.py, which calls inference.py and sends the prediction back.
To stop the server, press Ctrl+C in the first terminal. The model stays as a trusted local file; the request contains only input text.
