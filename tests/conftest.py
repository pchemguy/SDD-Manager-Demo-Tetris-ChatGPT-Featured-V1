"""Pytest boundaries for compiled modules and later real browser fixtures."""
from pathlib import Path
import json, subprocess
import pytest
import functools, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from tests.support.runtime import launch_browser
ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def ask():
    """Run a production-module request without calculating its expected answer."""
    def execute(request):
        result = subprocess.run(['node', 'tests/support/engine_driver.mjs'], cwd=ROOT, input=json.dumps(request), text=True, capture_output=True, timeout=10, check=True)
        return json.loads(result.stdout)
    return execute

@pytest.fixture(scope='session')
def server_url():
    """Serve the actual dist tree over an owned ephemeral loopback socket."""
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(ROOT / 'dist'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=5)

@pytest.fixture(scope='session', params=['chromium','firefox'])
def browser(request):
    """Use the pinned managed browser and the diagnosed process-only remedy."""
    with sync_playwright() as runner:
        instance = launch_browser(runner, request.param)
        yield instance
        instance.close()

@pytest.fixture
def page(browser):
    """Give each browser scenario fresh state and bounded native actions."""
    context = browser.new_context(viewport={'width':1280,'height':720})
    instance = context.new_page()
    instance.set_default_timeout(10000)
    try:
        yield instance
    finally:
        context.close()
