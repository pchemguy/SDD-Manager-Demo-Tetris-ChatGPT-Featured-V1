"""Run selected pytest suites with project-owned dependencies and deadlines."""
from pathlib import Path
import os, signal, subprocess, sys, time
ROOT = Path(__file__).resolve().parents[1]

def environment():
    """Return isolated import, browser and cache locations."""
    env = dict(os.environ)
    env['PYTHONPATH'] = str(ROOT / '.tools/python')
    env['PLAYWRIGHT_BROWSERS_PATH'] = str(ROOT / '.tools/browsers')
    env['npm_config_cache'] = str(ROOT / '.tools/npm-cache')
    return env

def _linux_children():
    """Map only this owner's direct procfs children into its PID namespace."""
    def status(path):
        return {line.split(':',1)[0]:line.split(':',1)[1].strip() for line in path.read_text().splitlines() if ':' in line}
    own = status(Path('/proc/self/status'))
    depth = len(own['NSpid'].split())
    if int(own['NSpid'].split()[-1]) != os.getpid():
        raise RuntimeError('Cannot establish process namespace ownership')
    result = []
    interface = Path(f'/proc/self/task/{own["Pid"]}/children')
    candidates = interface.read_text().split() if interface.exists() else (entry.name for entry in Path('/proc').iterdir() if entry.name.isdecimal())
    for kernel_id in candidates:
        try:
            child = status(Path('/proc') / kernel_id / 'status')
            if child['PPid'] == own['Pid']:
                result.append(int(child['NSpid'].split()[depth-1]))
        except FileNotFoundError:
            pass
    return result

def _reap_owned():
    """Kill/reap adopted descendants until none remain, with a finite deadline."""
    deadline = time.monotonic() + 5
    while children := _linux_children():
        for child in children:
            try: os.kill(child, signal.SIGKILL)
            except ProcessLookupError: pass
            try: os.waitpid(child, os.WNOHANG)
            except ChildProcessError: pass
        if time.monotonic() >= deadline:
            raise RuntimeError('Owned descendant cleanup unconfirmed')
        time.sleep(.01)

def run(args, timeout=180):
    """Bound an exclusive job; Linux subreaping also owns detached children."""
    linux = sys.platform == 'linux'
    if linux:
        import ctypes
        if _linux_children():
            raise RuntimeError('Check supervisor requires an exclusive child scope')
        if ctypes.CDLL(None, use_errno=True).prctl(36, ctypes.c_ulong(1), 0, 0, 0) != 0:
            raise RuntimeError('Child-subreaper facility unavailable')
    proc = subprocess.Popen(args, cwd=ROOT, env=environment(), start_new_session=os.name != 'nt')
    try:
        result = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == 'nt':
            subprocess.run(['taskkill.exe', '/F', '/T', '/PID', str(proc.pid)], check=False, timeout=15)
        else:
            try: os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError: pass
        proc.wait(timeout=15)
        if linux: _reap_owned()
        raise RuntimeError('Owned check process exceeded its deadline')
    if linux:
        _reap_owned()
    return result

def main():
    """Select existing suites; an individually requested missing suite fails."""
    suite = sys.argv[1] if len(sys.argv) > 1 else 'all'
    allowed = ['environment', 'core', 'browser', 'package']
    if suite not in allowed + ['all']:
        raise SystemExit('Unknown suite')
    paths = [f'tests/{name}' for name in (allowed if suite == 'all' else [suite]) if list((ROOT / 'tests' / name).glob('test_*.py'))]
    if not paths:
        raise SystemExit('No implemented tests in selected suite')
    print('Selected implemented suites: ' + ', '.join(paths), flush=True)
    raise SystemExit(run([sys.executable, '-m', 'pytest', '-q', *paths]))

if __name__ == '__main__':
    main()
