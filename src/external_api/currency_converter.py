"""
Модуль для конвертации валют через внешнее API.
Предоставляет функции для конвертации USD и EUR в рубли.
"""

import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class CurrencyConverter:
    """
    Класс для конвертации валют через Exchange Rates Data API.
    """

    def __init__(self) -> None:
        """
        Инициализирует конвертер валют с API ключом.
        """
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.base_url = "https://api.apilayer.com/exchangerates_data/latest"

    def get_exchange_rate(self, from_currency: str, to_currency: str = "RUB") -> float:
        """
        Получает текущий курс обмена валюты через API.

        Аргументы:
            from_currency: Исходная валюта (например, "USD", "EUR")
            to_currency: Целевая валюта (по умолчанию "RUB")

        Возвращает:
            Курс обмена валюты

        Исключения:
            ValueError: Если API ключ не установлен или произошла ошибка API
            requests.RequestException: Если произошла сетевая ошибка
        """
        if not self.api_key:
            raise ValueError("API ключ для Exchange Rates API не установлен. "
                             "Убедитесь, что переменная EXCHANGE_RATE_API_KEY установлена в .env файле.")

        headers = {
            "apikey": self.api_key
        }

        params = {
            "base": from_currency,
            "symbols": to_currency
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("success", True):
                error_info = data.get("error", {})
                raise ValueError(f"API ошибка: {error_info.get('info', 'Неизвестная ошибка')}")

            rates = data.get("rates", {})
            if to_currency not in rates:
                raise ValueError(f"Курс для валюты {to_currency} не найден в ответе API")

            return rates[to_currency]

        except requests.RequestException as e:
            raise requests.RequestException(f"Сетевая ошибка при запросе к API: {e}")

    def convert_to_rubles(self, transaction: Dict[str, Any]) -> float:
        """
        Конвертирует сумму транзакции в рубли.

        Аргументы:
            transaction: Словарь с данными о транзакции

        Возвращает:
            Сумму транзакции в рублях как float

        Исключения:
            KeyError: Если в транзакции отсутствуют необходимые ключи
            ValueError: Если сумма не может быть преобразована или произошла ошибка конвертации
        """
        from src.utils.file_operations import get_transaction_amount, get_transaction_currency

        try:
            amount = get_transaction_amount(transaction)
            currency = get_transaction_currency(transaction)

            # Если валюта уже рубли, возвращаем сумму как есть
            if currency == "RUB":
                return amount

            # Конвертируем USD и EUR в рубли
            if currency in ["USD", "EUR"]:
                exchange_rate = self.get_exchange_rate(currency, "RUB")
                return amount * exchange_rate

            # Для других валют возвращаем исходную сумму (или можно выбросить исключение)
            print(f"Внимание: валюта {currency} не поддерживается для конвертации. Возвращена исходная сумма.")
            return amount

        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при обработке транзакции: {e}")


# Создаем глобальный экземпляр конвертера для удобства использования
converter = CurrencyConverter()


def get_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Основная функция для получения суммы транзакции в рублях.

    Аргументы:
        transaction: Словарь с данными о транзакции

    Возвращает:
        Сумму транзакции в рублях как float

   """
    return converter.convert_to_rubles(transaction)