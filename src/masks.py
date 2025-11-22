from src.logging_config import get_masks_logger

logger = get_masks_logger()

def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 цифры"""
    logger.debug(f"Попытка маскировки номера карты: {card_number}")

    #Delete space for check
    cleaned_number = card_number.replace(' ', '')

    #Check len numb card
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
    """Маскирует номер счета, оставляя последние 4 цифры"""
    logger.debug(f"Попытка маскирования номера счета: {account_number}")

    #Check len numb card(min reasonable len)
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

    Аргументы:
        data: Строка с банковскими данными (номер карты или счета)

    Возвращает:
        Замаскированные данные

    Исключения:
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


def validate_and_mask_card(card_number: str) -> str:
    """
    Проверяет и маскирует номер карты с дополнительной валидацией.

    Аргументы:
        card_number: Номер карты для проверки и маскирования

    Возвращает:
        Замаскированный номер карты

    Исключения:
        ValueError: Если номер карты не прошел валидацию
    """
    logger.debug(f"Расширенная валидация и маскирование номера карты: {card_number}")

    # Проверяем базовые критерии
    if not card_number or not isinstance(card_number, str):
        error_msg = "Номер карты должен быть непустой строкой"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверяем наличие только допустимых символов
    cleaned = card_number.replace(" ", "")
    if not cleaned.isdigit():
        error_msg = f"Номер карты содержит недопустимые символы: {card_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Применяем алгоритм Луна для проверки контрольной суммы
    if not _luhn_check(cleaned):
        error_msg = f"Номер карты не прошел проверку контрольной суммы: {card_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.debug(f"Номер карты прошел расширенную валидацию: {card_number}")
    return get_mask_card_number(card_number)


def _luhn_check(card_number: str) -> bool:
    """
    Проверяет номер карты по алгоритму Луна.

    Аргументы:
        card_number: Номер карты без пробелов

    Возвращает:
        True если номер валиден, иначе False
    """
    try:
        digits = [int(d) for d in card_number]
        checksum = 0

        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 0:
                checksum += digit
            else:
                doubled = digit * 2
                checksum += doubled if doubled < 10 else doubled - 9

        return checksum % 10 == 0

    except Exception as e:
        logger.error(f"Ошибка при проверке алгоритмом Луна: {e}")
        return False