"""Run a k6 script in the real k6 runtime against a disposable HTTP fixture."""

import json
import os
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

K6_IMAGE = "grafana/k6:1.3.0"

DEFAULT_ENV = {
    "SEED_PASSWORD": "fixture-password",
    "USERS_SHA": "a" * 40,
    "POSTS_SHA": "b" * 40,
    "GATEWAY_SHA": "c" * 40,
    "VUS": "2",
    "RAMP_SECONDS": "1",
    "DURATION_SECONDS": "1",
    "ENVIRONMENT": "contract-test",
    "SUMMARY_PATH": "/results/summary.json",
}


class JsonHandler(BaseHTTPRequestHandler):
    """Base for fixture handlers: silent, with a JSON `respond`."""

    def log_message(self, *_):
        pass

    def respond(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run_k6(script, handler, **overrides):
    """Serve `handler`, run `loadtests/<script>` against it and return (result, summary).

    `summary` is None when the script wrote none.
    """
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory() as directory:
            env = {
                "BASE_URL": f"http://host.docker.internal:{server.server_port}/api",
                **DEFAULT_ENV,
                **overrides,
            }
            command = [
                "docker",
                "run",
                "--rm",
                "--user",
                f"{os.getuid()}:{os.getgid()}",
                "-v",
                f"{Path(__file__).resolve().parent}:/work:ro",
                "-v",
                f"{directory}:/results",
            ]
            for name, value in env.items():
                command.extend(["-e", f"{name}={value}"])
            result = subprocess.run(
                [*command, K6_IMAGE, "run", f"/work/{script}"],
                capture_output=True,
                text=True,
                timeout=45,
                check=False,
            )
            path = Path(directory) / "summary.json"
            summary = json.loads(path.read_text()) if path.exists() else None
            return result, summary
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
