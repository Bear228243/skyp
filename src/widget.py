"""Модуль для обработки и форматирования данных транзакций."""

from .masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str:
    """
    Определяет тип данных (карта или счет) и применяет соответствующую маскировку.

    Args:
        data: Строка с информацией о карте/счете

    Returns:
        Замаскированная строка
    """
    if not data:
        return data

    # Проверяем на счет (учитываем разные регистры)
    if "счет" in data.lower():
        parts = data.split()
        if len(parts) >= 2:
            account_number = parts[-1]
            if account_number.isdigit() and len(account_number) >= 4:
                masked_account = get_mask_account(account_number)
                return f"{' '.join(parts[:-1])} {masked_account}"

    # Проверяем на карту (ищем 16 цифр подряд)
    words = data.split()
    for word in words:
        if word.isdigit() and len(word) == 16:
            masked_card = get_mask_card_number(word)
            return data.replace(word, masked_card)

    return data


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат DD.MM.YYYY.

    Args:
        date_string: Дата в формате ISO (например, "2024-03-14T10:30:00.000")

    Returns:
        Дата в формате "DD.MM.YYYY" или исходная строка при ошибке
    """
    if not date_string or "T" not in date_string:
        return date_string

    try:
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except (ValueError, IndexError):
        return date_string


def format_transaction(transaction: dict) -> str:
    """
    Форматирует информацию о транзакции в читаемый вид.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Отформатированная строка
    """
    if not transaction:
        return ""

    result = []

    # Дата
    date = get_date(transaction.get("date", ""))
    if date:
        result.append(date)

    # Описание
    description = transaction.get("description", "")
    if description:
        result.append(description)

    # Отправитель
    from_account = transaction.get("from", "")
    if from_account:
        result.append(f"{mask_account_card(from_account)} ->")

    # Получатель
    to_account = transaction.get("to", "")
    if to_account:
        result.append(mask_account_card(to_account))

    # Сумма
    operation_amount = transaction.get("operationAmount", {})
    amount = operation_amount.get("amount", "")
    currency = operation_amount.get("currency", {}).get("name", "")
    if amount and currency:
        result.append(f"{amount} {currency}")

    return " ".join(result)