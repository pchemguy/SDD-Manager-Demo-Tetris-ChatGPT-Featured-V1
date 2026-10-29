"""Protect the official fallback's extraction boundary with hostile ZIPs."""
import stat, zipfile
import pytest
from tools.browser_fallback import extract

@pytest.mark.parametrize('name', ['../escape', '/absolute', 'dir\\escape'])
def test_rejects_escaping_member(tmp_path, name):
    """A remote entry must never write outside its owned browser root."""
    archive = tmp_path / 'bad.zip'
    with zipfile.ZipFile(archive, 'w') as out:
        out.writestr(name, 'unexpected')
    with pytest.raises(ValueError, match='Unsafe'):
        extract(archive, tmp_path / 'browser')

def test_rejects_link_member(tmp_path):
    """A ZIP symlink must not redirect subsequent extraction writes."""
    archive = tmp_path / 'link.zip'
    item = zipfile.ZipInfo('link')
    item.external_attr = (stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(archive, 'w') as out:
        out.writestr(item, '/outside')
    with pytest.raises(ValueError, match='Unsafe'):
        extract(archive, tmp_path / 'browser')
