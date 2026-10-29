"""Pytest boundaries for compiled modules and later real browser fixtures."""
from pathlib import Path
import json, subprocess
import pytest
import functools, threading, shutil
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

def pytest_addoption(parser):
    """Select actual consumer bytes and a deployment prefix without product hooks."""
    parser.addoption('--web-root', default=str(ROOT / 'dist'))
    parser.addoption('--web-prefix', default='')

@pytest.fixture(scope='session')
def web_root(request):
    root = Path(request.config.getoption('--web-root')).resolve(strict=True)
    if not root.is_dir() or not (root / 'index.html').is_file():
        raise ValueError('Selected web root must contain the built index.html')
    return root

@pytest.fixture(scope='session')
def server_url(request,web_root,tmp_path_factory):
    """Serve selected actual bytes at root or a validated nested deployment path."""
    prefix=request.config.getoption('--web-prefix').strip('/')
    if any(part in ('.','..') or not part.replace('-','').isalnum() for part in prefix.split('/') if prefix):
        raise ValueError('Unsafe test deployment prefix')
    root=web_root
    if prefix:
        root=tmp_path_factory.mktemp('web-host');shutil.copytree(web_root,root/prefix)
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/' + (prefix+'/' if prefix else '')
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
