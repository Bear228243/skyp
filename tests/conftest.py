import pytest


@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми банковскими операциями."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2020-01-01T12:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2020-01-02T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2020-01-03T12:00:00"},
    ]
