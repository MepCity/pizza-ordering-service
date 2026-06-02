from fastapi.testclient import TestClient


# GET /health → 200 ve {"status": "ok"} dönmeli
# CI pipeline'daki smoke test ve K8s liveness probe bu endpoint'i kullanır
def test_healthcheck_returns_ok(test_client: TestClient) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
