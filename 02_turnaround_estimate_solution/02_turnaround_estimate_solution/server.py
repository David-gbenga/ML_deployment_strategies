"""Local practice server; use a production server for public hosting."""
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from inference import predict, ModelInputError, load_model

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, response):
        data = json.dumps(response, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/predict":
            self.send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "-1"))
            if not 1 <= length <= 32768:
                raise ValueError("Body must be 1 to 32768 bytes")
            payload = json.loads(self.rfile.read(length))
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
            return
        try:
            response = predict(payload)
            self.send_json(200, response)
        except ModelInputError as error:
            self.send_json(400, {"error": str(error)})
        except Exception:
            logging.exception("Prediction failed")
            self.send_json(500, {"error": "internal error"})

if __name__ == "__main__":
    load_model()  # Fail at startup if the supplied model cannot load.
    print("Listening at http://127.0.0.1:8000; Ctrl+C to stop")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
