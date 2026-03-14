"""
Тесты для модуля external_api.
Проверяет корректность конвертации валют через внешнее API.
"""

import os
from unittest.mock import Mock, patch

import pytest

from src.external_api import CurrencyConverter, get_amount_in_rubles


@pytest.fixture
def sample_rub_transaction():
    """
    Фикстура предоставляет транзакцию в рублях.
    """
    return {
        "id": 1,
        "operationAmount": {
            "amount": "1000.00",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    }


@pytest.fixture
def sample_usd_transaction():
    """
    Фикстура предоставляет транзакцию в долларах.
    """
    return {
        "id": 2,
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }


@pytest.fixture
def sample_eur_transaction():
    """
    Фикстура предоставляет транзакцию в евро.
    """
    return {
        "id": 3,
        "operationAmount": {
            "amount": "50.00",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        }
    }


@pytest.fixture
def converter():
    """
    Фикстура предоставляет экземпляр CurrencyConverter.
    """
    return CurrencyConverter()


class TestCurrencyConverter:
    """Тесты для класса CurrencyConverter."""

    @patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_api_key"})
    def test_init_with_api_key(self):
        """
        Тест инициализации конвертера с API ключом.
        """
        converter = CurrencyConverter()
        assert converter.api_key == "test_api_key"

    def test_init_without_api_key(self):
        """
        Тест инициализации конвертера без API ключа.
        """
        # Временно удаляем переменную окружения, если она есть
        with patch.dict(os.environ, {}, clear=True):
            converter = CurrencyConverter()
            assert converter.api_key is None

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_success(self, mock_get, converter):
        """
        Тест успешного получения курса обмена.
        """
        # Мокаем успешный ответ API
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {
                "RUB": 75.50
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Устанавливаем API ключ для теста
        converter.api_key = "test_key"

        rate = converter.get_exchange_rate("USD", "RUB")

        assert rate == 75.50
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_api_error(self, mock_get, converter):
        """
        Тест обработки ошибки API.
        """
        # Мокаем ответ с ошибкой API
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": False,
            "error": {
                "info": "Invalid API key"
            }
        }
        mock_get.return_value = mock_response

        converter.api_key = "test_key"

        with pytest.raises(ValueError, match="API ошибка"):
            converter.get_exchange_rate("USD", "RUB")

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_network_error(self, mock_get, converter):
        """
        Тест обработки сетевой ошибки.
        """
        # Мокаем сетевую ошибку
        mock_get.side_effect = Exception("Network error")

        converter.api_key = "test_key"

        with pytest.raises(Exception, match="Network error"):
            converter.get_exchange_rate("USD", "RUB")

    def test_get_exchange_rate_no_api_key(self, converter):
        """
        Тест попытки получения курса без API ключа.
        """
        converter.api_key = None

        with pytest.raises(ValueError, match="API ключ для Exchange Rates API не установлен"):
            converter.get_exchange_rate("USD", "RUB")


class TestConvertToRubles:
    """Тесты для функции convert_to_rubles."""

    def test_convert_rub_transaction(self, converter, sample_rub_transaction):
        """
        Тест конвертации транзакции в рублях (без конвертации).
        """
        # Для рублевой транзакции конвертация не требуется
        result = converter.convert_to_rubles(sample_rub_transaction)

        assert result == 1000.00
        assert isinstance(result, float)

    @patch.object(CurrencyConverter, 'get_exchange_rate')
    def test_convert_usd_transaction(self, mock_get_rate, converter, sample_usd_transaction):
        """
        Тест конвертации транзакции в долларах.
        """
        # Мокаем курс доллара
        mock_get_rate.return_value = 75.50

        result = converter.convert_to_rubles(sample_usd_transaction)

        expected = 100.00 * 75.50  # 100 USD * 75.50 RUB/USD
        assert result == expected
        mock_get_rate.assert_called_once_with("USD", "RUB")

    @patch.object(CurrencyConverter, 'get_exchange_rate')
    def test_convert_eur_transaction(self, mock_get_rate, converter, sample_eur_transaction):
        """
        Тест конвертации транзакции в евро.
        """
        # Мокаем курс евро
        mock_get_rate.return_value = 85.25

        result = converter.convert_to_rubles(sample_eur_transaction)

        expected = 50.00 * 85.25  # 50 EUR * 85.25 RUB/EUR
        assert result == expected
        mock_get_rate.assert_called_once_with("EUR", "RUB")

    def test_convert_invalid_transaction(self, converter):
        """
        Тест конвертации некорректной транзакции.
        """
        invalid_transaction = {"id": 1}  # Нет данных о сумме и валюте

        with pytest.raises(ValueError, match="Ошибка при обработке транзакции"):
            converter.convert_to_rubles(invalid_transaction)


class TestGetAmountInRubles:
    """Тесты для основной функции get_amount_in_rubles."""

    def test_get_amount_rub(self, sample_rub_transaction):
        """
        Тест получения суммы в рублях для рублевой транзакции.
        """
        amount = get_amount_in_rubles(sample_rub_transaction)

        assert amount == 1000.00

    @patch.object(CurrencyConverter, 'get_exchange_rate')
    def test_get_amount_usd(self, mock_get_rate, sample_usd_transaction):
        """
        Тест получения суммы в рублях для долларовой транзакции.
        """
        mock_get_rate.return_value = 76.80

        amount = get_amount_in_rubles(sample_usd_transaction)

        expected = 100.00 * 76.80
        assert amount == expected

    @pytest.mark.parametrize("amount,currency,expected_rate,expected_result", [
        ("100.00", "RUB", None, 100.00),  # RUB - без конвертации
        ("50.00", "USD", 75.50, 3775.00),  # USD - с конвертацией
        ("25.00", "EUR", 85.25, 2131.25),  # EUR - с конвертацией
    ])
    @patch.object(CurrencyConverter, 'get_exchange_rate')
    def test_parametrized_conversion(self, mock_get_rate, amount, currency, expected_rate, expected_result):
        """
        Параметризованный тест конвертации различных валют.
        """
        if expected_rate:
            mock_get_rate.return_value = expected_rate

        transaction = {
            "operationAmount": {
                "amount": amount,
                "currency": {"code": currency}
            }
        }

        result = get_amount_in_rubles(transaction)
        assert result == expected_result
