import pytest
from src.processing import filter_by_state, sort_by_date
from typing import List, Dict, Any


class TestFilterByState:
    """Тесты для функции filter_by_state"""

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 3),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("UNKNOWN", 0),  # несуществующий статус
    ])
    def test_filter_by_state(self, sample_transactions: List[Dict[str, Any]], state: str, expected_count: int) -> None:
        """Тестирование фильтрации по разным статусам"""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count

        # Проверяем, что все элементы имеют нужный статус
        for item in result:
            assert item["state"] == state

    def test_filter_by_state_empty_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование фильтрации пустого списка"""
        result = filter_by_state(empty_transactions, "EXECUTED")
        assert result == []
        assert len(result) == 0

    def test_filter_by_state_default_parameter(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование фильтрации со значением по умолчанию"""
        result = filter_by_state(sample_transactions)
        # Должны вернуться только EXECUTED транзакции (значение по умолчанию)
        assert len(result) == 3
        for item in result:
            assert item["state"] == "EXECUTED"

    def test_filter_by_state_invalid_data(self, invalid_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование фильтрации некорректных данных"""
        result = filter_by_state(invalid_transactions, "EXECUTED")
        # Функция должна корректно обработать некорректные данные
        assert isinstance(result, list)


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_by_date_descending(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование сортировки по убыванию (по умолчанию)"""
        result = sort_by_date(sample_transactions)

        # Проверяем порядок дат (убывание)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

        # Проверяем, что все элементы сохранились
        assert len(result) == len(sample_transactions)

        # Первая транзакция должна быть самой новой
        assert result[0]["date"] == "2024-03-14T10:30:00.000"

    def test_sort_by_date_ascending(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование сортировки по возрастанию"""
        result = sort_by_date(sample_transactions, descending=False)

        # Проверяем порядок дат (возрастание)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

        # Первая транзакция должна быть самой старой
        assert result[0]["date"] == "2023-10-05T09:15:45.000"

    def test_sort_by_date_empty_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование сортировки пустого списка"""
        result = sort_by_date(empty_transactions)
        assert result == []

    def test_sort_by_date_single_element(self) -> None:
        """Тестирование сортировки списка с одним элементом"""
        single_transaction = [{
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-14T10:30:00.000",
            "amount": "100.00"
        }]

        result = sort_by_date(single_transaction)
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_sort_by_date_identical_dates(self) -> None:
        """Тестирование сортировки с одинаковыми датами"""
        transactions = [
            {"id": 1, "date": "2024-03-14T10:30:00.000", "state": "EXECUTED"},
            {"id": 2, "date": "2024-03-14T10:30:00.000", "state": "PENDING"},
            {"id": 3, "date": "2024-03-14T10:30:00.000", "state": "CANCELED"},
        ]

        result = sort_by_date(transactions)
        # При одинаковых датах порядок может быть любым, но без ошибок
        assert len(result) == 3

    def test_sort_by_date_invalid_data(self, invalid_transactions: List[Dict[str, Any]]) -> None:
        """Тестирование сортировки некорректных данных"""
        result = sort_by_date(invalid_transactions)
        # Функция должна обработать некорректные данные без падения
        assert isinstance(result, list)