"""
Тесты для модуля processing.
Проверяет функции фильтрации и сортировки транзакций.
"""

import pytest
from src.processing import filter_by_state, sort_by_date, get_last_transactions, filter_by_currency_code


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041'},
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций."""
    return []


class TestFilterByState:
    """Тесты для функции filter_by_state"""

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 3),
        ("CANCELED", 2),
        ("PENDING", 0),
    ])
    def test_filter_by_state(self, sample_transactions, state, expected_count):
        """Тестирование фильтрации по разным статусам"""
        result = filter_by_state(sample_transactions, state)
        assert len(result) == expected_count
        for item in result:
            assert item["state"] == state

    def test_filter_by_state_default(self, sample_transactions):
        """Тестирование фильтрации со значением по умолчанию"""
        result = filter_by_state(sample_transactions)
        assert len(result) == 3
        for item in result:
            assert item["state"] == "EXECUTED"

    def test_filter_by_state_empty(self, empty_transactions):
        """Тестирование фильтрации пустого списка"""
        result = filter_by_state(empty_transactions)
        assert result == []

    def test_filter_by_state_missing_state(self):
        """Тест при отсутствии поля state"""
        transactions = [{"id": 1}, {"id": 2, "state": "EXECUTED"}]
        result = filter_by_state(transactions, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_descending(self, sample_transactions):
        """Тест сортировки по убыванию"""
        result = sort_by_date(sample_transactions)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)
        assert result[0]["date"] == "2019-08-26T10:50:58.294041"

    def test_sort_ascending(self, sample_transactions):
        """Тест сортировки по возрастанию"""
        result = sort_by_date(sample_transactions, descending=False)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)
        assert result[0]["date"] == "2018-06-30T02:08:58.425572"

    def test_sort_empty(self, empty_transactions):
        """Тест сортировки пустого списка"""
        result = sort_by_date(empty_transactions)
        assert result == []

    def test_sort_with_invalid_dates(self):
        """Тест сортировки с некорректными датами"""
        transactions = [
            {"id": 1, "date": "invalid"},
            {"id": 2, "date": "2019-01-01T00:00:00"},
            {"id": 3},  # без даты
        ]
        result = sort_by_date(transactions)
        # Транзакция с корректной датой должна быть первой
        assert result[0]["id"] == 2


class TestGetLastTransactions:
    """Тесты для функции get_last_transactions"""

    def test_get_last_default(self, sample_transactions):
        """Тест получения последних 5 транзакций"""
        result = get_last_transactions(sample_transactions)
        assert len(result) == 3  # Всего 3 EXECUTED
        # Проверка порядка (по убыванию даты)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_get_last_custom_count(self, sample_transactions):
        """Тест получения последних 2 транзакций"""
        result = get_last_transactions(sample_transactions, count=2)
        assert len(result) == 2
        assert result[0]["date"] == "2019-08-26T10:50:58.294041"
        assert result[1]["date"] == "2019-07-03T18:35:29.512364"

    def test_get_last_zero_count(self, sample_transactions):
        """Тест с count=0"""
        result = get_last_transactions(sample_transactions, count=0)
        assert len(result) == 0

    def test_get_last_no_executed(self):
        """Тест когда нет выполненных транзакций"""
        transactions = [{"id": 1, "state": "CANCELED", "date": "2024-01-01"}]
        result = get_last_transactions(transactions)
        assert len(result) == 0

    def test_get_last_empty(self, empty_transactions):
        """Тест с пустым списком"""
        result = get_last_transactions(empty_transactions)
        assert result == []


class TestFilterByCurrencyCode:
    """Тесты для функции filter_by_currency_code"""

    @pytest.fixture
    def transactions_with_currency(self):
        """Фикстура с транзакциями, содержащими валюту"""
        return [
            {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
            {"id": 4, "operationAmount": {"currency": {"code": "EUR"}}},
            {"id": 5},  # без operationAmount
            {"id": 6, "operationAmount": {}},  # пустой operationAmount
        ]

    def test_filter_rub(self, transactions_with_currency):
        """Тест фильтрации по RUB"""
        result = filter_by_currency_code(transactions_with_currency, "RUB")
        assert len(result) == 2
        for item in result:
            assert item["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_usd(self, transactions_with_currency):
        """Тест фильтрации по USD"""
        result = filter_by_currency_code(transactions_with_currency, "USD")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_no_matches(self, transactions_with_currency):
        """Тест фильтрации по несуществующей валюте"""
        result = filter_by_currency_code(transactions_with_currency, "GBP")
        assert len(result) == 0

    def test_filter_empty(self):
        """Тест фильтрации пустого списка"""
        result = filter_by_currency_code([], "RUB")
        assert result == []
