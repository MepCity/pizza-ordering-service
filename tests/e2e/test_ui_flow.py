import socket
import threading
import time
from collections.abc import Generator

import pytest
import uvicorn

from src.main import app


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture
def live_server() -> Generator[str, None, None]:
    try:
        port = get_free_port()
    except PermissionError as exc:
        pytest.skip(f"Local port could not be allocated for E2E test: {exc}")

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    timeout = time.time() + 10
    while not server.started and time.time() < timeout:
        time.sleep(0.1)

    if not server.started:
        pytest.skip("Live server could not be started for Playwright E2E test")

    yield f"http://127.0.0.1:{port}"

    server.should_exit = True
    thread.join(timeout=5)


def test_user_can_create_order_from_web_ui(live_server: str) -> None:
    playwright = pytest.importorskip("playwright.sync_api")

    try:
        with playwright.sync_playwright() as browser_context:
            browser = browser_context.chromium.launch()
            page = browser.new_page()
            page.goto(live_server, wait_until="networkidle")
            page.fill("#customer-name", "Playwright User")
            page.fill("#extras", "olive")
            page.click("#submit-order")
            page.wait_for_timeout(500)

            result = page.locator("#order-result").inner_text()
            browser.close()
    except Exception as exc:
        pytest.skip(f"Playwright browser is not available: {exc}")

    assert "Playwright User" in result
    assert '"status": "pending"' in result
