"""Representative isolated browser interaction/rendering, not app acceptance."""
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from tests.support.runtime import launch_browser
import json
ROOT = Path(__file__).resolve().parents[2]

@pytest.mark.parametrize('engine', ['chromium', 'firefox'])
def test_repeated_interaction_rendering_and_teardown(engine):
    """Exercise two fresh contexts, native input and visible font/shape output."""
    with sync_playwright() as runner:
        browser = launch_browser(runner, engine)
        print(engine, browser.version)
        (ROOT / '.work' / f'{engine}-version.json').write_text(json.dumps({'version': browser.version, 'mode': 'managed headless shell' if engine == 'chromium' else 'managed headless Firefox'}))
        try:
            for index in range(2):
                context = browser.new_context(viewport={'width': 640, 'height': 480})
                page = context.new_page()
                page.set_default_timeout(10000)
                page.set_content('<body style="background:#102c38;color:#fff;font:32px monospace"><div style="background:#18bd91;padding:30px">READY</div><input aria-label="Probe"></body>')
                page.get_by_label('Probe').fill('abc')
                assert page.get_by_label('Probe').input_value() == 'abc'
                folder = ROOT / '.work/screenshots'
                folder.mkdir(parents=True, exist_ok=True)
                data = page.screenshot(path=str(folder / f'environment-{engine}-{index}.png'))
                assert len(data) > 1000
                context.close()
        finally:
            browser.close()
