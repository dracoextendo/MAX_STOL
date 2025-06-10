import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client