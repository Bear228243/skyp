"""Модуль с генераторами для работы с транзакциями."""

from typing import Dict, Iterator, List, Generator


def filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]:
    """
    Фильтрует транзакции по коду валюты.

    Функция-генератор, которая проходит по списку транзакций и возвращает
    только те транзакции, валюта которых соответствует заданной.

    Args:
        transactions: Список словарей с транзакциями
        currency_code: Код валюты для фильтрации (например, "USD", "RUB")

    Yields:
        Транзакции с указанной валютой
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генерирует описания транзакций.

    Функция-генератор, которая извлекает описание из каждой транзакции
    и возвращает их по одному.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описания транзакций
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует отформатированные номера банковских карт в заданном диапазоне.

    Генератор создает номера карт в формате XXXX XXXX XXXX XXXX,
    где X - цифра номера карты. Номера генерируются от start до stop включительно.

    Args:
        start: Начальный номер (включительно)
        stop: Конечный номер (включительно)

    Yields:
        Отформатированные номера карт
    """
    for number in range(start, stop + 1):
        card_number = str(number).zfill(16)
        formatted_number = " ".join([
            card_number[i:i + 4] for i in range(0, 16, 4)
        ])
        yield formatted_number


def card_number_range_generator(start: str, end: str) -> Iterator[str]:
    """
    Генерирует номера карт в заданном диапазоне.

    Args:
        start: Начальный номер в формате "XXXX XXXX XXXX XXXX"
        end: Конечный номер в формате "XXXX XXXX XXXX XXXX"

    Yields:
        Номера карт в заданном диапазоне
    """
    # Убираем пробелы для вычислений
    start_num = int(start.replace(" ", ""))
    end_num = int(end.replace(" ", ""))

    for number in range(start_num, end_num + 1):
        card_number = str(number).zfill(16)
        yield " ".join([card_number[i:i + 4] for i in range(0, 16, 4)])