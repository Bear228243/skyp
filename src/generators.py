"""
Дополнительные тесты для модуля generators.
Проверяет все функции и граничные случаи.
"""

import pytest
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
    card_number_range_generator
)


class TestGeneratorsAdditional:
    """Дополнительные тесты для функций-генераторов."""

    def test_filter_by_currency_with_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_filter_by_currency_with_missing_operation_amount(self):
        """Тест фильтрации при отсутствии operationAmount."""
        transactions = [
            {"id": 1},  # Без operationAmount
            {"id": 2, "operationAmount": {}},  # Пустой operationAmount
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert result == []

    def test_filter_by_currency_with_missing_currency(self):
        """Тест фильтрации при отсутствии информации о валюте."""
        transactions = [
            {"id": 1, "operationAmount": {"amount": "100"}},  # Без currency
            {"id": 2, "operationAmount": {"currency": {}}},  # Пустой currency
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert result == []

    def test_transaction_descriptions_with_empty_list(self):
        """Тест получения описаний из пустого списка."""
        result = list(transaction_descriptions([]))
        assert result == []

    def test_transaction_descriptions_with_missing_description(self):
        """Тест получения описаний при отсутствии поля description."""
        transactions = [
            {"id": 1},  # Без description
            {"id": 2, "description": ""},  # Пустое описание
            {"id": 3, "description": "Есть описание"},
        ]
        result = list(transaction_descriptions(transactions))
        assert len(result) == 1  # Только транзакция с непустым описанием
        assert result[0] == "Есть описание"

    def test_card_number_generator_with_invalid_range(self):
        """Тест генерации с некорректным диапазоном."""
        # start > stop
        result = list(card_number_generator(10, 5))
        assert result == []

    def test_card_number_generator_with_large_numbers(self):
        """Тест генерации с большими числами."""
        generator = card_number_generator(9999999999999995, 9999999999999999)
        result = list(generator)
        assert len(result) == 5
        assert result[0] == "9999 9999 9999 9995"
        assert result[-1] == "9999 9999 9999 9999"

    def test_card_number_generator_with_single_number(self):
        """Тест генерации одного номера."""
        result = list(card_number_generator(1234, 1234))
        assert len(result) == 1
        assert result[0] == "0000 0000 0000 1234"

    def test_card_number_range_generator(self):
        """Тест генерации номеров в диапазоне с форматированием."""
        generator = card_number_range_generator(
            "0000 0000 0000 0001",
            "0000 0000 0000 0003"
        )
        result = list(generator)
        assert len(result) == 3
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]

    def test_card_number_range_generator_with_invalid_format(self):
        """Тест генерации с некорректным форматом."""
        generator = card_number_range_generator("invalid", "format")
        with pytest.raises(ValueError):
            list(generator)