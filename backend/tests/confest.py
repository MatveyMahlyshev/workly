import pytest
from fastapi.testclient import TestClient

from core.models import db_helper
from main import app
from core.config import settings


@pytest.fixture(scope="function")
def client():
    original_testing = db_helper.testing
    db_helper.testing = True

    with TestClient(app) as client:
        yield client

    db_helper.testing = original_testing
    db_helper.engine.sync_engine.dispose()
