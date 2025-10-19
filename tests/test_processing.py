import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 0),
    ],
)
def test_filter_by_state(sample_operations, state, expected_count):
    """Проверяет фильтрацию операций по ключу 'state'."""
    result = filter_by_state(sample_operations, state)
    assert len(result) == expected_count


def test_filter_by_state_default(sample_operations):
    """Проверяет значение параметра state по умолчанию."""
    result = filter_by_state(sample_operations)
    assert all(op["state"] == "EXECUTED" for op in result)


@pytest.mark.parametrize("reverse", [True, False])
def test_sort_by_date(sample_operations, reverse):
    """Проверяет сортировку по дате в обоих направлениях."""
    sorted_ops = sort_by_date(sample_operations, reverse=reverse)
    dates = [op["date"] for op in sorted_ops]
    assert dates == sorted(dates, reverse=reverse)


def test_sort_by_date_equal_dates():
    """Проверяет корректность сортировки при одинаковых датах."""
    ops = [
        {"id": 1, "state": "EXECUTED", "date": "2020-01-01T12:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2020-01-01T12:00:00"},
    ]
    sorted_ops = sort_by_date(ops)
    assert sorted_ops == ops
