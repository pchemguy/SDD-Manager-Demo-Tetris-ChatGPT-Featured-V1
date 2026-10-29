"""Literal valid snapshots for testing transitions through the public engine."""
def running(kind='O', x=4, y=0, next_kind='I', remaining=1000, board=None, **stats):
    """Construct explicit board data; calculate no expected gameplay result."""
    data = dict(phase='running', board=board if board is not None else [[None]*10 for _ in range(20)], active=dict(kind=kind, rotation=0, x=x, y=y), next=next_kind, score=0, lines=0, level=1, remainingMs=remaining)
    data.update(stats)
    return data
