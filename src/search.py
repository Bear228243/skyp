"""
Модуль для поиска и анализа банковских операций с использованием регулярных выражений.
"""

import re
from collections import Counter
from typing import List, Dict, Any
from .logging_config import get_utils_logger

logger = get_utils_logger()


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых содержится заданная строка.

    Использует регулярные выражения для поиска (регистронезависимый поиск).
    Ищет вхождение строки как отдельного слова или части слова.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска в описании

    Returns:
        Список транзакций, у которых в описании есть искомая строка
    """
    if not transactions or not search_string:
        logger.debug("Пустой список транзакций или строка поиска")
        return []

    try:
        # Создаем регулярное выражение с флагом регистронезависимости
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)

        result = []
        for transaction in transactions:
            description = transaction.get("description", "")
            if description and pattern.search(description):
                result.append(transaction)

        logger.info(f"Найдено {len(result)} транзакций по запросу '{search_string}'")
        return result

    except Exception as e:
        logger.error(f"Ошибка при поиске транзакций: {e}")
        return []


def count_transactions_by_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций в каждой категории.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством транзакций в каждой категории
    """
    if not transactions or not categories:
        logger.debug("Пустой список транзакций или категорий")
        return {category: 0 for category in categories}

    try:
        # Создаем счетчик
        counter = Counter()

        for transaction in transactions:
            description = transaction.get("description", "")
            if not description:
                continue

            for category in categories:
                if re.search(re.escape(category), description, re.IGNORECASE):
                    counter[category] += 1

        result = {category: counter.get(category, 0) for category in categories}

        logger.info(f"Подсчитаны категории: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при подсчете категорий: {e}")
        return {category: 0 for category in categories}


def advanced_search_transactions(transactions: List[Dict[str, Any]], pattern: str) -> List[Dict[str, Any]]:
    """
    Расширенный поиск транзакций с использованием регулярных выражений.

    Позволяет использовать сложные шаблоны регулярных выражений.

    Args:
        transactions: Список словарей с транзакциями
        pattern: Регулярное выражение для поиска

    Returns:
        Список транзакций, соответствующих шаблону
    """
    if not transactions or not pattern:
        return []

    try:
        regex = re.compile(pattern, re.IGNORECASE)

        result = []
        for transaction in transactions:
            description = transaction.get("description", "")
            if description and regex.search(description):
                result.append(transaction)

        logger.info(f"Расширенный поиск по шаблону '{pattern}' нашел {len(result)} транзакций")
        return result

    except re.error as e:
        logger.error(f"Ошибка в регулярном выражении '{pattern}': {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при расширенном поиске: {e}")
        return []
