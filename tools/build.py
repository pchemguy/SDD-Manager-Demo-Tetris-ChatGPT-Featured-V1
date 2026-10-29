"""Compile the local TypeScript project and copy its static entry assets."""
from pathlib import Path
import os, shutil, subprocess
ROOT = Path(__file__).resolve().parents[1]

def build():
    """Build only the owned dist directory; refuse link redirection."""
    out = ROOT / 'dist'
    if out.is_symlink():
        raise ValueError('dist must not be a symlink')
    if out.exists():
        shutil.rmtree(out)
    npm = ['cmd.exe', '/d', '/c', 'npm.cmd'] if os.name == 'nt' else ['npm']
    subprocess.run(npm + ['exec', '--offline', '--', 'tsc', '-p', 'tsconfig.json'], cwd=ROOT, check=True, timeout=60)
    out.mkdir(exist_ok=True)
    for name in ('index.html', 'styles.css'):
        source = ROOT / 'web' / name
        if source.is_symlink():
            raise ValueError('Static assets must be ordinary files')
        shutil.copyfile(source, out / name)
    print('Built dist from pinned local TypeScript and static assets.')

if __name__ == '__main__':
    build()
