import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected",
    [
        (7000792289606361, "7000 79** **** 6361"),
        (1234567890123456, "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number_valid(card_number, expected):
    """Проверяет корректное маскирование номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("invalid_card", [123, 111111111111111, 12345678901234567])
def test_get_mask_card_number_invalid_length(invalid_card):
    """Проверяет, что ошибка вызывается при неверной длине номера карты."""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        (73654108430135874305, "**4305"),
        (12345678, "**5678"),
    ],
)
def test_get_mask_account_valid(account_number, expected):
    """Проверяет корректное маскирование банковского счёта."""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("invalid_account", [1, 12, 123])
def test_get_mask_account_invalid_length(invalid_account):
    """Проверяет обработку слишком коротких номеров счетов."""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)
