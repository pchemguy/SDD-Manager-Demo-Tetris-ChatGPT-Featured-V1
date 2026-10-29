"""Compile pinned TypeScript and copy only validated local production assets."""
from pathlib import Path
import os, shutil, subprocess
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ('index.html', 'styles.css', 'icon.svg')
MODULES = ('core/model.js','core/geometry.js','core/engine.js','shared/game-view.js',
           'platform/browser/input.js','platform/browser/host.js','platform/browser/main.js')
OUTPUTS = frozenset((*ASSETS, *MODULES, 'LICENSE.txt'))

def build():
    """Validate sources before cleanup; never follow links into owned output."""
    out, assets = ROOT / 'dist', ROOT / 'web'
    if out.is_symlink() or assets.is_symlink():
        raise ValueError('Build roots must not be symlinks')
    if not assets.is_dir() or {p.name for p in assets.iterdir()} != set(ASSETS):
        raise ValueError('Missing or unexpected static asset')
    sources = [assets / name for name in ASSETS] + [ROOT / 'LICENSE']
    if any(p.is_symlink() or not p.is_file() for p in sources):
        raise ValueError('Build assets must be ordinary files')
    if out.exists():
        if not out.is_dir() or any(p.is_symlink() for p in out.rglob('*')):
            raise ValueError('Unsafe generated output')
        shutil.rmtree(out)
    npm = ['cmd.exe', '/d', '/c', 'npm.cmd'] if os.name == 'nt' else ['npm']
    subprocess.run(npm + ['exec', '--offline', '--', 'tsc', '-p', 'tsconfig.json'], cwd=ROOT, check=True, timeout=60)
    out.mkdir(exist_ok=True)
    for name in ASSETS: shutil.copyfile(assets / name, out / name)
    shutil.copyfile(ROOT / 'LICENSE', out / 'LICENSE.txt')
    if {p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()} != OUTPUTS:
        raise ValueError('Unexpected compiled output inventory')
    print('Built dist from pinned local TypeScript and allowlisted assets.')

if __name__ == '__main__': build()
