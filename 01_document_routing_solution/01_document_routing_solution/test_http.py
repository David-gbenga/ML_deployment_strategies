import json
from pathlib import Path
from urllib.request import Request, urlopen
body = Path(__file__).with_name("sample_request.json").read_bytes()
request = Request("http://127.0.0.1:8000/predict", data=body,
                  headers={"Content-Type": "application/json"}, method="POST")
with urlopen(request, timeout=10) as response:
    print(json.dumps(json.loads(response.read()), indent=2))
