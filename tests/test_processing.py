import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state"""

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 3),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("UNKNOWN", 0),
    ])
    def test_filter_by_state(self, sample_transactions, state: str, expected_count: int) -> None:
        """Тестирование фильтрации по разным статусам"""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count
        for item in result:
            assert item["state"] == state

    def test_filter_by_state_empty_list(self, empty_transactions) -> None:
        """Тестирование фильтрации пустого списка"""
        result = filter_by_state(empty_transactions, "EXECUTED")
        assert result == []

    def test_filter_by_state_default(self, sample_transactions) -> None:
        """Тестирование фильтрации со значением по умолчанию"""
        result = filter_by_state(sample_transactions)
        assert len(result) == 3
        for item in result:
            assert item["state"] == "EXECUTED"


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_by_date_descending(self, sample_transactions) -> None:
        """Тестирование сортировки по убыванию"""
        result = sort_by_date(sample_transactions)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)
        assert result[0]["date"] == "2024-03-14T10:30:00.000"

    def test_sort_by_date_ascending(self, sample_transactions) -> None:
        """Тестирование сортировки по возрастанию"""
        result = sort_by_date(sample_transactions, descending=False)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)
        assert result[0]["date"] == "2023-10-05T09:15:45.000"

    def test_sort_by_date_empty_list(self, empty_transactions) -> None:
        """Тестирование сортировки пустого списка"""
        result = sort_by_date(empty_transactions)
        assert result == []