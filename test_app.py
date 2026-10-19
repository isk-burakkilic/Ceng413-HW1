import importlib

import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APP_GREETING", "Hello")
    monkeypatch.setenv("APP_NAME", "test-app")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    import app as app_module

    importlib.reload(app_module)
    return app_module.app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_greet_default(client):
    assert client.get("/greet").get_json() == {"message": "Hello, world!"}


def test_greet_name(client):
    assert client.get("/greet?name=Ada").get_json() == {"message": "Hello, Ada!"}


def test_visit_counts_up(client):
    assert client.get("/visit").get_json() == {"visits": 1}
    assert client.get("/visit").get_json() == {"visits": 2}


def test_info_reads_env(client):
    body = client.get("/info").get_json()
    assert body["name"] == "test-app"
    assert body["version"] == "9.9.9"
    assert body["hostname"]
