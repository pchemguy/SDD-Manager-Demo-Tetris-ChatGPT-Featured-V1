"""Visible stats/preview, native accessibility and specified viewport acceptance."""
from pathlib import Path
import pytest
from tests.browser.test_play import freeze_clock_and_draw_os

@pytest.mark.parametrize('width,height',[(640,480),(1280,720)])
def test_visible_complete_experience(page,server_url,width,height):
    page.set_viewport_size({'width':width,'height':height})
    freeze_clock_and_draw_os(page);page.goto(server_url)
    assert page.locator('.preview .filled').count()==0
    assert page.locator('[data-stat=score]').inner_text()=='000000'
    assert page.locator('[data-stat=level]').inner_text()=='1'
    page.get_by_role('button',name='Start',exact=True).focus();page.keyboard.press('Enter')
    assert page.locator('.preview .filled').count()==4
    assert page.locator('.preview').get_attribute('aria-label')=='Next piece: O'
    # Five adjacent O pieces clear two rows through real keyboard actions.
    for column in (0,2,4,6,8):
        for _ in range(abs(column-4)):page.keyboard.press('ArrowLeft' if column<4 else 'ArrowRight')
        for _ in range(19):page.keyboard.press('ArrowDown')
    assert page.locator('[data-stat=score]').inner_text()=='000100'
    assert page.locator('[data-stat=lines]').inner_text()=='02'
    page.keyboard.press('p')
    assert page.get_by_role('status').inner_text()=='Paused'
    assert page.locator('[data-stat=score]').inner_text()=='000100'
    assert page.locator('.overlay').is_visible()
    for selector in ('.board','.side','h1','button.toggle','button:has-text("Restart")'):
        box=page.locator(selector).bounding_box()
        assert box and box['x']>=0 and box['y']>=0 and box['x']+box['width']<=width and box['y']+box['height']<=height
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight')
    page.get_by_role('button',name='Resume',exact=True).focus();page.keyboard.press('Space')
    assert page.get_by_role('status').inner_text()=='Playing'
    assert page.locator('.board').evaluate('(n)=>document.activeElement===n')
    path=Path('.work/screenshots')/f'complete-{page.context.browser.browser_type.name}-{width}.png'
    path.parent.mkdir(parents=True,exist_ok=True);page.screenshot(path=str(path),full_page=True)
