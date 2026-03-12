"""
Модуль с функциями-генераторами для работы с транзакциями.
"""

from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по валюте.

    Args:
        transactions: Список транзакций
        currency: Код валюты для фильтрации

    Yields:
        Транзакции с указанной валютой
    """
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except (KeyError, AttributeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Возвращает описания транзакций.

    Args:
        transactions: Список транзакций

    Yields:
        Описания транзакций
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генерирует номера карт в заданном диапазоне.

    Args:
        start: Начальное число
        stop: Конечное число

    Yields:
        Номера карт в формате XXXX XXXX XXXX XXXX
    """
    for number in range(start, stop + 1):
        # Форматируем номер карты: 16 цифр с пробелами каждые 4 цифры
        num_str = str(number).zfill(16)
        formatted = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        yield formatted
