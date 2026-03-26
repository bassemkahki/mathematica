from fastapi.testclient import TestClient
from engine.server import app

client = TestClient(app)

def test_primes_endpoint():
    response = client.get("/api/v1/sequences/primes?n=5")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["points"] is not None
    assert len(body["data"]["points"]) == 5
    p = body["data"]["points"][0]
    assert "x" in p
    assert "y" in p
    assert "z" in p

def test_fractal_endpoint():
    response = client.get("/api/v1/sequences/fractal?iterations=2")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["points"] is not None
    assert len(body["data"]["points"]) > 0
    p = body["data"]["points"][0]
    assert "x" in p
    assert "y" in p
    assert "z" in p
