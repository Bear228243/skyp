from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу"""
    if not transactions:
        return []

    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате"""
    if not transactions:
        return []

    def get_date_key(transaction: Dict[str, Any]) -> str:
        return transaction.get("date", "")

    return sorted(transactions, key=get_date_key, reverse=descending)