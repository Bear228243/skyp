import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number"""

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("6831982476737658", "6831 98** **** 7658"),
        ("1234567812345678", "1234 56** **** 5678"),
    ])
    def test_get_mask_card_number_valid(self, card_number: str, expected: str) -> None:
        """Тестирование корректных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("card_number", [
        "1234",  # слишком короткий
        "123456789012",  # 12 цифр
        "",  # пустая строка
        "abcd1234efgh5678",  # содержит буквы
    ])
    def test_get_mask_card_number_invalid(self, card_number: str) -> None:
        """Тестирование некорректных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == card_number


class TestGetMaskAccount:
    """Тесты для функции get_mask_account"""

    @pytest.mark.parametrize("account_number, expected", [
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
    ])
    def test_get_mask_account_valid(self, account_number: str, expected: str) -> None:
        """Тестирование корректных номеров счетов"""
        result = get_mask_account(account_number)
        assert result == expected

    @pytest.mark.parametrize("account_number", [
        "123",  # слишком короткий
        "",  # пустая строка
        "abc123",  # содержит буквы
    ])
    def test_get_mask_account_invalid(self, account_number: str) -> None:
        """Тестирование некорректных номеров счетов"""
        result = get_mask_account(account_number)
        assert result == account_number

    def test_get_mask_account_minimum_length(self) -> None:
        """Тестирование минимальной длины номера счета"""
        result = get_mask_account("1234")
        assert result == "**1234"