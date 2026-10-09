# Document Routing — Text Classification

Hypothetical Williams Lea practice exercise, not an actual company assessment. Synthetic model/data: practice deployment only, not evidence of production accuracy.

## Your task
Complete only `predict(payload)` in inference.py. A server and trained model are supplied; do not retrain. Aim for 30–45 minutes.

Model: fitted TF-IDF + logistic regression pipeline. Classes: contract, invoice, support.
Input: exactly one text string, 1–4000 characters after stripping whitespace.
Output: label, confidence (4 decimal places), review_required, model_version.
Choose the class with highest probability using model.classes_ for column mapping.
Flag confidence < 0.55 for human review; still return the best label. The threshold is a practice business rule, not validated policy. Probability is an estimate, not a correctness guarantee.

## Files and request flow
server.py parses JSON, calls inference.predict(), and serializes its response. inference.py validates data and loads the trusted local model.joblib. requirements.txt pins its dependencies. scenario.json and this guide describe the task; they are not automatically read during prediction. sample_request.json is read by the test clients.

## Setup in Windows PowerShell / VS Code
Extract this ZIP into its own folder and open that folder in VS Code. Use Python 3.11 or 3.12 (3.12 used for validation).
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_prediction.py
python server.py
```
If activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python`; no execution-policy change is needed. Select .venv\Scripts\python.exe as the VS Code interpreter. In a second terminal in the same folder run:
```powershell
.\.venv\Scripts\python.exe test_http.py
```
Open http://127.0.0.1:8000/health in a browser. Stop with Ctrl+C before running the other scenario (both use port 8000). Challenge tests intentionally fail until predict() is completed. Linux/macOS activation: `source .venv/bin/activate`.

## Acceptance criteria
Valid requests return JSON with the specified fields. Invalid records raise ModelInputError, translated by the server into HTTP 400. Model failures return HTTP 500 with internal traceback logged. Repeat calls reuse the loaded model. Test model loading and direct inference before HTTP debugging. The server loads the model at startup, so missing/corrupt artifacts fail immediately.

## Fundamental approach
Read the contract first; identify classifier versus regressor, required preprocessing and output policy. Inspect model metadata using the supplied trusted artifact. Pin dependencies; implement the smallest correct prediction function, then test direct calls and HTTP. Ask about ambiguity instead of assuming labels, units or feature ordering.

## Problem-solving capability
Trace failures by layer: malformed JSON belongs to transport; wrong field names to validation; absent artifact to packaging; incompatible model versions to environment. Compare expected and actual types/keys. Reproduce one request before changing code.

## Coding standards
Use descriptive names, fixed artifact paths based on __file__, explicit input checks and JSON-compatible Python scalars. Keep inference independent of HTTP. Avoid a blanket exception in predict() that hides model bugs. Never load an artifact supplied by a caller.

## Deployment and MLOps understanding
This single-request local server demonstrates the deployment contract, not production hosting. For Azure ML use its required init/run entry points or a container endpoint; for another platform adapt its contract. Package model, code and pinned environment as one versioned release. Before release check predictions, schema and model readiness; compare a candidate on controlled traffic and retain rollback artifacts. Monitor latency, errors, input drift and quality with delayed labels. Classification: track per-class precision/recall and review rate. Regression: track MAE in minutes and bias by workload/priority. Drift prompts investigation, not automatic retraining. For public deployment add a production HTTP server, authentication, TLS, request timeouts and resource limits.

## Model-specific interview explanation
The fitted vectorizer must be reused, never fitted on live text. Its learned vocabulary is part of the artifact. Select labels using classes_, not guessed column ordering. Low-confidence and out-of-vocabulary requests require review; high confidence alone does not establish correctness. Evaluate macro-F1, class recall and calibration on representative held-out data before adopting a threshold.

## References
https://scikit-learn.org/stable/model_persistence.html
https://docs.python.org/3/library/http.server.html
