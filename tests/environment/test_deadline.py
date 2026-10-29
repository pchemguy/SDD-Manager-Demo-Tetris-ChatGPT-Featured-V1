"""A timed-out check must not leave its owned detached descendants running."""
import os, signal, sys, time
import pytest
from tools.check import run

@pytest.mark.skipif(sys.platform != 'linux', reason='Observed Linux process-ownership regression')
def test_deadline_reaps_detached_descendant(tmp_path):
    """Reproduce a detached browser-like child escaping an ordinary killpg."""
    record = tmp_path / 'child.pid'
    script = "import subprocess,sys,time; from pathlib import Path; p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True); Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(30)"
    child = None
    try:
        with pytest.raises(RuntimeError, match='deadline'):
            run([sys.executable, '-c', script, str(record)], timeout=1)
        child = int(record.read_text())
        with pytest.raises(ProcessLookupError):
            os.kill(child, 0)
    finally:
        if child is None and record.exists():child=int(record.read_text())
        if child is not None:
            try:os.kill(child, signal.SIGKILL)
            except ProcessLookupError:pass

@pytest.mark.skipif(sys.platform != 'linux', reason='Linux adopted-child cleanup')
def test_normal_job_reaps_exited_descendant(tmp_path):
    """A finished child's reap is normal job cleanup, not a false test failure."""
    record = tmp_path / 'finished.pid'
    script = "import subprocess,sys,os; from pathlib import Path; p=subprocess.Popen([sys.executable,'-c','pass'],stdout=subprocess.PIPE,start_new_session=True); Path(sys.argv[1]).write_text(str(p.pid)); p.stdout.read(); os._exit(0)"
    assert run([sys.executable, '-c', script, str(record)], timeout=5) == 0
    with pytest.raises(ProcessLookupError):
        os.kill(int(record.read_text()), 0)
