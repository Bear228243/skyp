"""
Модуль для работы с файйлами операций над банковскими картами.
Предоставляет функции для чтения Json-файлов с транзакциями.
"""

import json
import os
from typing import Any, Dict, List

def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Json-файл и возвращает список словарей с данными о транзакциях.

    :param
        file_path: Путь к Json-файлу
    :return:
        Список словарей с данными о транзакциях.
        Если файл не найден, пустой или содержит не список, то возвращает пустой список.
    """
    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return []

    try:
        # Открываем и читаем файл
        with open(file_path, 'r', encodings='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            print(f"Файл {file_path} не является списком")
            return []

        return data

    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []

def get_transaction_amount(transaction: Dict[str, Any]) -> float:
    """
    Извлекает сумму транзакции из словаря транзакций.

    :param
        transaction: Словарь с данными о транзакциях.
    :return:
        Сумму транзакций как float
    :exceptions:
        ValueError: Если сумма не может быть преобразована в float.
        KeyError: Если в транзакции отсутствует необходимые данные.
    """
    try:
        # Получаем сумму из operationAmount -> amount
        amount_str = transaction["operationAmount"]["amount"]
        return float(amount_str)
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательный ключ в транзакции: {e}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Невозможно преобразовать сумму {amount_str} в float: {e}")

def get_transaction_currency(transaction: Dict[str, Any]) -> str:
    """
    Извлекает код валюты транзакции.

    Аргументы:
        transaction: Словарь с данными о транзакции

    Возвращает:
        Код валюты транзакции (например, "RUB", "USD", "EUR")

    Исключения:
        KeyError: Если в транзакции отсутствуют необходимые ключи
    """
    try:
        return transaction["operationAmount"]["currency"]["code"]
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательный ключ валюты в транзакции: {e}")
