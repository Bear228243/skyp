"""
Модуль для конвертации валют через внешнее API.
Предоставляет функции для конвертации USD и EUR в рубли.
"""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

from .logging_config import get_external_api_logger

# Загружаем переменные окружения из .env файла
load_dotenv()

logger = get_external_api_logger()


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

        if not self.api_key:
            logger.warning("API ключ для Exchange Rates API не установлен в переменных окружения")
        else:
            logger.debug("CurrencyConverter инициализирован с API ключом")

    def get_exchange_rate(self, from_currency: str, to_currency: str = "RUB") -> float:
        """
        Получает текущий курс обмена валюты через API.

        Args:
            from_currency: Исходная валюта (например, "USD", "EUR")
            to_currency: Целевая валюта (по умолчанию "RUB")

        Returns:
            Курс обмена валюты

        Raises:
            ValueError: Если API ключ не установлен или произошла ошибка API
            requests.RequestException: Если произошла сетевая ошибка
        """
        if not self.api_key:
            error_msg = "API ключ для Exchange Rates API не установлен."
            logger.error(error_msg)
            raise ValueError(error_msg)

        headers = {
            "apikey": self.api_key
        }

        params = {
            "base": from_currency,
            "symbols": to_currency
        }

        try:
            logger.debug(f"Отправка запроса к API: {self.base_url}")
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"Получаем ответ от API: {data}")

            if not data.get("success", True):
                error_info = data.get("error", {})
                error_msg = f"API ошибка: {error_info.get('info', 'Неизвестная ошибка')}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            rates = data.get("rates", {})
            if to_currency not in rates:
                error_msg = f"Курс для валюты {to_currency} не найден в ответе API"
                logger.error(error_msg)
                raise ValueError(error_msg)

            rate = rates[to_currency]
            logger.info(f"Успешно получен курс обмена: {from_currency} -> {to_currency} = {rate}")
            return rate

        except requests.RequestException as e:
            error_msg = f"Сетевая ошибка при запросе к API: {e}"
            logger.error(error_msg)
            raise requests.RequestException(error_msg)
        except Exception as e:
            error_msg = f"Неожиданная ошибка при получении курса обмена: {e}"
            logger.error(error_msg)
            raise

    def convert_to_rubles(self, transaction: Dict[str, Any]) -> float:
        """
        Конвертирует сумму транзакции в рубли.

        Args:
            transaction: Словарь с данными о транзакции

        Returns:
            Сумму транзакции в рублях как float

        Raises:
            KeyError: Если в транзакции отсутствуют необходимые ключи
            ValueError: Если сумма не может быть преобразована или произошла ошибка конвертации
        """
        from .utils import get_transaction_amount, get_transaction_currency

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

            # Для других валют возвращаем исходную сумму
            logger.warning(
                f"Валюта {currency} не поддерживается для конвертации. Возвращена исходная сумма.")
            return amount

        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при обработке транзакции: {e}")


# Создаем глобальный экземпляр конвертера для удобства использования
converter = CurrencyConverter()


def get_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Основная функция для получения суммы транзакции в рублях.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумму транзакции в рублях как float

    Raises:
        ValueError: Если произошла ошибка при обработке транзакции
    """
    logger.debug(f"Конвертация суммы транзакции в рубли: {transaction.get('id', 'Unknown')}")

    from .utils import get_transaction_amount, get_transaction_currency

    try:
        amount = get_transaction_amount(transaction)
        currency = get_transaction_currency(transaction)

        logger.debug(f"Транзакция {transaction.get('id', 'Unknown')}: сумма={amount}, валюта={currency}")

        # Если валюта уже рубли, возвращаем сумму как есть
        if currency == "RUB":
            logger.debug("Транзакция уже в рублях, конвертация не требуется")
            return amount

        # Конвертируем USD и EUR в рубли
        if currency in ["USD", "EUR"]:
            logger.info(f"Конвертация {currency} в RUB для транзакции {transaction.get('id', 'Unknown')}")
            exchange_rate = converter.get_exchange_rate(currency, "RUB")
            result = amount * exchange_rate
            logger.info(f"Успешная конвертация: {amount} {currency} = {result} RUB")
            return result

        # Для других валют возвращаем исходную сумму
        logger.warning(f"Валюта {currency} не поддерживается для конвертации. Возвращена исходная сумма")
        return amount

    except (KeyError, ValueError) as e:
        error_msg = f"Ошибка при обработке транзакции {transaction.get('id', 'Unknown')}: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg)
