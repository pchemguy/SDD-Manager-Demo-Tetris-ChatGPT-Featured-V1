"""Session, clock and lock/spawn behavior from SPEC S-01 through S-04."""
import pytest
from tests.support.scenarios import running

def session(ask, state=None, actions=(), values=None):
    request = dict(op='session', actions=list(actions))
    if state is not None: request['state'] = state
    if values is not None: request['values'] = values
    return ask(request)

def test_ready_and_start_draws(ask):
    ready = session(ask)['state']
    assert ready['board'] == [[None]*10 for _ in range(20)]
    assert ready['phase'] == 'ready' and ready['active'] is None and ready['next'] is None
    result = session(ask, actions=[{'type':'start'}], values=[0,.999999])
    assert result['state']['phase'] == 'running'
    assert result['state']['active']['kind'] == 'I' and result['state']['next'] == 'Z'
    assert result['draws'] == 2 and result['inputUnchanged']

@pytest.mark.parametrize('value,kind', [(0,'I'),(1/7,'J'),(.35,'L'),(.5,'O'),(.65,'S'),(.8,'T'),(.999999,'Z')])
def test_independent_uniform_mapping_and_repeats(ask, value, kind):
    result = session(ask, actions=[{'type':'start'}], values=[value])
    assert result['state']['active']['kind'] == result['state']['next'] == kind
    assert result['draws'] == 2

def test_contact_is_not_lock_and_exact_expiry_locks(ask):
    result = session(ask, running(y=17), [dict(type='advance', elapsedMs=n) for n in [999,1,999,1]])
    a,b,c,d = result['snapshots'][1:]
    assert a['active']['y'] == 17 and a['remainingMs'] == 1
    assert b['active']['y'] == 18 and not any(any(row) for row in b['board'])
    assert c['active']['kind'] == 'O' and c['remainingMs'] == 1
    assert d['active']['kind'] == 'I' and sum(cell is not None for row in d['board'] for cell in row) == 4
    assert result['draws'] == 1 and result['inputUnchanged']

def test_soft_drop_preserves_cadence_then_failed_attempt_locks(ask):
    result = session(ask, running(y=17, remaining=333), [{'type':'softDrop'},{'type':'softDrop'}])
    assert result['snapshots'][1]['active']['y'] == 18
    assert result['snapshots'][1]['remainingMs'] == 333
    assert result['state']['active']['kind'] == 'I' and result['state']['remainingMs'] == 1000

def test_lag_discards_overflow_without_multiple_steps(ask):
    result = session(ask, running(), [{'type':'advance','elapsedMs':100000},{'type':'advance','elapsedMs':0}])
    assert result['state']['active']['y'] == 1 and result['state']['remainingMs'] == 1000

def test_movement_rotation_and_soft_drop_do_not_postpone_gravity(ask):
    actions = [{'type':'move','dx':-1},{'type':'rotate','direction':1},{'type':'softDrop'},{'type':'advance','elapsedMs':499},{'type':'advance','elapsedMs':1}]
    result = session(ask, running(remaining=500), actions)
    assert result['snapshots'][3]['remainingMs'] == 500
    assert result['state']['active']['y'] == 2 and result['state']['remainingMs'] == 1000
    assert result['draws'] == 0 and result['inputUnchanged']

def test_rejected_wall_move_and_rotation_do_not_kick(ask):
    assert session(ask, running(x=0), [{'type':'move','dx':-1}])['state'] == running(x=0)
    state = running(kind='I', x=-2, remaining=777)
    state['active']['rotation'] = 1
    assert session(ask, state, [{'type':'rotate','direction':1}])['state'] == state

def test_legal_moves_and_rotation_are_applied(ask):
    result = session(ask, running(kind='T',x=3), [{'type':'move','dx':-1},{'type':'move','dx':1},{'type':'rotate','direction':1}])
    assert result['snapshots'][1]['active']['x'] == 2
    assert result['snapshots'][2]['active']['x'] == 3
    assert result['state']['active'] == {'kind':'T','rotation':1,'x':3,'y':0}

def test_simultaneous_clear_compacts_before_spawn(ask):
    board = [[None]*10 for _ in range(20)]
    board[0][3] = 'Z'
    for row in [18,19]:
        board[row] = ['J']*4+[None,None]+['J']*4
    result = session(ask, running(y=18, board=board, next_kind='J'), [{'type':'softDrop'}])
    assert result['state']['phase'] == 'running' and result['state']['active']['kind'] == 'J'
    assert result['state']['board'][:2] == [[None]*10]*2
    assert result['state']['board'][2][3] == 'Z'
    assert result['draws'] == 1 and result['inputUnchanged']

def test_top_out_consumes_no_replacement_draw_and_restart_clears(ask):
    board = [[None]*10 for _ in range(20)];board[0][3] = 'Z'
    result = session(ask, running(x=0,y=18,board=board,next_kind='J'), [{'type':'softDrop'}])
    assert result['state']['phase'] == 'game-over' and result['state']['active'] is None
    assert result['state']['next'] == 'J' and result['draws'] == 0
    fresh = session(ask, result['state'], [{'type':'restart'}], [0,0])
    assert fresh['state']['phase'] == 'running' and fresh['draws'] == 2
    assert fresh['state']['board'] == [[None]*10 for _ in range(20)]

@pytest.mark.parametrize('action', [{'type':'move','dx':0},{'type':'rotate','direction':0},{'type':'advance','elapsedMs':-1},{'type':'advance','elapsedMs':'NaN'},{'type':'advance','elapsedMs':'Infinity'},{'type':'unknown'}])
def test_invalid_internal_actions_preserve_state(ask, action):
    state = running()
    result = session(ask,state,[action])
    assert result.get('error') and result['state'] == state and result['inputUnchanged']

@pytest.mark.parametrize('values', [[-0.1],[1],[None],[]])
def test_invalid_random_source_preserves_ready(ask, values):
    result = session(ask,actions=[{'type':'start'}],values=values)
    assert result.get('error') and result['state']['phase'] == 'ready' and result['inputUnchanged']
