from .masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str:
    """Определяет тип данных (карта или счет) и применяет соответствующую маску"""
    if not data:
        return data

    # Проверяем на счет
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
    """Преобразует дату из формата ISO в формат DD.MM.YYYY"""
    if not date_string or "T" not in date_string:
        return date_string

    try:
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except (ValueError, IndexError):
        return date_string
