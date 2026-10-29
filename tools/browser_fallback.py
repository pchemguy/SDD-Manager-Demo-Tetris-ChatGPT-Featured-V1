"""Recover matching Linux browser assets from documented official sources."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, platform, stat, time, urllib.request, zipfile, subprocess, sys, re
ROOT = Path(__file__).resolve().parents[1]

def download(url, target):
    """Download a finite ordinary ZIP, validating the full archive before use."""
    deadline = time.monotonic() + 180
    with urllib.request.urlopen(url, timeout=30) as response, target.open('wb') as out:
        total = 0
        while data := response.read(1024 * 1024):
            total += len(data)
            if total > 512 * 1024 * 1024 or time.monotonic() > deadline:
                raise RuntimeError('Browser download exceeded bounds')
            out.write(data)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('Browser archive CRC failed')
    return hashlib.sha256(target.read_bytes()).hexdigest()

def extract(archive_path, destination):
    """Reject traversal/symlink/device entries and preserve executable modes."""
    if destination.is_symlink():
        raise ValueError('Browser destination is a link')
    with zipfile.ZipFile(archive_path) as archive:
        for item in archive.infolist():
            path = PurePosixPath(item.filename)
            mode = item.external_attr >> 16
            if path.is_absolute() or '..' in path.parts or '\\' in item.filename or stat.S_ISLNK(mode):
                raise ValueError('Unsafe browser archive member')
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError('Special browser archive member')
        for item in archive.infolist():
            target = destination / item.filename
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(item) as src, target.open('wb') as out:
                    while data := src.read(1024 * 1024):
                        out.write(data)
                mode = item.external_attr >> 16
                if mode & 0o111:
                    target.chmod(0o755)
    (destination / 'INSTALLATION_COMPLETE').touch()

def main():
    """Use the installed runner's exact revisions, never a guessed substitute."""
    if (ROOT / '.tools/browsers/__dirlock').exists():
        raise RuntimeError('Reconcile the owning installer before fallback extraction')
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise RuntimeError('This documented fallback is Linux x86_64 only')
    metadata = json.loads((ROOT / '.tools/python/playwright/driver/package/browsers.json').read_text())
    browsers = {b['name']: b for b in metadata['browsers']}
    shell = browsers['chromium-headless-shell']
    version = shell['browserVersion']
    with urllib.request.urlopen(f'https://googlechromelabs.github.io/chrome-for-testing/{version}.json', timeout=25) as response:
        cft = json.load(response)
    url = next(x['url'] for x in cft['downloads']['chrome-headless-shell'] if x['platform'] == 'linux64')
    if not url.startswith(f'https://storage.googleapis.com/chrome-for-testing-public/{version}/'):
        raise ValueError('Unexpected official CfT asset location')
    work = ROOT / '.work/downloads'
    work.mkdir(parents=True, exist_ok=True)
    records = []
    entries = [(url, f'chromium_headless_shell-{shell["revision"]}')]
    env = dict(os.environ, PYTHONPATH=str(ROOT / '.tools/python'), PLAYWRIGHT_BROWSERS_PATH=str(ROOT / '.tools/browsers'))
    planned = subprocess.check_output([sys.executable, '-m', 'playwright', 'install', '--dry-run', 'firefox'], env=env, text=True, timeout=30)
    firefox_url = next(u for u in re.findall(r'Download fallback 1:\s+(https://\S+)', planned) if '/firefox/' in u)
    if not firefox_url.startswith('https://playwright.download.prss.microsoft.com/'):
        raise ValueError('Unexpected official Firefox fallback')
    entries.append((firefox_url, f'firefox-{browsers["firefox"]["revision"]}'))
    ffmpeg = browsers['ffmpeg']
    entries.append((f'https://playwright.download.prss.microsoft.com/dbazure/download/playwright/builds/ffmpeg/{ffmpeg["revision"]}/ffmpeg-linux.zip', f'ffmpeg-{ffmpeg["revision"]}'))
    for index, (source, directory) in enumerate(entries):
        if (ROOT / '.tools/browsers' / directory / 'INSTALLATION_COMPLETE').exists():
            records.append({'source': source, 'directory': directory, 'reused': True})
            print('Reused contained installation ' + directory, flush=True)
            continue
        archive = work / f'official-{index}.zip'
        digest = download(source, archive)
        extract(archive, ROOT / '.tools/browsers' / directory)
        records.append({'source': source, 'directory': directory, 'sha256': digest, 'size': archive.stat().st_size})
        print('Validated/extracted ' + directory, flush=True)
    (ROOT / '.work/browser-fallback.json').write_text(json.dumps(records, indent=2))

if __name__ == '__main__':
    main()
