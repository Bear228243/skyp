"""Модуль для обработки и фильтрации транзакций."""

from typing import List, Dict, Any
from datetime import datetime


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Args:
        transactions: Список транзакций
        state: Статус для фильтрации (по умолчанию "EXECUTED")

    Returns:
        Отфильтрованный список транзакций
    """
    if not transactions:
        return []

    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions: Список транзакций
        descending: Сортировка по убыванию (по умолчанию True)

    Returns:
        Отсортированный список транзакций
    """
    if not transactions:
        return []

    def get_date_key(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get("date", "")
        try:
            # Убираем временную зону если есть
            date_str = date_str.split('.')[0] if '.' in date_str else date_str
            return datetime.fromisoformat(date_str.replace('Z', ''))
        except (ValueError, AttributeError):
            return datetime.min

    return sorted(transactions, key=get_date_key, reverse=descending)


def get_last_transactions(transactions: List[Dict[str, Any]], count: int = 5) -> List[Dict[str, Any]]:
    """
    Возвращает последние выполненные транзакции.

    Args:
        transactions: Список всех транзакций
        count: Количество возвращаемых транзакций

    Returns:
        Список последних выполненных транзакций
    """
    executed_transactions = filter_by_state(transactions, "EXECUTED")
    sorted_transactions = sort_by_date(executed_transactions, descending=True)
    return sorted_transactions[:count]


def filter_by_currency_code(transactions: List[Dict[str, Any]], currency_code: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты.

    Args:
        transactions: Список транзакций
        currency_code: Код валюты (например, "USD", "RUB")

    Returns:
        Отфильтрованный список транзакций
    """
    if not transactions:
        return []

    filtered = []
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            filtered.append(transaction)

    return filtered