"""
Модуль для работы с файлами операций над банковскими картами.
Предоставляет функции для чтения Json-файлов с транзакциями.
"""

import json
import os
from typing import Any, Dict, List

from src.logging_config import get_utils_logger

#Create loger for module utils
logger = get_utils_logger()

def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Json-файл и возвращает список словарей с данными о транзакциях.

    :param
        file_path: Путь к JSON-файлу
    :return:
        Список словарей с данными о транзакциях.
        Если файл не найден, пустой или содержит не список, то возвращает пустой список.
    """
    logger.info(f"Попытка чтения JSON-файла:{file_path}")

    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        error_msg = f"Файл {file_path} не найден"
        logger.error(error_msg)
        return []

    try:
        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            error_msg = f"Файл {file_path} не является списком"
            logger.error(error_msg)
            return []

        logger.info(f"Успешное чтение JSON-файла:{file_path}. Заргужено {len(data)} записей.")
        return data

    except json.JSONDecodeError as e:
        error_msg = f"Ошибка декодирования JSON в файле {file_path}: {e}"
        logger.error(error_msg)
        return []
    except Exception as e:
        error_msg = "Неожиданная ошибка при чтении файла {file_path}: {e}"
        logger.error(error_msg)
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
    logger.info(f"Извлечение суммы из транзакции: {transaction.get('id', 'Unknown')}")

    try:
        # Получаем сумму из operationAmount -> amount
        amount_str = transaction["operationAmount"]["amount"]
        return float(amount_str)

        logger.debug(f"Успешное извлечение суммы: {amount} из транзакции {transaction.get('id', 'Unknown')}")
        return amount

    except KeyError as e:
        error_msg = f"Отсутствует обязательный ключ в транзакции: {e}"
        logger.error(error_msg)
        raise KeyError(error_msg)
    except (ValueError, TypeError) as e:
        amount_str = transaction.get("operationAmount", {}).get("amount", "Unknown")
        error_msg = f"Невозможно преобразовать сумму {amount_str} в float: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg)


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
    logger.debug(f"Извлечение валюты из транзакции: {transaction.get('id', 'Unknown')}")

    try:
        currency = transaction["operationAmount"]["currency"]["code"]
        logger.debug(f"Успешное извлечение валюты: {currency} из транзакции {transaction.get('id', 'Unknown')}")
        return currency

    except KeyError as e:
        error_msg = f"Отсутствует обязательный ключ валюты в транзакции: {e}"
        logger.error(error_msg)
        raise KeyError(error_msg)


def validate_transaction_structure(transaction: Dict[str, Any]) -> bool:
    """
    Проверяет структуру транзакции на наличие обязательных полей.

    Аргументы:
        transaction: Словарь с данными о транзакции

    Возвращает:
        True если структура корректна, иначе False
    """
    logger.debug(f"Валидация структуры транзакции: {transaction.get('id', 'Unknown')}")

    required_fields = ["id", "operationAmount"]
    operation_amount_fields = ["amount", "currency"]
    currency_fields = ["code"]

    try:
        # Проверяем основные поля
        for field in required_fields:
            if field not in transaction:
                logger.warning(f"Отсутствует обязательное поле '{field}' в транзакции")
                return False

        # Проверяем поля operationAmount
        operation_amount = transaction["operationAmount"]
        for field in operation_amount_fields:
            if field not in operation_amount:
                logger.warning(f"Отсутствует поле '{field}' в operationAmount транзакции {transaction['id']}")
                return False

        # Проверяем поля currency
        currency = operation_amount["currency"]
        for field in currency_fields:
            if field not in currency:
                logger.warning(f"Отсутствует поле '{field}' в currency транзакции {transaction['id']}")
                return False

        logger.debug(f"Структура транзакции {transaction['id']} прошла валидацию")
        return True

    except Exception as e:
        error_msg = f"Ошибка при валидации структуры транзакции: {e}"
        logger.error(error_msg)
        return False