"""
Тесты для модуля generators.
Проверяет функции-генераторы для работы с транзакциями.
"""

import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    @pytest.fixture
    def transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return [
            {
                "id": 1,
                "operationAmount": {
                    "amount": "100.00",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 2,
                "operationAmount": {
                    "amount": "200.00",
                    "currency": {"code": "RUB"}
                }
            },
            {
                "id": 3,
                "operationAmount": {
                    "amount": "300.00",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 4,
                "operationAmount": {
                    "amount": "400.00",
                    "currency": {"code": "EUR"}
                }
            },
        ]

    def test_filter_usd_transactions(self, transactions):
        """Тест фильтрации USD транзакций."""
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 2
        for transaction in result:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_rub_transactions(self, transactions):
        """Тест фильтрации RUB транзакций."""
        result = list(filter_by_currency(transactions, "RUB"))
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_no_matches(self, transactions):
        """Тест фильтрации без совпадений."""
        result = list(filter_by_currency(transactions, "GBP"))
        assert len(result) == 0

    def test_filter_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = list(filter_by_currency([], "USD"))
        assert len(result) == 0

    def test_filter_missing_operation_amount(self):
        """Тест фильтрации при отсутствии operationAmount."""
        transactions = [
            {"id": 1},
            {"id": 2, "operationAmount": {}},
            {"id": 3, "operationAmount": {"currency": {"code": "USD"}}}
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 3


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    @pytest.fixture
    def transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Перевод с карты на карту"},
        ]

    def test_descriptions_generation(self, transactions):
        """Тест генерации описаний."""
        descriptions = list(transaction_descriptions(transactions))
        assert len(descriptions) == 3
        assert descriptions[0] == "Перевод организации"
        assert descriptions[1] == "Перевод со счета на счет"
        assert descriptions[2] == "Перевод с карты на карту"

    def test_empty_list(self):
        """Тест с пустым списком."""
        descriptions = list(transaction_descriptions([]))
        assert len(descriptions) == 0

    def test_missing_description(self):
        """Тест при отсутствии поля description."""
        transactions = [
            {"id": 1},
            {"id": 2, "description": ""},
            {"id": 3, "description": "Есть описание"}
        ]
        descriptions = list(transaction_descriptions(transactions))
        assert len(descriptions) == 1
        assert descriptions[0] == "Есть описание"


class TestCardNumberGenerator:
    """Тесты для функции card_number_generator."""

    def test_generate_range(self):
        """Тест генерации диапазона номеров."""
        generator = card_number_generator(1, 5)
        result = list(generator)
        assert len(result) == 5
        assert result[0] == "0000 0000 0000 0001"
        assert result[1] == "0000 0000 0000 0002"
        assert result[2] == "0000 0000 0000 0003"
        assert result[3] == "0000 0000 0000 0004"
        assert result[4] == "0000 0000 0000 0005"

    def test_single_number(self):
        """Тест генерации одного номера."""
        generator = card_number_generator(1234, 1234)
        result = list(generator)
        assert len(result) == 1
        assert result[0] == "0000 0000 0000 1234"

    def test_invalid_range(self):
        """Тест с некорректным диапазоном (start > stop)."""
        generator = card_number_generator(10, 5)
        result = list(generator)
        assert len(result) == 0

    def test_large_numbers(self):
        """Тест с большими числами."""
        generator = card_number_generator(9999999999999995, 9999999999999999)
        result = list(generator)
        assert len(result) == 5
        assert result[0] == "9999 9999 9999 9995"
        assert result[-1] == "9999 9999 9999 9999"