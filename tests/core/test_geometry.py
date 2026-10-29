"""Independent occupied-cell and collision fixtures from SPEC S-02."""
import pytest

@pytest.mark.parametrize('kind', list('IJLOSTZ'))
def test_four_cells_and_full_rotation_cycle(ask, kind):
    first = ask({'kind': kind})
    assert len(first['cells']) == 4
    for direction in [-1, 1]:
        assert ask({'kind': kind, 'turns': 4, 'direction': direction}) == first

def test_literal_spawn_and_rotation_coordinates(ask):
    initial = ask({'kind': 'I'})
    assert initial['piece'] == {'kind': 'I', 'rotation': 0, 'x': 3, 'y': 0}
    assert {(p['x'], p['y']) for p in initial['cells']} == {(3, 1), (4, 1), (5, 1), (6, 1)}
    turned = ask({'kind': 'I', 'turns': 1})
    assert {(p['x'], p['y']) for p in turned['cells']} == {(5, 0), (5, 1), (5, 2), (5, 3)}
    assert ask({'kind': 'O', 'turns': 1})['piece']['rotation'] == 0

def test_padding_is_not_an_occupied_boundary(ask):
    board = [[None]*10 for _ in range(20)]
    piece = {'kind': 'I', 'rotation': 1, 'x': -2, 'y': 0}
    assert ask({'piece': piece, 'board': board})['fits']
    assert not ask({'piece': dict(piece, x=-3), 'board': board})['fits']
    board[2][0] = 'Z'
    assert not ask({'piece': piece, 'board': board})['fits']
    assert ask({'piece': {'kind':'I', 'rotation':0, 'x':3, 'y':18}, 'board':board})['fits']
    assert not ask({'piece': {'kind':'I', 'rotation':0, 'x':3, 'y':19}, 'board':board})['fits']

def test_unknown_piece_is_rejected(ask):
    assert 'piece' in ask({'kind':'?'})['error'].lower()

@pytest.mark.parametrize('kind,expected', [
    ('I', {(3,1),(4,1),(5,1),(6,1)}),
    ('J', {(3,0),(3,1),(4,1),(5,1)}),
    ('L', {(5,0),(3,1),(4,1),(5,1)}),
    ('O', {(4,0),(5,0),(4,1),(5,1)}),
    ('S', {(4,0),(5,0),(3,1),(4,1)}),
    ('T', {(4,0),(3,1),(4,1),(5,1)}),
    ('Z', {(3,0),(4,0),(4,1),(5,1)}),
])
def test_all_canonical_spawn_fixtures(ask, kind, expected):
    assert {(p['x'],p['y']) for p in ask({'kind':kind})['cells']} == expected

def test_counterclockwise_origin_and_input_preservation(ask):
    piece = {'kind':'T','rotation':0,'x':3,'y':0}
    result = ask({'piece':piece,'turns':1,'direction':-1})
    assert result['inputUnchanged']
    assert result['piece'] == dict(piece, rotation=3)
    assert {(p['x'],p['y']) for p in result['cells']} == {(3,1),(4,0),(4,1),(4,2)}
