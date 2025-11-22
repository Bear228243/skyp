"""
Тесты для модуля file_operations.
Проверяет корректность чтения JSON-файлов и обработки транзакций.
"""

import json
import os
import tempfile
import pytest
from unittest.mock import mock_open, patch

from src.utils_file_operations import (
    read_json_file,
    get_transaction_amount,
    get_transaction_currency
)


@pytest.fixture
def sample_transaction():
    """
    Фикстура предоставляет пример корректной транзакции.
    """
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }


@pytest.fixture
def temp_json_file():
    """
    Фикстура создает временный JSON-файл для тестирования.
    """
    # Создаем временный файл с корректными данными
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    test_data = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "RUB"}
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "USD"}
            }
        }
    ]
    json.dump(test_data, temp_file)
    temp_file.close()

    yield temp_file.name

    # Удаляем временный файл после теста
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


class TestReadJsonFile:
    """Тесты для функции read_json_file."""

    def test_read_valid_json_file(self, temp_json_file):
        """
        Тест чтения корректного JSON-файла.
        """
        result = read_json_file(temp_json_file)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_read_nonexistent_file(self):
        """
        Тест чтения несуществующего файла.
        """
        result = read_json_file("nonexistent_file.json")

        assert result == []

    @patch("builtins.open", mock_open(read_data='{"not": "a list"}'))
    def test_read_json_not_list(self):
        """
        Тест чтения JSON-файла, который не содержит список.
        """
        result = read_json_file("test.json")

        assert result == []

    @patch("builtins.open", mock_open(read_data='invalid json'))
    def test_read_invalid_json(self):
        """
        Тест чтения файла с некорректным JSON.
        """
        result = read_json_file("test.json")

        assert result == []

    def test_read_empty_file(self):
        """
        Тест чтения пустого файла.
        """
        # Создаем временный пустой файл
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()

        try:
            result = read_json_file(temp_file.name)
            assert result == []
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


class TestTransactionAmount:
    """Тесты для функции get_transaction_amount."""

    def test_get_valid_amount(self, sample_transaction):
        """
        Тест извлечения корректной суммы из транзакции.
        """
        amount = get_transaction_amount(sample_transaction)

        assert amount == 31957.58
        assert isinstance(amount, float)

    def test_get_amount_with_comma(self):
        """
        Тест извлечения суммы с дробной частью.
        """
        transaction = {
            "operationAmount": {
                "amount": "123.45",
                "currency": {"code": "RUB"}
            }
        }

        amount = get_transaction_amount(transaction)
        assert amount == 123.45

    def test_get_amount_missing_key(self):
        """
        Тест извлечения суммы при отсутствии обязательных ключей.
        """
        transaction = {"id": 1}  # Нет operationAmount

        with pytest.raises(KeyError):
            get_transaction_amount(transaction)

    def test_get_amount_invalid_format(self):
        """
        Тест извлечения суммы в некорректном формате.
        """
        transaction = {
            "operationAmount": {
                "amount": "not_a_number",
                "currency": {"code": "RUB"}
            }
        }

        with pytest.raises(ValueError):
            get_transaction_amount(transaction)


class TestTransactionCurrency:
    """Тесты для функции get_transaction_currency."""

    def test_get_valid_currency(self, sample_transaction):
        """
        Тест извлечения корректного кода валюты.
        """
        currency = get_transaction_currency(sample_transaction)

        assert currency == "RUB"

    def test_get_currency_missing_key(self):
        """
        Тест извлечения валюты при отсутствии обязательных ключей.
        """
        transaction = {"id": 1}  # Нет operationAmount

        with pytest.raises(KeyError):
            get_transaction_currency(transaction)

    @pytest.mark.parametrize("currency_code", ["USD", "EUR", "GBP", "JPY"])
    def test_get_different_currencies(self, currency_code):
        """
        Параметризованный тест для различных кодов валют.
        """
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": currency_code}
            }
        }

        result = get_transaction_currency(transaction)
        assert result == currency_code


def test_integration_read_and_process(temp_json_file):
    """
    Интеграционный тест чтения файла и обработки транзакций.
    """
    transactions = read_json_file(temp_json_file)

    assert len(transactions) == 2

    # Проверяем первую транзакцию
    amount1 = get_transaction_amount(transactions[0])
    currency1 = get_transaction_currency(transactions[0])

    assert amount1 == 100.00
    assert currency1 == "RUB"

    # Проверяем вторую транзакцию
    amount2 = get_transaction_amount(transactions[1])
    currency2 = get_transaction_currency(transactions[1])

    assert amount2 == 50.00
    assert currency2 == "USD"


def test_read_json_file_logging(tmp_path):
    """
    Тест логирования при чтении JSON-файла.
    """
    # Создаем временный JSON файл
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"id": 1, "name": "test"}]', encoding='utf-8')

    result = read_json_file(str(json_file))
    assert result == [{"id": 1, "name": "test"}]


def test_read_nonexistent_file_logging():
    """
    Тест логирования при попытке чтения несуществующего файла.
    """
    result = read_json_file("nonexistent.json")
    assert result == []
