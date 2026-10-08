"""Local JSON HTTP deployment harness. Never accept pickles from callers."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from inference import predict, ModelInputError

MAX_BYTES = 32_768

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        data = json.dumps(payload, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == '/health':
            self._send(200, {'status': 'ok'})
        else:
            self._send(404, {'error': 'not found'})

    def do_POST(self):
        if self.path != '/predict':
            return self._send(404, {'error': 'not found'})
        try:
            length = int(self.headers.get('Content-Length', '-1'))
            if not 0 <= length <= MAX_BYTES:
                return self._send(413, {'error': 'body exceeds limit or missing length'})
            request = json.loads(self.rfile.read(length))
            self._send(200, predict(request))
        except (ValueError, ModelInputError) as exc:
            self._send(400, {'error': str(exc)})
        except Exception:
            self.log_message('Unexpected inference error')
            self._send(500, {'error': 'internal inference error'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()

""" 
def do_POST(self):
    if self.path != '/predict':
        return self._send(404, {'error': 'not found'})

    # 1. Validate the declared request-body size.
    try:
        length = int(self.headers.get('Content-Length', '-1'))
    except ValueError:
        return self._send(
            400,
            {'error': 'Content-Length must be an integer'}
        )

    if not 0 <= length <= MAX_BYTES:
        return self._send(
            413,
            {'error': 'body exceeds limit or missing length'}
        )

    # 2. Read and parse the JSON.
    try:
        body = self.rfile.read(length)
        request = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return self._send(
            400,
            {'error': 'body must contain valid JSON'}
        )

    # 3. Validate model inputs and run inference.
    try:
        prediction = predict(request)

    except ModelInputError as exc:
        return self._send(400, {'error': str(exc)})

    except Exception:
        # Includes an unexpected ValueError from the model.
        self.log_message('Unexpected inference error')
        return self._send(
            500,
            {'error': 'internal inference error'}
        )

    # 4. Serialize and send the prediction.
    try:
        self._send(200, prediction)
    except (TypeError, ValueError):
        self.log_message('Prediction could not be serialized')
        return self._send(
            500,
            {'error': 'invalid inference output'}
        )






"""