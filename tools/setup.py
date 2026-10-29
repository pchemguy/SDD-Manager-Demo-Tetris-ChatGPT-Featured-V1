"""Install locked project-local tools and matching isolated managed browsers."""
from pathlib import Path
import os, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]

def main():
    """Provision without changing global packages or browser installations."""
    if '--official-fallback' in sys.argv:
        subprocess.run([sys.executable, str(ROOT / 'tools/browser_fallback.py')], check=True, timeout=400)
        return
    target = ROOT / '.tools/python'
    target.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONPATH=str(target), PLAYWRIGHT_BROWSERS_PATH=str(ROOT / '.tools/browsers'), PIP_CACHE_DIR=str(ROOT / '.tools/pip-cache'), npm_config_cache=str(ROOT / '.tools/npm-cache'))
    npm = ['cmd.exe', '/d', '/c', 'npm.cmd'] if os.name == 'nt' else ['npm']
    subprocess.run(npm + ['ci', '--ignore-scripts'], cwd=ROOT, env=env, check=True, timeout=120)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '--require-hashes', '--target', str(target), '-r', 'requirements.lock'], cwd=ROOT, env=env, check=True, timeout=180)
    subprocess.run([sys.executable, '-m', 'playwright', 'install', '--only-shell', 'chromium', 'firefox'], cwd=ROOT, env=env, check=True, timeout=240)

if __name__ == '__main__':
    main()
