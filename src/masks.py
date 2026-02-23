"""Модуль для маскирования номеров карт и счетов."""

from .logging_config import get_masks_logger

logger = get_masks_logger()


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя первые 6 и последние 4 цифры.

    Args:
        card_number: Номер карты в формате "XXXX XX** **** XXXX" или "XXXXXXXXXXXXXXXX"

    Returns:
        Замаскированный номер карты

    Raises:
        ValueError: Если номер карты некорректен
    """
    logger.debug(f"Попытка маскировки номера карты: {card_number}")

    # Удаляем пробелы для проверки
    cleaned_number = card_number.replace(' ', '')

    # Проверяем длину номера карты
    if len(cleaned_number) != 16:
        error_msg = f"Неверная длина номера карты: {len(cleaned_number)}. Ожидается 16 цифр"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверяем, что номер состоит только из цифр
    if not cleaned_number.isdigit():
        error_msg = f"Номер карты содержит недопустимые символы: {card_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        # Маскируем номер карты
        masked_number = (
            f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
        )

        logger.info(f"Успешно замаскирован номер карты: {card_number} -> {masked_number}")
        return masked_number

    except Exception as e:
        error_msg = f"Ошибка при маскировании номера карты {card_number}: {e}"
        logger.error(error_msg)
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя последние 4 цифры.

    Args:
        account_number: Номер счета

    Returns:
        Замаскированный номер счета

    Raises:
        ValueError: Если номер счета некорректен
    """
    logger.debug(f"Попытка маскирования номера счета: {account_number}")

    # Проверяем минимальную длину номера счета
    if len(account_number) < 4:
        error_msg = f"Слишком короткий номер счёта: {account_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if not account_number.isdigit():
        error_msg = f"Номер счета содержит недопустимые символы: {account_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        # Маскируем номер счета, оставляя только последние 4 цифры
        masked_number = f"**{account_number[-4:]}"

        logger.info(f"Успешно замаскирован номер счета: {account_number} -> {masked_number}")
        return masked_number

    except Exception as e:
        error_msg = f"Ошибка при маскировании номера счета {account_number}: {e}"
        logger.error(error_msg)
        raise


def mask_bank_data(data: str) -> str:
    """
    Автоматически определяет тип банковских данных и применяет соответствующую маску.

    Args:
        data: Строка с банковскими данными (номер карты или счета)

    Returns:
        Замаскированные данные

    Raises:
        ValueError: Если тип данных не может быть определен
    """
    logger.debug(f"Автоматическое определение типа данных для маскирования: {data}")

    # Очищаем данные от пробелов для анализа
    cleaned_data = data.replace(" ", "")

    try:
        # Определяем тип данных по длине и формату
        if len(cleaned_data) == 16 and cleaned_data.isdigit():
            # Это номер карты
            logger.debug(f"Определен как номер карты: {data}")
            return get_mask_card_number(data)
        elif len(cleaned_data) >= 4:
            # Это номер счета
            logger.debug(f"Определен как номер счета: {data}")
            return get_mask_account(data)
        else:
            error_msg = f"Не удалось определить тип банковских данных: {data}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    except Exception as e:
        error_msg = f"Ошибка при автоматическом маскировании данных {data}: {e}"
        logger.error(error_msg)
        raise