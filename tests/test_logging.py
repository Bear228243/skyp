"""
Тесты для системы логирования.
"""

import os
import logging
import pytest
from src.logging_config import setup_logger, get_utils_logger, get_masks_logger
from src.utils import read_json_file
from src.masks import get_mask_card_number, get_mask_account


@pytest.fixture
def temp_log_file():
    """
    Фикстура создает временный файл лога для тестирования.
    """
    log_file = "test_logging.log"

    # Очищаем существующие обработчики
    logger = logging.getLogger("test_logger")
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    logger = setup_logger("test_logger", log_file, level=logging.DEBUG)

    yield logger, log_file

    # Очистка после теста
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    # Удаляем файл если существует
    log_path = os.path.join("logs", log_file)
    if os.path.exists(log_path):
        try:
            os.remove(log_path)
        except PermissionError:
            pass


class TestLoggingConfiguration:
    """Тесты конфигурации логирования."""

    def test_setup_logger_creation(self, temp_log_file):
        """
        Тест создания логера через setup_logger.
        """
        logger, log_file = temp_log_file

        assert logger is not None
        assert logger.name == "test_logger"
        assert logger.level == logging.DEBUG
        assert len(logger.handlers) > 0

    def test_log_file_creation(self, temp_log_file):
        """
        Тест создания файла лога.
        """
        logger, log_file = temp_log_file

        # Записываем тестовое сообщение
        test_message = "Тестовое сообщение лога"
        logger.info(test_message)

        # Проверяем, что файл создан
        log_path = os.path.join("logs", log_file)
        assert os.path.exists(log_path)


class TestUtilsLogging:
    """Тесты логирования в модуле utils."""

    def test_utils_logger_creation(self):
        """
        Тест создания логера для модуля utils.
        """
        logger = get_utils_logger()

        assert logger is not None
        assert logger.name == "utils"
        assert logger.level == logging.DEBUG


class TestMasksLogging:
    """Тесты логирования в модуле masks."""

    def test_masks_logger_creation(self):
        """
        Тест создания логера для модуля masks.
        """
        logger = get_masks_logger()

        assert logger is not None
        assert logger.name == "masks"
        assert logger.level == logging.DEBUG

    def test_card_masking_logging(self):
        """
        Тест логирования при маскировании карт.
        """
        card_number = "1234567812345678"
        masked = get_mask_card_number(card_number)

        assert masked == "1234 56** **** 5678"

    def test_account_masking_logging(self):
        """
        Тест логирования при маскировании счетов.
        """
        account_number = "12345678901234567890"
        masked = get_mask_account(account_number)

        assert masked == "**7890"

    def test_masking_error_logging(self):
        """
        Тест логирования ошибок при маскировании.
        """
        with pytest.raises(ValueError):
            get_mask_card_number("invalid_card_number")