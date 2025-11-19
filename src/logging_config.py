"""
Модуль конфигурации логирования для проекта.
Настраивает логеры для различных модулей проекта.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
        name: str,
        log_file: str,
        level: int = logging.DEBUG,
        formatter: Optional[logging.Formatter] = None
) -> logging.Logger:
    """
    Настраивает и возвращает логер для указанного модуля.

    Аргументы:
        name: Имя логера (обычно __name__ модуля)
        log_file: Имя файла для записи логов
        level: Уровень логирования
        formatter: Форматтер для логов

    Возвращает:
        Настроенный объект логера
    """
    # Создаем логер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Проверяем, не добавлены ли уже обработчики
    if logger.handlers:
        return logger

    # Создаем папку для логов, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Создаем обработчик для файла
    file_path = os.path.join(log_dir, log_file)
    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )

    # Устанавливаем уровень для обработчика
    file_handler.setLevel(level)

    # Создаем форматтер, если не передан
    if formatter is None:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Устанавливаем форматтер для обработчика
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логеру
    logger.addHandler(file_handler)

    return logger


def get_utils_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля utils.
    """
    return setup_logger(
        name='utils',
        log_file='utils.log',
        level=logging.DEBUG
    )


def get_masks_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля masks.
    """
    return setup_logger(
        name='masks',
        log_file='masks.log',
        level=logging.DEBUG
    )


def get_currency_converter_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля currency_converter.
    """
    return setup_logger(
        name='external_api.currency_converter',
        log_file='currency_converter.log',
        level=logging.DEBUG
    )