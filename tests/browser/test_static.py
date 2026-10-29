"""Actual root/nested static deployment and local-only asset policy."""
from pathlib import Path
import functools,threading,shutil
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import pytest
ROOT=Path(__file__).resolve().parents[2]

@pytest.fixture
def nested_url(tmp_path,web_root):
    root=tmp_path/'games/classic';shutil.copytree(web_root,root)
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(SimpleHTTPRequestHandler,directory=str(tmp_path)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:yield f'http://127.0.0.1:{server.server_port}/games/classic/'
    finally:server.shutdown();server.server_close();thread.join(5)

@pytest.mark.parametrize('deployment',['root','nested'])
def test_static_local_assets_and_csp(page,server_url,nested_url,deployment):
    url=server_url.rstrip('/')+'/' if deployment=='root' else nested_url
    requests=[];failures=[];errors=[]
    page.on('request',lambda r:requests.append(r.url));page.on('response',lambda r:failures.append(r.url) if r.status>=400 else None)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url);page.get_by_role('button',name='Start',exact=True).click()
    page.wait_for_timeout(100)
    assert page.locator('.board .active').count()==4
    policy=page.locator('meta[http-equiv="Content-Security-Policy"]').get_attribute('content')
    assert "default-src 'none'" in policy and "script-src 'self'" in policy and "connect-src 'none'" in policy
    assert all(u.startswith(url) for u in requests)
    assert not failures and not errors
    assert page.locator('script:not([src])').count()==0
