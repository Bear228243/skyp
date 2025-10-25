def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 цифры"""
    if not card_number or len(card_number) < 16:
        return card_number

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета, оставляя последние 4 цифры"""
    if not account_number or len(account_number) < 4:
        return account_number

    return f"**{account_number[-4:]}"