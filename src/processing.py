from typing import List, Dict, Any

def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по значению ключа 'state'.

    :param operations: Список словарей с операциями.
    :param state: Желаемое состояние операции (по умолчанию 'EXECUTED').
    :return: Новый список операций с заданным состоянием.
    """
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате (ключ 'date').

    :param operations: Список словарей с операциями.
    :param reverse: Порядок сортировки (True — по убыванию, False — по возрастанию).
    :return: Новый отсортированный список операций.
    """
    return sorted(operations, key=lambda x: x['date'], reverse=reverse)