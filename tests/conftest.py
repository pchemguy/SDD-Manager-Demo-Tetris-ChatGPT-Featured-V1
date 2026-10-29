"""Pytest boundaries for compiled modules and later real browser fixtures."""
from pathlib import Path
import json, subprocess
import pytest
ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def ask():
    """Run a production-module request without calculating its expected answer."""
    def execute(request):
        result = subprocess.run(['node', 'tests/support/engine_driver.mjs'], cwd=ROOT, input=json.dumps(request), text=True, capture_output=True, timeout=10, check=True)
        return json.loads(result.stdout)
    return execute
