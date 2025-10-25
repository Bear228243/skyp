import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для функции mask_account_card"""

    @pytest.mark.parametrize("input_string, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Maestro 6831982476737658", "Maestro 6831 98** **** 7658"),
    ])
    def test_mask_account_card_valid(self, input_string: str, expected: str) -> None:
        """Тестирование корректных входных данных"""
        result = mask_account_card(input_string)
        assert result == expected

    @pytest.mark.parametrize("input_string", [
        "Invalid String",
        "",
        "1234567890123456",  # только номер без типа
    ])
    def test_mask_account_card_invalid(self, input_string: str) -> None:
        """Тестирование некорректных входных данных"""
        result = mask_account_card(input_string)
        assert isinstance(result, str)


class TestGetDate:
    """Тесты для функции get_date"""

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-14T10:30:00.000", "14.03.2024"),
        ("2023-12-01T15:45:30.123", "01.12.2023"),
        ("2022-08-20T08:00:00.000", "20.08.2022"),
    ])
    def test_get_date_valid(self, input_date: str, expected: str) -> None:
        """Тестирование корректных дат"""
        result = get_date(input_date)
        assert result == expected

    @pytest.mark.parametrize("invalid_date", [
        "invalid_date_string",
        "",
        "2024-03-14",  # без времени
    ])
    def test_get_date_invalid(self, invalid_date: str) -> None:
        """Тестирование некорректных дат"""
        result = get_date(invalid_date)
        assert result == invalid_date