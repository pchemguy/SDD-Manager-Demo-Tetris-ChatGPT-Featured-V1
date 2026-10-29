"""Run selected pytest suites with project-owned dependencies and deadlines."""
from pathlib import Path
import os, signal, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]

def environment():
    """Return isolated import, browser and cache locations."""
    env = dict(os.environ)
    env['PYTHONPATH'] = str(ROOT / '.tools/python')
    env['PLAYWRIGHT_BROWSERS_PATH'] = str(ROOT / '.tools/browsers')
    env['npm_config_cache'] = str(ROOT / '.tools/npm-cache')
    return env

def run(args, timeout=180):
    """Bound the whole owned process group, including hung browser creation."""
    proc = subprocess.Popen(args, cwd=ROOT, env=environment(), start_new_session=os.name != 'nt')
    try:
        return proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == 'nt':
            subprocess.run(['taskkill.exe', '/F', '/T', '/PID', str(proc.pid)], check=False, timeout=15)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
        proc.wait(timeout=15)
        raise RuntimeError('Owned check process exceeded its deadline')

def main():
    """Select existing suites; an individually requested missing suite fails."""
    suite = sys.argv[1] if len(sys.argv) > 1 else 'all'
    allowed = ['environment', 'core', 'browser', 'package']
    if suite not in allowed + ['all']:
        raise SystemExit('Unknown suite')
    paths = [f'tests/{name}' for name in (allowed if suite == 'all' else [suite]) if list((ROOT / 'tests' / name).glob('test_*.py'))]
    if not paths:
        raise SystemExit('No implemented tests in selected suite')
    raise SystemExit(run([sys.executable, '-m', 'pytest', '-q', *paths]))

if __name__ == '__main__':
    main()
