import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для функции mask_account_card"""

    @pytest.mark.parametrize("input_string, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Maestro 6831982476737658", "Maestro 6831 98** **** 7658"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ])
    def test_mask_account_card_valid(self, input_string: str, expected: str) -> None:
        """Тестирование корректных входных данных"""
        result = mask_account_card(input_string)
        assert result == expected

    @pytest.mark.parametrize("input_string", [
        "Invalid String",
        "",
        "1234567890123456",  # только номер без типа
        "Карта 1234abcd5678efgh",  # некорректный номер
        "Account 1234567890",  # неизвестный тип
    ])
    def test_mask_account_card_invalid(self, input_string: str) -> None:
        """Тестирование некорректных входных данных"""
        result = mask_account_card(input_string)
        assert isinstance(result, str)

    def test_mask_account_card_edge_cases(self) -> None:
        """Тестирование граничных случаев"""
        # Пробелы в начале/конце
        result = mask_account_card("  Visa 7000792289606361  ")
        assert "7000 79** **** 6361" in result

        # Разный регистр
        result = mask_account_card("счет 64686473678894779589")
        assert "**9589" in result

        # None input
        result = mask_account_card(None)  # type: ignore
        assert result is None


class TestGetDate:
    """Тесты для функции get_date"""

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-14T10:30:00.000", "14.03.2024"),
        ("2023-12-01T15:45:30.123", "01.12.2023"),
        ("2022-08-20T08:00:00.000", "20.08.2022"),
        ("2020-01-01T00:00:00.000", "01.01.2020"),
    ])
    def test_get_date_valid(self, input_date: str, expected: str) -> None:
        """Тестирование корректных дат"""
        result = get_date(input_date)
        assert result == expected
        assert len(result) == 10  # DD.MM.YYYY
        assert result.count(".") == 2

    @pytest.mark.parametrize("invalid_date, expected", [
        ("invalid_date_string", "invalid_date_string"),
        ("", ""),
        ("2024/03/14 10:30:00", "2024/03/14 10:30:00"),
        ("14.03.2024", "14.03.2024"),  # уже в нужном формате
        ("2024-03-14", "2024-03-14"),  # без времени
    ])
    def test_get_date_invalid(self, invalid_date: str, expected: str) -> None:
        """Тестирование некорректных дат"""
        result = get_date(invalid_date)
        assert result == expected

    def test_get_date_none_input(self) -> None:
        """Тестирование None входных данных"""
        result = get_date(None)  # type: ignore
        assert result is None