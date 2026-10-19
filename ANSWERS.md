# HW-1 Answers

## 1. Order of the instructions in my Dockerfile

My Dockerfile starts with the things that change least and ends with the things that change most. First comes the pinned base image (`python:3.12-slim`), then `WORKDIR`, then I copy only `requirements.txt` and run `pip install`, and only after that I copy `app.py`. Every instruction is a cached layer, and when one layer changes, Docker rebuilds that layer and every layer after it. Because my dependencies rarely change, the `pip install` layer stays `CACHED` when I edit the code, so a rebuild takes only a few seconds. If I swapped `COPY requirements.txt .` with `COPY . .` (copying all code before installing), every small code edit would break the cache and `pip install` would run again on every build, like `Dockerfile.v1` in the lab. The test stage follows the same idea: pytest is installed before the code and test files are copied, and the final stage copies the app from the test stage, so the image is only built if the tests pass.

## 2. Data inside a container

Data written inside a container lives in its thin writable layer, and that layer is deleted together with the container. I saw this with the `/visit` endpoint: without a volume the counter went back to 1 after I removed and restarted the container. To keep the data I run the container with a named volume, `-v hw1data:/data`, and the app writes its counter to `DATA_DIR=/data`. With the volume, after `docker rm -f hw1` and a new `docker run`, the counter continued from 2 to 3. An application should keep important state outside the container, in a volume, a database or object storage, so that any container can be stopped and replaced at any time.

## 3. The `latest` tag

`latest` is only a moving label, not a fixed version: it points to whatever image was pushed most recently. If I build with `python:latest` today and again next month, I may get a different Python version and different system libraries, so the same Dockerfile can give a different image or even fail. This breaks reproducibility, because I can no longer say exactly what is inside my image. Instead I pinned the base image to `python:3.12-slim`, and I pinned every Python package with an exact version in `requirements.txt` (`flask==3.1.3`, `gunicorn==23.0.0`) and `requirements-dev.txt` (`pytest==8.3.4`). I also tag my own image with a version, `ceng413-hw1:1.0`, instead of `latest`.

## Use of an AI assistant

Yes, I used an AI assistant. It helped me fix my Docker Desktop installation (enabling WSL 2), review my Dockerfile and `.dockerignore`, and prepare a first draft of these answers, which I checked against the lab results and can explain line by line.
