"""Real keyboard/button acceptance against the built HTTP application."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def freeze_clock_and_draw_os(page):
    """Control platform boundaries in the test only; ship no fixture global."""
    page.add_init_script('Math.random = () => 0.5; performance.now = () => 0; window.requestAnimationFrame = () => 1; window.cancelAnimationFrame = () => {};')

def active_positions(page):
    return page.locator('.board .active').evaluate_all('(cells) => cells.map(c => Number(c.dataset.index))')

def test_live_movement_failed_down_lock_clear_and_restart(page, browser, server_url):
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    freeze_clock_and_draw_os(page)
    page.goto(server_url)
    page.get_by_role('button',name='Start',exact=True).click()
    assert active_positions(page)==[4,5,14,15]
    page.keyboard.press('ArrowLeft')
    assert active_positions(page)==[3,4,13,14]
    page.keyboard.press('ArrowUp')
    assert active_positions(page)==[3,4,13,14]
    for _ in range(18):page.keyboard.press('ArrowDown')
    assert page.locator('.board .settled').count()==0
    page.keyboard.press('ArrowDown')
    assert page.locator('.board .settled').count()==4
    folder=ROOT/'.work/screenshots';folder.mkdir(parents=True,exist_ok=True)
    page.screenshot(path=str(folder/f'game-basic-{browser.browser_type.name}.png'))
    page.keyboard.press('r')
    assert page.locator('.board .settled').count()==0
    for target in [0,2,4,6,8]:
        for _ in range(abs(target-4)):
            page.keyboard.press('ArrowLeft' if target<4 else 'ArrowRight')
        for _ in range(19):page.keyboard.press('ArrowDown')
    assert page.locator('.board .settled').count()==0
    assert page.get_by_role('status').inner_text()=='Playing'
    page.get_by_role('button',name='Restart',exact=True).click()
    assert active_positions(page)==[4,5,14,15]
    assert not errors

def test_native_gravity_moves_the_live_piece(page, server_url):
    page.add_init_script('Math.random = () => 0.5;')
    page.goto(server_url)
    page.get_by_role('button',name='Start',exact=True).click()
    page.wait_for_function("Number(document.querySelector('.board .active').dataset.index) >= 14")
    assert len(active_positions(page))==4

def test_composed_host_owns_one_loop_and_disposes(page, server_url):
    page.goto(server_url)
    result=page.evaluate('''async () => {
      const {mountGame}=await import('/platform/browser/host.js');
      const root=document.createElement('div');document.body.append(root);
      const frames=[], cancelled=[];
      const host=mountGame(root,{random:()=>0.5,now:()=>0,
        requestFrame:cb=>{frames.push(cb);return frames.length},cancelFrame:id=>cancelled.push(id)});
      root.querySelector('button').click();
      root.querySelector('.board').dispatchEvent(new KeyboardEvent('keydown',{code:'ArrowLeft',bubbles:true}));
      const scheduled=frames.length;
      host.dispose();host.dispose();frames[0](1000);
      return {scheduled,cancelled,children:root.children.length};
    }''')
    assert result=={'scheduled':1,'cancelled':[1],'children':0}
