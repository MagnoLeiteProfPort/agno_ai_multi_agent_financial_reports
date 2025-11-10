from fastapi.testclient import TestClient
from apps.api.main import app

def test_health():
    c = TestClient(app)
    r = c.get("/v1/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True
