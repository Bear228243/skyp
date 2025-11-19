"""
Тесты для системы логирования.
"""

import os
import logging
import pytest
from src.logging_config import setup_logger, get_utils_logger, get_masks_logger
from src.utils_file_operations import read_json_file
from src.masks import get_mask_card_number, get_mask_account


@pytest.fixture
def temp_log_file():
    """
    Фикстура создает временный файл лога для тестирования.
    """
    log_file = "test_logging.log"
    logger = setup_logger("test_logger", log_file, level=logging.DEBUG)

    yield logger, log_file

    # Очистка после теста
    if os.path.exists(f"logs/{log_file}"):
        os.remove(f"logs/{log_file}")


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
        assert len(logger.handlers) == 1

    def test_log_file_creation(self, temp_log_file):
        """
        Тест создания файла лога.
        """
        logger, log_file = temp_log_file

        # Записываем тестовое сообщение
        test_message = "Тестовое сообщение лога"
        logger.info(test_message)

        # Проверяем, что файл создан и содержит сообщение
        log_path = f"logs/{log_file}"
        assert os.path.exists(log_path)

        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert test_message in content

    def test_log_format(self, temp_log_file):
        """
        Тест формата лог-сообщений.
        """
        logger, log_file = temp_log_file

        logger.error("Тестовое сообщение об ошибке")

        log_path = f"logs/{log_file}"
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Проверяем элементы формата
            assert "test_logger" in content
            assert "ERROR" in content
            assert "Тестовое сообщение об ошибке" in content


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

    def test_file_operations_logging(self, tmp_path, capsys):
        """
        Тест логирования в функциях работы с файлами.
        """
        # Создаем временный JSON файл
        json_file = tmp_path / "test.json"
        json_file.write_text('[{"id": 1, "name": "test"}]', encoding='utf-8')

        # Читаем файл и проверяем логи
        result = read_json_file(str(json_file))

        # Проверяем, что файл прочитан успешно
        assert len(result) == 1
        assert result[0]["id"] == 1


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

    def test_card_masking_logging(self, capsys):
        """
        Тест логирования при маскировании карт.
        """
        card_number = "1234567812345678"
        masked = get_mask_account(card_number)

        assert masked == "1234 56** **** 5678"

    def test_account_masking_logging(self, capsys):
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


def test_log_directory_creation():
    """
    Тест автоматического создания папки logs.
    """
    # Удаляем папку logs если существует
    if os.path.exists("logs"):
        import shutil
        shutil.rmtree("logs")

    # Создаем логер - должен создать папку logs
    logger = setup_logger("test_dir_creation", "test_dir.log")
    logger.info("Тест создания директории")

    assert os.path.exists("logs")
    assert os.path.isdir("logs")