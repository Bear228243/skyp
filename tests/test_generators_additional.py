"""
Дополнительные тесты для модуля generators.
Проверяет граничные случаи и обработку ошибок.
"""

import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


class TestGeneratorsAdditional:
    """Дополнительные тесты для функций-генераторов."""

    def test_filter_by_currency_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_filter_by_currency_no_operation_amount(self):
        """Тест фильтрации при отсутствии operationAmount."""
        transactions = [
            {"id": 1},
            {"id": 2, "operationAmount": {}},
            {"id": 3, "operationAmount": {"currency": {"code": "USD"}}}
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_filter_by_currency_no_currency_field(self):
        """Тест фильтрации при отсутствии поля currency."""
        transactions = [
            {"id": 1, "operationAmount": {"amount": "100"}},
            {"id": 2, "operationAmount": {"currency": {}}},
            {"id": 3, "operationAmount": {"currency": {"code": "USD"}}}
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_filter_by_currency_no_matches(self):
        """Тест фильтрации без совпадений."""
        transactions = [
            {"operationAmount": {"currency": {"code": "RUB"}}},
            {"operationAmount": {"currency": {"code": "EUR"}}}
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 0

    def test_filter_by_currency_multiple_matches(self):
        """Тест фильтрации с несколькими совпадениями."""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}}
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_transaction_descriptions_empty_list(self):
        """Тест получения описаний из пустого списка."""
        result = list(transaction_descriptions([]))
        assert len(result) == 0

    def test_transaction_descriptions_missing_description(self):
        """Тест получения описаний при отсутствии поля description."""
        transactions = [
            {"id": 1},
            {"id": 2, "description": ""},
            {"id": 3, "description": "Тестовое описание"},
            {"id": 4, "description": None}  # type: ignore
        ]
        result = list(transaction_descriptions(transactions))
        assert len(result) == 1
        assert result[0] == "Тестовое описание"

    def test_transaction_descriptions_all_present(self):
        """Тест получения описаний когда все поля присутствуют."""
        transactions = [
            {"description": "Описание 1"},
            {"description": "Описание 2"},
            {"description": "Описание 3"}
        ]
        result = list(transaction_descriptions(transactions))
        assert len(result) == 3
        assert result == ["Описание 1", "Описание 2", "Описание 3"]

    def test_card_number_generator_start_equals_stop(self):
        """Тест генерации когда start == stop."""
        result = list(card_number_generator(5, 5))
        assert len(result) == 1
        assert result[0] == "0000 0000 0000 0005"

    def test_card_number_generator_start_greater_than_stop(self):
        """Тест генерации когда start > stop."""
        result = list(card_number_generator(10, 5))
        assert len(result) == 0

    def test_card_number_generator_zero_start(self):
        """Тест генерации с нулевым start."""
        result = list(card_number_generator(0, 2))
        assert len(result) == 3
        assert result[0] == "0000 0000 0000 0000"
        assert result[1] == "0000 0000 0000 0001"
        assert result[2] == "0000 0000 0000 0002"

    def test_card_number_generator_large_range(self):
        """Тест генерации большого диапазона."""
        result = list(card_number_generator(9999999999999990, 9999999999999995))
        assert len(result) == 6
        assert result[0] == "9999 9999 9999 9990"
        assert result[-1] == "9999 9999 9999 9995"

    def test_card_number_generator_formatting(self):
        """Тест форматирования номеров карт."""
        result = list(card_number_generator(123456789012345, 123456789012345))
        assert result[0] == "0123 4567 8901 2345"

    def test_card_number_generator_leading_zeros(self):
        """Тест генерации с ведущими нулями."""
        result = list(card_number_generator(1, 3))
        assert result[0] == "0000 0000 0000 0001"
        assert result[1] == "0000 0000 0000 0002"
        assert result[2] == "0000 0000 0000 0003"
