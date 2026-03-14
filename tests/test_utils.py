"""
Тесты для модуля utils.
Проверяет корректность чтения файлов и обработки транзакций.
"""

import json
import os
import tempfile
import pytest
from unittest.mock import Mock, mock_open, patch

# Условный импорт pandas
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

from src.utils import (
    read_json_file,
    read_csv_file,
    read_excel_file,
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


class TestReadCsvFile:
    """Тесты для функции read_csv_file."""

    def test_read_valid_csv_file_with_semicolon(self, tmp_path):
        """
        Тест чтения корректного CSV-файла с разделителем ';'.
        """
        # Создаем временный CSV файл с разделителем ;
        csv_content = """id;amount;currency;description
    1;100.50;USD;Transaction 1
    2;200.75;EUR;Transaction 2"""

        csv_file = tmp_path / "test_semicolon.csv"
        csv_file.write_text(csv_content, encoding='utf-8')

        # Используем патч для замены pandas.read_csv на mock
        with patch('pandas.read_csv') as mock_read_csv:
            # Настраиваем mock для возврата DataFrame
            mock_df = Mock()
            mock_df.to_dict.return_value = [
                {"id": 1, "amount": 100.50, "currency": "USD", "description": "Transaction 1"},
                {"id": 2, "amount": 200.75, "currency": "EUR", "description": "Transaction 2"}
            ]
            mock_read_csv.return_value = mock_df

            result = read_csv_file(str(csv_file))

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100.50
        assert result[1]["currency"] == "EUR"

    @patch('pandas.read_csv')
    def test_read_csv_error(self, mock_read_csv):
        """
        Тест обработки ошибки при чтении CSV.
        """
        mock_read_csv.side_effect = Exception("CSV read error")

        result = read_csv_file("test.csv")

        assert result == []


class TestReadExcelFile:
    """Тесты для функции read_excel_file."""

    def test_read_valid_excel_file(self, tmp_path):
        """
        Тест чтения корректного Excel-файла.
        """
        if not PANDAS_AVAILABLE:
            pytest.skip("pandas не установлен, пропускаем тест Excel")

        # Создаем временный Excel файл
        df = pd.DataFrame({
            'id': [1, 2],
            'amount': [100.50, 200.75],
            'currency': ['USD', 'EUR'],
            'description': ['Transaction 1', 'Transaction 2']
        })

        excel_file = tmp_path / "test.xlsx"
        df.to_excel(excel_file, index=False)

        result = read_excel_file(str(excel_file))

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["currency"] == "EUR"

    @patch('pandas.read_excel')
    def test_read_excel_error(self, mock_read_excel):
        """
        Тест обработки ошибки при чтении Excel.
        """
        mock_read_excel.side_effect = Exception("Excel read error")

        result = read_excel_file("test.xlsx")

        assert result == []

    def test_read_excel_pandas_not_available(self):
        """
        Тест когда pandas не установлен.
        """
        # Создаем мок для pandas.read_excel, который выбрасывает исключение
        with patch('pandas.read_excel', side_effect=ImportError("No module named 'pandas'")):
            result = read_excel_file("test.xlsx")
            assert result == []


class TestTransactionAmount:
    """Тесты для функции get_transaction_amount."""

    def test_get_valid_amount(self, sample_transaction):
        """
        Тест извлечения корректной суммы из транзакции.
        """
        amount = get_transaction_amount(sample_transaction)

        assert amount == 31957.58
        assert isinstance(amount, float)

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
