# Invoice anomaly flagging solution reasoning

## Fundamental approach
The model artifact is supplied; load once from a script-relative, trusted path. Establish an explicit JSON schema and preserve batch order. Keep the inference function independent of HTTP so it can be checked without a running service.

## Problem solving
Isolation Forest decision_function is relative; capture fitted threshold and never call the score a probability. Check invalid types, missing and extra fields, batch size, and model output shape before relying on results. The supplied threshold is an illustrative operational policy requiring validation on representative data.

## Coding standards
Use named functions, bounds, concise error messages and explicit conversion of NumPy values to JSON-safe Python types. The service returns 400 for input errors and hides internal errors behind a 500 response. Pin compatible dependency ranges and record model version.

## Technical understanding
The artifact and training examples are synthetic, so confidence, thresholds and accuracy are not production validated. `/health` checks process liveness; a production readiness probe should also ensure the model loads. Add structured telemetry for request count, latency, 4xx/5xx, drift, class mix and manual review rate. Authenticate the service, enforce TLS, redact sensitive document text, define versioned rollout and rollback, and avoid auto-actioning risky predictions.
