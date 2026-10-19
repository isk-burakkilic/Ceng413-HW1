# HW-1 Dockerfile, built from the Week 4 lab Dockerfile (v2).
# 1. Pinned, small base image          -> reproducible, smaller, fewer CVEs
# 2. Dependencies before code          -> build cache works
# 3. Tests run during the build        -> a broken app never becomes an image
# 4. Multi-stage: pytest stays behind  -> final image has only what it needs
# 5. Non-root user + HEALTHCHECK       -> limits damage, Docker sees health

# ---- Stage 1: base (runtime dependencies only) ----
FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: test (adds pytest, runs the unit tests) ----
FROM base AS test

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY app.py test_app.py ./
RUN python -m pytest -q -p no:cacheprovider

# ---- Stage 3: final (what we actually run) ----
FROM base AS final

# Copy the app from the test stage: the final image depends on the tests,
# so the tests always run, and we ship exactly the code that was tested.
COPY --from=test /app/app.py .

# Create an unprivileged user and a data folder it may write to.
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /data \
    && chown appuser:appuser /data
USER appuser

ENV DATA_DIR=/data
EXPOSE 8000

# python:3.12-slim has no curl, so Python itself calls /health.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
