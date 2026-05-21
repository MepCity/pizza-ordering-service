from fastapi.testclient import TestClient


def test_home_page_returns_html(test_client: TestClient) -> None:
    response = test_client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Pizza Ordering Service" in response.text
    assert "Create Order" in response.text
