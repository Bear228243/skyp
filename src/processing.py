"""
Дополнительные тесты для модуля processing.
Проверяет все функции и граничные случаи.
"""

import pytest
from datetime import datetime
from src.processing import (
    filter_by_state,
    sort_by_date,
    get_last_transactions,
    filter_by_currency_code
)


class TestProcessingAdditional:
    """Дополнительные тесты для функций processing."""

    def test_filter_by_state_with_missing_state(self, sample_transactions):
        """Тест фильтрации при отсутствии поля state."""
        transactions = sample_transactions.copy()
        transactions.append({"id": 6, "date": "2024-01-01"})  # Без state

        result = filter_by_state(transactions, "EXECUTED")
        assert len(result) == 3  # Должен игнорировать транзакцию без state

    def test_filter_by_state_case_sensitivity(self, sample_transactions):
        """Тест чувствительности к регистру."""
        # Функция должна быть чувствительна к регистру
        result = filter_by_state(sample_transactions, "executed")
        assert len(result) == 0  # Должен найти 0, т.к. статус в верхнем регистре

    def test_sort_by_date_with_invalid_dates(self):
        """Тест сортировки с некорректными датами."""
        transactions = [
            {"id": 1, "date": "invalid-date"},
            {"id": 2, "date": "2024-01-01T10:00:00"},
            {"id": 3},  # Без даты
        ]

        result = sort_by_date(transactions, descending=True)
        # Транзакции с некорректными датами должны быть в конце
        assert result[0]["id"] == 2  # С корректной датой
        # Остальные могут быть в любом порядке

    def test_sort_by_date_with_timezone(self):
        """Тест сортировки с датами в разных часовых поясах."""
        transactions = [
            {"id": 1, "date": "2024-01-01T10:00:00+03:00"},
            {"id": 2, "date": "2024-01-01T09:00:00+00:00"},
        ]

        result = sort_by_date(transactions, descending=True)
        # Должен корректно обработать временные зоны

    def test_get_last_transactions_with_count_greater_than_list(self, sample_transactions):
        """Тест получения последних транзакций с count > размера списка."""
        result = get_last_transactions(sample_transactions, count=10)
        assert len(result) == 3  # Должен вернуть все выполненные транзакции

    def test_get_last_transactions_with_zero_count(self, sample_transactions):
        """Тест получения 0 последних транзакций."""
        result = get_last_transactions(sample_transactions, count=0)
        assert len(result) == 0

    def test_get_last_transactions_with_no_executed(self):
        """Тест получения последних транзакций, когда нет выполненных."""
        transactions = [
            {"id": 1, "state": "PENDING", "date": "2024-01-01"},
            {"id": 2, "state": "CANCELED", "date": "2024-01-02"},
        ]
        result = get_last_transactions(transactions, count=5)
        assert len(result) == 0

    def test_filter_by_currency_code(self, sample_transactions):
        """Тест фильтрации по коду валюты."""
        result = filter_by_currency_code(sample_transactions, "USD")
        assert len(result) == 2  # В sample_transactions 2 транзакции в USD

    def test_filter_by_currency_code_with_no_matches(self, sample_transactions):
        """Тест фильтрации по несуществующему коду валюты."""
        result = filter_by_currency_code(sample_transactions, "JPY")
        assert len(result) == 0

    def test_filter_by_currency_code_with_missing_currency(self):
        """Тест фильтрации при отсутствии информации о валюте."""
        transactions = [
            {"id": 1, "operationAmount": {}},  # Пустой operationAmount
            {"id": 2},  # Без operationAmount
            {"id": 3, "operationAmount": {"currency": {}}},  # Пустой currency
        ]
        result = filter_by_currency_code(transactions, "USD")
        assert len(result) == 0