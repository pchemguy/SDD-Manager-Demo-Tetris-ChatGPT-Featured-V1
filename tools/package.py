"""Prepare deterministic static-browser ZIPs; validate data before extraction."""
from pathlib import Path
import argparse,hashlib,json,re,stat,subprocess,tempfile,zipfile,os
try:
    from .build import ROOT,OUTPUTS,build
except ImportError:
    from build import ROOT,OUTPUTS,build
NAME='classic-tetris-browser.zip'
MEMBERS=frozenset({'web/'+n for n in OUTPUTS}|{'INSTALL.md','release.json','SHA256SUMS'})
MAX_FILE=2*1024*1024
MAX_TOTAL=8*1024*1024

def digest(data):
    """Hash exact bytes rather than text-normalized content."""
    return hashlib.sha256(data).hexdigest()

def manifest(payload):
    return ''.join(f'{digest(value)}  {name}\n' for name,value in sorted(payload.items())).encode('ascii')

def ordinary(path):
    return path.is_file() and not path.is_symlink()

def safe_parent(path):
    if any(parent.is_symlink() for parent in (path,*path.parents)):
        raise ValueError('Output paths must not follow symlinks')

def create_archive(web,install,target,version,source_commit,source_dirty):
    """Package an explicit built tree and identity; callers own build provenance."""
    web,install,target=Path(web),Path(install),Path(target)
    if not re.fullmatch(r'\d+\.\d+\.\d+',version) or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}',source_commit) or type(source_dirty) is not bool:
        raise ValueError('Invalid package identity')
    if web.is_symlink() or not web.is_dir() or not ordinary(install):
        raise ValueError('Package inputs must be ordinary files/directories')
    entries=list(web.rglob('*'))
    if any(p.is_symlink() or not (p.is_dir() or p.is_file()) for p in entries):
        raise ValueError('Package input links/special files are forbidden')
    files={p.relative_to(web).as_posix():p for p in entries if p.is_file()}
    if set(files)!=OUTPUTS:raise ValueError('Missing or extra production file')
    payload={'web/'+name:path.read_bytes() for name,path in files.items()}
    payload['INSTALL.md']=install.read_bytes()
    payload['release.json']=(json.dumps(dict(schema_version=1,version=version,source_commit=source_commit,source_dirty=source_dirty,platform='browser-static'),sort_keys=True,indent=2)+'\n').encode('utf-8')
    if any(len(value)>MAX_FILE for value in payload.values()) or sum(map(len,payload.values()))>MAX_TOTAL:
        raise ValueError('Package payload exceeds limits')
    payload['SHA256SUMS']=manifest(payload)
    safe_parent(target);safe_parent(target.with_suffix(target.suffix+'.sha256'));target.parent.mkdir(parents=True,exist_ok=True)
    # One owned temporary file prevents a failed write replacing a valid archive.
    handle,temp=tempfile.mkstemp(prefix='.package-',suffix='.tmp',dir=target.parent);os.close(handle)
    temporary=Path(temp)
    try:
        with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for name,value in sorted(payload.items()):
                info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.create_system=3
                info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,value,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        verify_archive(temporary)
        temporary.replace(target)
        target.with_suffix(target.suffix+'.sha256').write_text(f'{digest(target.read_bytes())}  {target.name}\n',encoding='ascii',newline='\n')
    finally:temporary.unlink(missing_ok=True)
    return target

def verify_archive(path):
    """Return bounded, integrity-checked bytes without creating any output paths."""
    try:
        with zipfile.ZipFile(path) as archive:
            infos=archive.infolist();names=[i.filename for i in infos]
            if len(names)!=len(MEMBERS) or set(names)!=MEMBERS:
                raise ValueError('Invalid archive inventory or duplicates')
            if sum(i.file_size for i in infos)>MAX_TOTAL:
                raise ValueError('Archive exceeds size limit')
            for info in infos:
                if info.flag_bits&1 or info.file_size>MAX_FILE or info.create_system!=3 or not stat.S_ISREG(info.external_attr>>16):
                    raise ValueError('Unsafe archive member')
            payload={info.filename:archive.read(info) for info in infos}
        expected=manifest({name:value for name,value in payload.items() if name!='SHA256SUMS'})
        if payload['SHA256SUMS']!=expected:raise ValueError('Payload hash mismatch')
        metadata=json.loads(payload['release.json'])
        if set(metadata)!={'schema_version','version','source_commit','source_dirty','platform'} or metadata['schema_version']!=1 or metadata['platform']!='browser-static' or type(metadata['source_dirty']) is not bool or not re.fullmatch(r'\d+\.\d+\.\d+',metadata['version']) or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}',metadata['source_commit']):
            raise ValueError('Invalid release metadata')
        return payload
    except (zipfile.BadZipFile,KeyError,TypeError,json.JSONDecodeError,UnicodeDecodeError,RuntimeError) as error:
        raise ValueError('Invalid browser archive') from error

def extract_verified(path,destination):
    """Extract validated known members only into a new owned directory."""
    payload=verify_archive(path);destination=Path(destination);safe_parent(destination)
    if destination.exists():raise ValueError('Extraction destination must be new')
    destination.mkdir(parents=True)
    for name,value in payload.items():
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(value)
    return destination

def main():
    """Build current source, package candidate identity, optionally require clean Git."""
    parser=argparse.ArgumentParser();parser.add_argument('--require-clean',action='store_true');args=parser.parse_args()
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT))
    if args.require_clean and dirty:raise SystemExit('Release packaging requires a clean source tree')
    build()
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()!=source:
        raise RuntimeError('Source commit changed during packaging')
    version=json.loads((ROOT/'package.json').read_text())['version']
    target=create_archive(ROOT/'dist',ROOT/'docs/INSTALL.md',ROOT/'artifacts'/NAME,version,source,dirty)
    print(f'{target.name}: version {version}, source {source}, source_dirty={dirty}, SHA-256 {digest(target.read_bytes())}')

if __name__=='__main__':main()
