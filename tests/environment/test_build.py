"""Build preflight must reject missing/extra assets and redirected inputs."""
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('build_tool',ROOT/'tools/build.py')
build_tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(build_tool)

@pytest.mark.parametrize('defect',['missing','extra','symlink'])
def test_rejects_invalid_asset_tree(tmp_path,monkeypatch,defect):
    (tmp_path/'web').mkdir()
    for name in ('index.html','styles.css','icon.svg'):(tmp_path/'web'/name).write_text('asset')
    (tmp_path/'LICENSE').write_text('notice')
    if defect=='missing':(tmp_path/'web/styles.css').unlink()
    if defect=='extra':(tmp_path/'web/secret.tkn').write_text('not a token')
    if defect=='symlink':
        (tmp_path/'web/styles.css').unlink();(tmp_path/'web/styles.css').symlink_to(tmp_path/'LICENSE')
    monkeypatch.setattr(build_tool,'ROOT',tmp_path)
    monkeypatch.setattr(build_tool.subprocess,'run',lambda *a,**k:pytest.fail('compilation started before invalid input rejection'))
    with pytest.raises(ValueError):build_tool.build()
