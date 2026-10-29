"""Complete consumer flows against whichever built/extracted web root is selected."""
from tests.browser.test_play import freeze_clock_and_draw_os,active_positions

def test_game_over_retains_queue_and_restart_recovers(page,server_url):
    freeze_clock_and_draw_os(page);page.goto(server_url)
    page.get_by_role('button',name='Start',exact=True).click()
    for count in range(19,0,-2):
        for _ in range(count):page.keyboard.press('ArrowDown')
    assert page.get_by_role('status').inner_text()=='Game over'
    assert page.locator('.board .active').count()==0
    assert page.locator('.board .settled').count()==40
    assert page.locator('.preview .piece-O').count()==4
    assert page.locator('.overlay').inner_text()=='Game over'
    for key in ['ArrowDown','ArrowLeft','ArrowUp','p']:page.keyboard.press(key)
    assert page.get_by_role('status').inner_text()=='Game over'
    page.get_by_role('button',name='Restart',exact=True).focus();page.keyboard.press('Enter')
    assert active_positions(page)==[4,5,14,15]
    assert page.locator('.board .settled').count()==0
    assert page.locator('[data-stat=score]').inner_text()=='000000'
    assert page.get_by_role('status').inner_text()=='Playing'

def test_preview_promotes_and_unfocused_board_ignores_shortcuts(page,server_url):
    page.add_init_script('''{const values=[0.5,0,0.8];let i=0;Math.random=()=>values[Math.min(i++,2)];performance.now=()=>0;requestAnimationFrame=()=>1;cancelAnimationFrame=()=>{};}''')
    page.goto(server_url);page.get_by_role('button',name='Start',exact=True).click()
    assert page.locator('.preview .piece-I').count()==4
    page.get_by_role('button',name='Restart',exact=True).focus();page.keyboard.press('ArrowLeft')
    assert active_positions(page)==[4,5,14,15]
    page.locator('.board').focus()
    for _ in range(19):page.keyboard.press('ArrowDown')
    assert active_positions(page)==[13,14,15,16]
    assert page.locator('.preview .piece-T').count()==4
    page.keyboard.down('p');page.keyboard.down('p');page.keyboard.up('p')
    assert page.get_by_role('status').inner_text()=='Paused'

def test_level_crossing_displays_complete_progression(page,server_url):
    freeze_clock_and_draw_os(page);page.goto(server_url)
    page.get_by_role('button',name='Start',exact=True).click()
    for _ in range(5):
        for target in (0,2,4,6,8):
            for _ in range(abs(target-4)):page.keyboard.press('ArrowLeft' if target<4 else 'ArrowRight')
            for _ in range(19):page.keyboard.press('ArrowDown')
    assert page.locator('[data-stat=lines]').inner_text()=='10'
    assert page.locator('[data-stat=level]').inner_text()=='2'
    assert page.locator('[data-stat=score]').inner_text()=='000500'
    assert page.locator('.board .settled').count()==0
