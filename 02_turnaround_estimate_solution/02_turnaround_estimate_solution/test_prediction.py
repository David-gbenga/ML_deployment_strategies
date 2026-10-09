import json
from pathlib import Path
from inference import predict
payload = json.loads(Path(__file__).with_name("sample_request.json").read_text())
print(json.dumps(predict(payload), indent=2))
