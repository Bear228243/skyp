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
    def test_get_mask_card_number_valid(self, card_number: str, expected: str) -> None:
        """Тестирование корректных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("card_number", [
        "1234",  # слишком короткий
        "123456789012",  # 12 цифр
        "",  # пустая строка
        "abcd1234efgh5678",  # содержит буквы
        "1234-5678-9012-3456",  # содержит дефисы
        "1234 5678 9012 3456",  # содержит пробелы
    ])
    def test_get_mask_card_number_invalid(self, card_number: str) -> None:
        """Тестирование некорректных номеров карт"""
        result = get_mask_card_number(card_number)
        # Для некорректных данных должна возвращаться исходная строка
        assert result == card_number

    def test_get_mask_card_number_none_input(self) -> None:
        """Тестирование None входных данных"""
        result = get_mask_card_number(None)  # type: ignore
        assert result is None


class TestGetMaskAccount:
    """Тесты для функции get_mask_account"""

    @pytest.mark.parametrize("account_number, expected", [
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
    ])
    def test_get_mask_account_valid(self, account_number: str, expected: str) -> None:
        """Тестирование корректных номеров счетов"""
        result = get_mask_account(account_number)
        assert result == expected

    @pytest.mark.parametrize("account_number", [
        "1234",  # слишком короткий (но 4 цифры - минимальная длина для маскирования)
        "123",  # слишком короткий
        "",  # пустая строка
        "abc123",  # содержит буквы
        "12-34-56",  # содержит дефисы
        "123 456",  # содержит пробелы
    ])
    def test_get_mask_account_invalid(self, account_number: str) -> None:
        """Тестирование некорректных номеров счетов"""
        result = get_mask_account(account_number)
        # Для некорректных данных должна возвращаться исходная строка
        assert result == account_number

    def test_get_mask_account_edge_cases(self) -> None:
        """Тестирование граничных случаев"""
        # Минимальная допустимая длина (4 цифры)
        result = get_mask_account("1234")
        assert result == "**1234"  # Должно маскироваться

        # Номер короче 4 символов
        result = get_mask_account("123")
        assert result == "123"  # Не должен маскироваться