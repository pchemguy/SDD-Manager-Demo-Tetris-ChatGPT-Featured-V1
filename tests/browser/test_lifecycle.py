"""Native controls plus explicitly modeled lifecycle/clock/failure boundaries."""
from tests.browser.test_play import freeze_clock_and_draw_os,active_positions

def test_native_pause_keys_and_resume_focus(page,server_url):
    freeze_clock_and_draw_os(page);page.goto(server_url)
    page.get_by_role('button',name='Start',exact=True).click()
    page.keyboard.press('p')
    assert page.get_by_role('status').inner_text()=='Paused'
    saved=active_positions(page)
    page.keyboard.press('ArrowDown')
    assert active_positions(page)==saved
    page.get_by_role('button',name='Resume',exact=True).click()
    assert page.get_by_role('status').inner_text()=='Playing'
    assert page.locator('.board').evaluate('(n)=>document.activeElement===n')
    page.keyboard.press('Escape')
    assert page.get_by_role('status').inner_text()=='Paused'

def test_controlled_host_preserves_pause_remainder_and_due_order(page,server_url):
    page.goto(server_url)
    result=page.evaluate('''async()=>{
      const {mountGame}=await import('/platform/browser/host.js');
      const root=document.createElement('div');document.body.append(root);
      let time=0;const frames=[];
      const host=mountGame(root,{random:()=>0.5,now:()=>time,requestFrame:cb=>{frames.push(cb);return frames.length},cancelFrame:()=>{}});
      const positions=()=>[...root.querySelectorAll('.active')].map(n=>Number(n.dataset.index));
      const key=code=>root.querySelector('.board').dispatchEvent(new KeyboardEvent('keydown',{code,bubbles:true}));
      root.querySelector('button').click();time=600;key('ArrowLeft');
      root.querySelector('.toggle').click();const paused=root.querySelector('[role=status]').textContent;
      time=10000;root.querySelector('.toggle').click();
      time=10399;frames.at(-1)(time);const before=positions();
      time=10400;key('ArrowDown');const after=positions();
      host.dispose();return {paused,before,after};
    }''')
    assert result=={'paused':'Paused','before':[3,4,13,14],'after':[23,24,33,34]}

def test_modeled_visibility_blur_and_hidden_resume_guard(page,server_url):
    page.goto(server_url)
    result=page.evaluate('''async()=>{
      const {mountGame}=await import('/platform/browser/host.js');
      const root=document.createElement('div');document.body.append(root);let hidden=false;
      const descriptor=Object.getOwnPropertyDescriptor(document,'hidden');
      Object.defineProperty(document,'hidden',{configurable:true,get:()=>hidden});
      const host=mountGame(root,{random:()=>0.5,now:()=>0,requestFrame:()=>1,cancelFrame:()=>{}});
      const phase=()=>root.querySelector('[role=status]').textContent;
      root.querySelector('button').click();hidden=true;document.dispatchEvent(new Event('visibilitychange'));
      const onHide=phase();root.querySelector('.toggle').click();const hiddenResume=phase();
      hidden=false;document.dispatchEvent(new Event('visibilitychange'));const restored=phase();
      root.querySelector('.toggle').click();window.dispatchEvent(new Event('blur'));const onBlur=phase();
      window.dispatchEvent(new Event('focus'));const onFocus=phase();host.dispose();
      if(descriptor)Object.defineProperty(document,'hidden',descriptor);else delete document.hidden;
      return {onHide,hiddenResume,restored,onBlur,onFocus};
    }''')
    assert result==dict.fromkeys(['onHide','hiddenResume','restored','onBlur','onFocus'],'Paused')

def test_internal_and_render_failures_stop_without_uncaught_error(page,server_url):
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(server_url)
    result=page.evaluate('''async()=>{
      const {mountGame}=await import('/platform/browser/host.js');const results=[];
      for(const mode of ['random','render']){
        const root=document.createElement('div');document.body.append(root);let calls=0;const frames=[];
        const host=mountGame(root,{random:()=>{calls++;return mode==='random'?1:0.5},now:()=>0,requestFrame:cb=>{frames.push(cb);return 1},cancelFrame:()=>{}});
        const start=root.querySelector('button');
        if(mode==='render')Object.defineProperty(root.querySelector('.cell'),'className',{set(){throw new Error('render fault')}});
        start.click();const first=calls;start.dispatchEvent(new Event('click'));
        results.push({message:root.textContent,stopped:calls===first&&frames.length===0});host.dispose();
      }return results;
    }''')
    assert all('Game unavailable' in r['message'] and 'Reload' in r['message'] and r['stopped'] for r in result)
    assert not errors

def test_native_repeat_modifiers_and_unassigned_space(page,server_url):
    page.add_init_script('Math.random=()=>0.8;performance.now=()=>0;requestAnimationFrame=()=>1;cancelAnimationFrame=()=>{};')
    page.goto(server_url);page.get_by_role('button',name='Start',exact=True).click()
    page.keyboard.down('ArrowUp');page.keyboard.down('ArrowUp');page.keyboard.up('ArrowUp')
    assert active_positions(page)==[4,14,15,24]
    page.keyboard.down('ArrowLeft');page.keyboard.down('ArrowLeft');page.keyboard.up('ArrowLeft')
    assert active_positions(page)==[2,12,13,22]
    page.keyboard.press('Control+ArrowRight');page.keyboard.press('Space')
    assert active_positions(page)==[2,12,13,22]
