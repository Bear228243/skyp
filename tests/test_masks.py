import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number"""

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("6831982476737658", "6831 98** **** 7658"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ])
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Тестирование корректных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == expected
        assert len(result.replace(" ", "")) == len(card_number)

    @pytest.mark.parametrize("card_number", [
        "1234",
        "123456789012",  # 12 цифр
        "12345678901234567890",  # 20 цифр
        "",
        "abcd1234efgh5678",  # буквы
        "1234-5678-9012-3456",  # с дефисами
    ])
    def test_get_mask_card_number_invalid(self, card_number):
        """Тестирование некорректных номеров карт"""
        result = get_mask_card_number(card_number)
        # Функция должна обрабатывать некорректные данные без падения
        assert isinstance(result, str)

    def test_get_mask_card_number_short(self):
        """Тестирование короткого номера карты"""
        result = get_mask_card_number("12345678")
        assert result == "1234 56** **** 5678"


class TestGetMaskAccount:
    """Тесты для функции get_mask_account"""

    @pytest.mark.parametrize("account_number, expected", [
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
    ])
    def test_get_mask_account_valid(self, account_number, expected):
        """Тестирование корректных номеров счетов"""
        result = get_mask_account(account_number)
        assert result == expected
        assert result.startswith("**")

    @pytest.mark.parametrize("account_number", [
        "1234",  # слишком короткий
        "",  # пустая строка
        "abc123def456",  # буквы
        "1234 5678 9012 3456",  # с пробелами
    ])
    def test_get_mask_account_invalid(self, account_number):
        """Тестирование некорректных номеров счетов"""
        result = get_mask_account(account_number)
        assert isinstance(result, str)

    def test_get_mask_account_edge_cases(self):
        """Тестирование граничных случаев"""
        # Минимальная допустимая длина
        result = get_mask_account("123456")
        assert result == "**3456"

        # Номер короче 4 символов
        result = get_mask_account("123")
        assert len(result) >= 2