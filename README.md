# Williams Lea style deployment solutions

Five fictional exercises with pre-trained synthetic models. They are inspired by public service areas, not an actual assessment. Each numbered folder is an independent Python package.

Create an environment, install its requirements, run `python server.py --port 8000`, and send the `sample_input` from `scenario.json` to `POST /predict`. `GET /health` reports process liveness.

Each folder contains a complete inference.py and solution_notes.md explaining reasoning, coding standards and deployment considerations.

The joblib files must be loaded only from this trusted bundle. Python 3.11+ and scikit-learn 1.8.0 are recommended. The local HTTP harness is for practice, not production.

Scenario inspiration: https://www.williamslea.com/services/document-word-processing/ and https://www.williamslea.com/technology/workflow-management-and-data-analytics/ .
