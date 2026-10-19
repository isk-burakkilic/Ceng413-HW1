"""Small web service for CENG413 HW-1 (based on the Week 4 lab app).

Endpoints
  GET /health        -> {"status": "ok"}            (stateless)
  GET /greet?name=X  -> {"message": "Hello, X!"}    (stateless)
  GET /visit         -> {"visits": N}               (STATEFUL on purpose:
                        the counter is stored in a file so we can see what
                        happens to data when a container is removed)
  GET /info          -> {"name": ..., "version": ..., "hostname": ...}
                        (NEW for HW-1: app name and version come from
                        environment variables, hostname shows which
                        container answered)

Configuration comes from environment variables (12-factor style):
  APP_GREETING  default "Hello"
  DATA_DIR      default "/data"   (where the visit counter file lives)
  APP_NAME      default "ceng413-hw1"
  APP_VERSION   default "1.0.0"
"""
import os
import socket
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

GREETING = os.environ.get("APP_GREETING", "Hello")
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
APP_NAME = os.environ.get("APP_NAME", "ceng413-hw1")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")


def _counter_file() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / "visits.txt"


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/greet")
def greet():
    name = request.args.get("name", "world")
    return jsonify(message=f"{GREETING}, {name}!")


@app.get("/visit")
def visit():
    f = _counter_file()
    current = int(f.read_text()) if f.exists() else 0
    current += 1
    f.write_text(str(current))
    return jsonify(visits=current)


@app.get("/info")
def info():
    return jsonify(name=APP_NAME, version=APP_VERSION, hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
