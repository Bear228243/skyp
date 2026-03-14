"""
Дополнительные тесты для модуля masks.
Проверяет граничные случаи и обработку ошибок.
"""

from unittest.mock import patch

import pytest

from src.masks import get_mask_account, get_mask_card_number, mask_bank_data


class TestMasksAdditional:
    """Дополнительные тесты для функций маскирования."""

    @patch('src.masks.logger')
    def test_get_mask_card_number_logging_error(self, mock_logger):
        """Тест логирования ошибки при маскировании карты."""
        with pytest.raises(ValueError):
            get_mask_card_number("123")
        mock_logger.error.assert_called()

    @patch('src.masks.logger')
    def test_get_mask_card_number_logging_success(self, mock_logger):
        """Тест логирования успеха при маскировании карты."""
        result = get_mask_card_number("7000792289606361")
        assert result == "7000 79** **** 6361"
        mock_logger.info.assert_called()

    @patch('src.masks.logger')
    def test_get_mask_account_logging_error(self, mock_logger):
        """Тест логирования ошибки при маскировании счета."""
        with pytest.raises(ValueError):
            get_mask_account("abc")
        mock_logger.error.assert_called()

    @patch('src.masks.logger')
    def test_get_mask_account_logging_success(self, mock_logger):
        """Тест логирования успеха при маскировании счета."""
        result = get_mask_account("64686473678894779589")
        assert result == "**9589"
        mock_logger.info.assert_called()

    def test_mask_bank_data_card(self):
        """Тест автоматического определения карты."""
        result = mask_bank_data("7000792289606361")
        assert result == "7000 79** **** 6361"

    def test_mask_bank_data_account(self):
        """Тест автоматического определения счета."""
        result = mask_bank_data("64686473678894779589")
        assert result == "**9589"

    def test_mask_bank_data_invalid_length(self):
        """Тест ошибки при некорректной длине данных."""
        with pytest.raises(ValueError, match="Не удалось определить тип банковских данных"):
            mask_bank_data("123")

    def test_mask_bank_data_empty_string(self):
        """Тест с пустой строкой."""
        with pytest.raises(ValueError, match="Не удалось определить тип банковских данных"):
            mask_bank_data("")

    def test_mask_bank_data_with_letters(self):
        """Тест с буквами в номере."""
        with pytest.raises(ValueError):
            mask_bank_data("abcd1234efgh5678")

    @patch('src.masks.logger')
    def test_mask_bank_data_logging_error(self, mock_logger):
        """Тест логирования ошибки при автоматическом определении."""
        with pytest.raises(ValueError):
            mask_bank_data("invalid")
        mock_logger.error.assert_called()

    @patch('src.masks.get_mask_card_number')
    def test_mask_bank_data_card_exception(self, mock_get_mask):
        """Тест обработки исключения при маскировании карты."""
        mock_get_mask.side_effect = Exception("Card error")
        with pytest.raises(Exception):
            mask_bank_data("7000792289606361")

    @patch('src.masks.get_mask_account')
    def test_mask_bank_data_account_exception(self, mock_get_mask):
        """Тест обработки исключения при маскировании счета."""
        mock_get_mask.side_effect = Exception("Account error")
        with pytest.raises(Exception):
            mask_bank_data("64686473678894779589")
