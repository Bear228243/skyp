import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state"""

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 3),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("UNKNOWN", 0),  # несуществующий статус
    ])
    def test_filter_by_state(self, sample_transactions, state, expected_count):
        """Тестирование фильтрации по разным статусам"""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count

        # Проверяем, что все элементы имеют нужный статус
        for item in result:
            assert item["state"] == state

    def test_filter_by_state_empty_list(self, empty_transactions):
        """Тестирование фильтрации пустого списка"""
        result = filter_by_state(empty_transactions, "EXECUTED")
        assert result == []
        assert len(result) == 0

    def test_filter_by_state_default_parameter(self, sample_transactions):
        """Тестирование фильтрации со значением по умолчанию"""
        result = filter_by_state(sample_transactions)
        # Проверяем, что функция работает без явного указания state
        assert isinstance(result, list)

    def test_filter_by_state_case_sensitivity(self, sample_transactions):
        """Тестирование чувствительности к регистру"""
        result_lower = filter_by_state(sample_transactions, "executed")
        result_upper = filter_by_state(sample_transactions, "EXECUTED")

        # Результаты должны быть одинаковыми или функция должна обрабатывать регистр
        assert len(result_lower) == len(result_upper)


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_by_date_descending(self, sample_transactions):
        """Тестирование сортировки по убыванию"""
        result = sort_by_date(sample_transactions)

        # Проверяем порядок дат (убывание)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

        # Проверяем, что все элементы сохранились
        assert len(result) == len(sample_transactions)

    def test_sort_by_date_ascending(self, sample_transactions):
        """Тестирование сортировки по возрастанию"""
        result = sort_by_date(sample_transactions, descending=False)

        # Проверяем порядок дат (возрастание)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

    def test_sort_by_date_empty_list(self, empty_transactions):
        """Тестирование сортировки пустого списка"""
        result = sort_by_date(empty_transactions)
        assert result == []

    def test_sort_by_date_single_element(self):
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

    def test_sort_by_date_identical_dates(self):
        """Тестирование сортировки с одинаковыми датами"""
        transactions = [
            {"id": 1, "date": "2024-03-14T10:30:00.000", "state": "EXECUTED"},
            {"id": 2, "date": "2024-03-14T10:30:00.000", "state": "PENDING"},
            {"id": 3, "date": "2024-03-14T10:30:00.000", "state": "CANCELED"},
        ]

        result = sort_by_date(transactions)
        # При одинаковых датах порядок может быть любым, но без ошибок
        assert len(result) == 3

    @pytest.mark.parametrize("invalid_date", [
        "invalid_date",
        "",
        "2024/03/14",
        None,
    ])
    def test_sort_by_date_invalid_format(self, invalid_date):
        """Тестирование сортировки с некорректными датами"""
        transactions = [
            {"id": 1, "date": "2024-03-14T10:30:00.000", "state": "EXECUTED"},
            {"id": 2, "date": invalid_date, "state": "PENDING"},
        ]

        # Функция должна обрабатывать некорректные даты без падения
        result = sort_by_date(transactions)
        assert isinstance(result, list)