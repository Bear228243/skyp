"""
Дополнительные тесты для модуля utils.
Проверяет граничные случаи и обработку ошибок.
"""

import pytest
from unittest.mock import patch

from src.utils import (
    read_json_file,
    load_transactions_from_file,
    validate_transaction_structure,
    get_transaction_amount,
    get_transaction_currency
)


@pytest.fixture
def sample_transaction():
    """Фикстура предоставляет пример корректной транзакции."""
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


class TestUtilsAdditional:
    """Дополнительные тесты для функций utils."""

    @patch('src.utils.os.path.exists')
    def test_read_json_file_permission_error(self, mock_exists):
        """Тест ошибки доступа при чтении JSON."""
        mock_exists.return_value = True

        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = read_json_file("test.json")
            assert result == []

    @patch('src.utils.os.path.exists')
    def test_read_json_file_unexpected_error(self, mock_exists):
        """Тест неожиданной ошибки при чтении JSON."""
        mock_exists.return_value = True

        with patch('builtins.open', side_effect=MemoryError("Out of memory")):
            result = read_json_file("test.json")
            assert result == []

    def test_load_transactions_from_file_json_error(self):
        """Тест обработки ошибки при загрузке JSON."""
        with patch('src.utils.read_json_file', side_effect=Exception("JSON error")):
            result = load_transactions_from_file("test.json")
            assert result == []

    def test_load_transactions_from_file_csv_error(self):
        """Тест обработки ошибки при загрузке CSV."""
        with patch('src.utils.read_csv_file', side_effect=Exception("CSV error")):
            result = load_transactions_from_file("test.csv")
            assert result == []

    def test_load_transactions_from_file_excel_error(self):
        """Тест обработки ошибки при загрузке Excel."""
        with patch('src.utils.read_excel_file', side_effect=Exception("Excel error")):
            result = load_transactions_from_file("test.xlsx")
            assert result == []

    def test_load_transactions_from_file_unsupported(self):
        """Тест загрузки из неподдерживаемого формата."""
        result = load_transactions_from_file("test.txt")
        assert result == []

    def test_validate_transaction_structure_valid(self, sample_transaction):
        """Тест валидации корректной транзакции."""
        assert validate_transaction_structure(sample_transaction) is True

    def test_validate_transaction_structure_missing_id(self, sample_transaction):
        """Тест валидации транзакции без id."""
        transaction = sample_transaction.copy()
        del transaction["id"]
        assert validate_transaction_structure(transaction) is False

    def test_validate_transaction_structure_missing_operation_amount(self, sample_transaction):
        """Тест валидации транзакции без operationAmount."""
        transaction = sample_transaction.copy()
        del transaction["operationAmount"]
        assert validate_transaction_structure(transaction) is False

    def test_validate_transaction_structure_missing_amount(self, sample_transaction):
        """Тест валидации транзакции без amount."""
        transaction = sample_transaction.copy()
        del transaction["operationAmount"]["amount"]
        assert validate_transaction_structure(transaction) is False

    def test_validate_transaction_structure_missing_currency(self, sample_transaction):
        """Тест валидации транзакции без currency."""
        transaction = sample_transaction.copy()
        del transaction["operationAmount"]["currency"]
        assert validate_transaction_structure(transaction) is False

    def test_validate_transaction_structure_missing_code(self, sample_transaction):
        """Тест валидации транзакции без code."""
        transaction = sample_transaction.copy()
        del transaction["operationAmount"]["currency"]["code"]
        assert validate_transaction_structure(transaction) is False

    def test_validate_transaction_structure_with_string(self):
        """Тест валидации со строкой вместо словаря."""
        with patch('src.utils.logger') as mock_logger:
            result = validate_transaction_structure("not a dict")
            assert result is False
            mock_logger.error.assert_called()

    def test_get_transaction_amount_key_error_logging(self):
        """Тест логирования KeyError при получении суммы."""
        with patch('src.utils.logger') as mock_logger:
            transaction = {"id": 1}  # Нет operationAmount
            with pytest.raises(KeyError):
                get_transaction_amount(transaction)
            mock_logger.error.assert_called()

    def test_get_transaction_amount_value_error_logging(self):
        """Тест логирования ValueError при получении суммы."""
        with patch('src.utils.logger') as mock_logger:
            transaction = {
                "operationAmount": {
                    "amount": "not_a_number",
                    "currency": {"code": "RUB"}
                }
            }
            with pytest.raises(ValueError):
                get_transaction_amount(transaction)
            mock_logger.error.assert_called()

    def test_get_transaction_currency_key_error_logging(self):
        """Тест логирования KeyError при получении валюты."""
        with patch('src.utils.logger') as mock_logger:
            transaction = {"id": 1}  # Нет operationAmount
            with pytest.raises(KeyError):
                get_transaction_currency(transaction)
            mock_logger.error.assert_called()