"""Pause preserves snapshots/countdown and never resets the gravity interval."""
from tests.core.test_session import session
from tests.support.scenarios import running

def test_pause_freezes_commands_and_resume_uses_remainder(ask):
    actions=[{'type':'advance','elapsedMs':580},{'type':'pause'},{'type':'advance','elapsedMs':50000},{'type':'move','dx':-1},{'type':'rotate','direction':1},{'type':'softDrop'},{'type':'resume'},{'type':'advance','elapsedMs':419},{'type':'advance','elapsedMs':1}]
    result=session(ask,running(),actions)
    paused=result['snapshots'][2]
    assert paused['phase']=='paused' and paused['remainingMs']==420
    assert all(s==paused for s in result['snapshots'][3:7])
    assert result['snapshots'][7]['remainingMs']==420 and result['snapshots'][7]['phase']=='running'
    assert result['snapshots'][8]['active']['y']==0 and result['snapshots'][8]['remainingMs']==1
    assert result['state']['active']['y']==1 and result['state']['remainingMs']==1000
    assert result['inputUnchanged'] and result['draws']==0

def test_inapplicable_phase_commands_and_paused_restart(ask):
    ready=session(ask,actions=[{'type':'pause'},{'type':'resume'}])
    assert ready['state']['phase']=='ready' and ready['draws']==0
    assert session(ask,running(remaining=321),[{'type':'resume'}])['state']==running(remaining=321)
    state=running(phase='paused',score=100,lines=2)
    reset=session(ask,state,[{'type':'restart'}])
    assert reset['state']['phase']=='running' and reset['state']['score']==0 and reset['state']['lines']==0
    assert reset['draws']==2
