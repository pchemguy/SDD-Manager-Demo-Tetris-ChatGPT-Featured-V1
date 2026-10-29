"""Independent inventory/hash expectations and extracted-byte browser acceptance."""
from pathlib import Path
import hashlib,json,shutil,stat,subprocess,sys,zipfile
import pytest
from tools.package import create_archive,verify_archive,extract_verified
from tools.check import environment
ROOT=Path(__file__).resolve().parents[2]
SOURCE='a'*40
EXPECTED_WEB={'index.html','styles.css','icon.svg','LICENSE.txt','core/model.js','core/geometry.js','core/engine.js','shared/game-view.js','platform/browser/input.js','platform/browser/host.js','platform/browser/main.js'}

@pytest.fixture
def candidate(tmp_path):
    target=tmp_path/'classic-tetris-browser.zip'
    create_archive(ROOT/'dist',ROOT/'docs/INSTALL.md',target,'0.1.0',SOURCE,True)
    return target

def test_determinism_inventory_metadata_and_checksums(candidate,tmp_path):
    other=tmp_path/'repeat/classic-tetris-browser.zip'
    create_archive(ROOT/'dist',ROOT/'docs/INSTALL.md',other,'0.1.0',SOURCE,True)
    assert candidate.read_bytes()==other.read_bytes()
    digest=hashlib.sha256(candidate.read_bytes()).hexdigest()
    assert candidate.with_suffix('.zip.sha256').read_text()==digest+'  classic-tetris-browser.zip\n'
    with zipfile.ZipFile(candidate) as z:
        names=z.namelist()
        assert names==sorted(names) and len(names)==len(set(names))
        assert set(names)=={'web/'+n for n in EXPECTED_WEB}|{'INSTALL.md','release.json','SHA256SUMS'}
        assert all(i.date_time==(1980,1,1,0,0,0) and stat.S_ISREG(i.external_attr>>16) for i in z.infolist())
        assert z.testzip() is None
        metadata=json.loads(z.read('release.json'))
        assert metadata=={'schema_version':1,'version':'0.1.0','source_commit':SOURCE,'source_dirty':True,'platform':'browser-static'}
        lines=z.read('SHA256SUMS').decode().splitlines()
        listed={line.split('  ',1)[1]:line.split('  ',1)[0] for line in lines}
        assert set(listed)==set(names)-{'SHA256SUMS'}
        for name,digest in listed.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
    assert set(verify_archive(candidate))==set(names)

@pytest.mark.parametrize('defect',['missing','extra','symlink'])
def test_source_inventory_rejects_invalid_inputs(tmp_path,defect):
    web=tmp_path/'web';shutil.copytree(ROOT/'dist',web)
    if defect=='missing':(web/'styles.css').unlink()
    if defect=='extra':(web/'unexpected.tkn').write_text('test fixture')
    if defect=='symlink':
        (web/'styles.css').unlink();(web/'styles.css').symlink_to(ROOT/'dist/styles.css')
    with pytest.raises(ValueError):create_archive(web,ROOT/'docs/INSTALL.md',tmp_path/'bad.zip','0.1.0',SOURCE,False)

@pytest.mark.parametrize('defect',['traversal','duplicate','symlink','tamper','oversized'])
def test_hostile_archive_is_rejected_before_extraction(candidate,tmp_path,defect):
    bad=tmp_path/'bad.zip'
    with zipfile.ZipFile(candidate) as old,zipfile.ZipFile(bad,'w') as new:
        for info in old.infolist():
            value=old.read(info.filename)
            if info.filename=='web/styles.css':
                if defect=='symlink':info.external_attr=(stat.S_IFLNK|0o777)<<16
                if defect=='tamper':value=b'corrupted CSS'
                if defect=='oversized':value=b'x'*(2*1024*1024+1)
            new.writestr(info,value)
        if defect=='traversal':new.writestr('../outside.txt','bad')
        if defect=='duplicate':
            with pytest.warns(UserWarning,match='Duplicate name'):new.writestr('web/index.html','duplicate')
    dest=tmp_path/'extracted'
    with pytest.raises(ValueError):extract_verified(bad,dest)
    assert not dest.exists() and not (tmp_path/'outside.txt').exists()

def test_complete_browser_suite_against_extracted_bytes(candidate,tmp_path):
    target=tmp_path/'extracted';extract_verified(candidate,target)
    result=subprocess.run([sys.executable,'tools/check.py','browser','--web-root',str(target/'web'),'--web-prefix','games/classic'],cwd=ROOT,env=environment(),capture_output=True,text=True,timeout=150)
    assert result.returncode==0,result.stdout+'\n'+result.stderr
    assert '30 passed' in result.stdout
