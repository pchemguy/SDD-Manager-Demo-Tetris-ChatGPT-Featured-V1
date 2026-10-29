"""Literal clear scores, old-level awards and resulting gravity intervals."""
import pytest
from tests.support.scenarios import running
from tests.core.test_session import session

def vertical_clear(rows, next_kind='O', **stats):
    board = [[None]*10 for _ in range(20)]
    for y in range(20-rows,20): board[y]=['J']*4+[None]+['J']*5
    state = running(kind='I',x=2,y=16,board=board,next_kind=next_kind,**stats)
    state['active']['rotation']=1
    return state

@pytest.mark.parametrize('rows,points', [(0,0),(1,40),(2,100),(3,300),(4,1200)])
def test_clear_awards_and_line_totals(ask, rows, points):
    result=session(ask,vertical_clear(rows),[{'type':'softDrop'}])
    assert result['state']['score']==points
    assert result['state']['lines']==rows
    assert result['inputUnchanged']

def test_old_level_scores_and_new_level_sets_spawn_interval(ask):
    result=session(ask,vertical_clear(4,score=50,lines=19,level=2),[{'type':'softDrop'}])['state']
    assert result['score']==2450 and result['lines']==23 and result['level']==3
    assert result['remainingMs']==850

def test_crossing_ten_lines_and_minimum_interval(ask):
    result=session(ask,vertical_clear(1,lines=9),[{'type':'softDrop'}])['state']
    assert result['level']==2 and result['remainingMs']==925 and result['score']==40
    fast=session(ask,vertical_clear(1,lines=119,level=12),[{'type':'softDrop'},{'type':'advance','elapsedMs':100}])['state']
    assert fast['level']==13 and fast['remainingMs']==100 and fast['active']['y']==1

def test_no_drop_points_and_progression_retained_on_top_out(ask):
    assert session(ask,running(score=50),[{'type':'softDrop'}])['state']['score']==50
    state=vertical_clear(1,lines=9,next_kind='J')
    state['board'][0][3]='Z'
    result=session(ask,state,[{'type':'softDrop'}])
    assert result['state']['phase']=='game-over' and result['draws']==0
    assert result['state']['score']==40 and result['state']['lines']==10 and result['state']['level']==2

def test_nonadjacent_rows_preserve_survivor_order(ask):
    state=vertical_clear(0)
    for y in [17,19]:state['board'][y]=['J']*4+[None]+['J']*5
    state['board'][18][0]='Z'
    result=session(ask,state,[{'type':'softDrop'}])['state']
    assert result['score']==100 and result['lines']==2
    assert result['board'][18]==[None]*4+['I']+[None]*5
    assert result['board'][19]==['Z']+[None]*3+['I']+[None]*5
