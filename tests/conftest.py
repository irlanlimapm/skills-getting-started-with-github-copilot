import copy
import pytest

from fastapi.testclient import TestClient
from src.app import app, activities as activities_data

ORIGINAL_ACTIVITIES = copy.deepcopy(activities_data)


@pytest.fixture(autouse=True)
def reset_activities():
    activities_data.clear()
    activities_data.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities_data.clear()
    activities_data.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app)
