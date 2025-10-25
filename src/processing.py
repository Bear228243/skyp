from typing import List, Dict, Any, Optional


def filter_by_state(transactions: list, state: str = "EXECUTED") -> list:
    """Фильтрует транзакции по статусу (нечувствительно к регистру)"""
    state_upper = state.upper()
    return [transaction for transaction in transactions
            if transaction.get("state", "").upper() == state_upper]

def sort_by_date(transactions: list, descending: bool = True) -> list:
    """Сортирует транзакции по дате"""
    if not transactions:
        return []

    def get_date_key(transaction: dict) -> str:
        date = transaction.get("date")
        # Заменяем None на минимальную дату для сортировки
        return date if date else "0000-00-00T00:00:00.000"

    return sorted(transactions, key=get_date_key, reverse=descending)