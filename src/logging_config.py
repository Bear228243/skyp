"""
Модуль конфигурации логирования для проекта.
Настраивает логеры для различных модулей проекта.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logger(
        name: str,
        log_file: str,
        level: int = logging.DEBUG,
        formatter: Optional[logging.Formatter] = None
) -> logging.Logger:
    """
    Настраивает и возвращает логер для указанного модуля.

    Args:
        name: Имя логера (обычно __name__ модуля)
        log_file: Имя файла для записи логов
        level: Уровень логирования
        formatter: Форматтер для логов

    Returns:
        Настроенный объект логера
    """
    # Создаем логер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Проверяем, не добавлены ли уже обработчики
    if logger.handlers:
        return logger

    # Создаем абсолютный путь к папке logs
    project_root = Path(__file__).parent.parent
    log_dir = project_root / "logs"

    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    # Создаем обработчик для файла
    file_path = log_dir / log_file
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

    # Добавляем вывод в консоль для удобства отладки
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

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


def get_external_api_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля external_api.
    """
    return setup_logger(
        name='external_api',
        log_file='external_api.log',
        level=logging.DEBUG
    )


def get_processing_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля processing.
    """
    return setup_logger(
        name='processing',
        log_file='processing.log',
        level=logging.DEBUG
    )


def get_widget_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля widget.
    """
    return setup_logger(
        name='widget',
        log_file='widget.log',
        level=logging.DEBUG
    )


def get_generators_logger() -> logging.Logger:
    """
    Возвращает настроенный логер для модуля generators.
    """
    return setup_logger(
        name='generators',
        log_file='generators.log',
        level=logging.DEBUG
    )
