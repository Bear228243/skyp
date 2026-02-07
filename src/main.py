"""Основной модуль для запуска приложения."""

import sys
from pathlib import Path

# Добавляем src в путь Python
sys.path.insert(0, str(Path(__file__).parent))

from src.masks import get_mask_card_number, get_mask_account, mask_bank_data
from src.widget import mask_account_card, get_date, format_transaction
from src.processing import filter_by_state, sort_by_date, get_last_transactions
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.decorators import log
from src.utils import read_json_file, load_transactions_from_file
from src.external_api import get_amount_in_rubles


@log()
def process_transactions(file_path: str) -> None:
    """
    Обрабатывает транзакции из файла и выводит результат.

    Args:
        file_path: Путь к файлу с транзакциями
    """
    print(f"Обработка файла: {file_path}")

    # Загружаем транзакции
    transactions = load_transactions_from_file(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции")
        return

    print(f"Загружено {len(transactions)} транзакций")

    # Получаем последние 5 выполненных транзакций
    last_transactions = get_last_transactions(transactions, 5)

    print("\nПоследние 5 выполненных транзакций:")
    print("-" * 60)

    for i, transaction in enumerate(last_transactions, 1):
        formatted = format_transaction(transaction)
        print(f"{i}. {formatted}")


def demo_all_modules() -> None:
    """Демонстрация работы всех модулей."""

    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ПРОЕКТА")
    print("=" * 60)

    # 1. Маскирование данных
    print("\n1. Маскирование данных:")
    print("-" * 40)

    card = "7000792289606361"
    account = "73654108430135874305"

    print(f"Карта: {card}")
    print(f"Замаскированная карта: {get_mask_card_number(card)}")
    print(f"Счет: {account}")
    print(f"Замаскированный счет: {get_mask_account(account)}")
    print(f"Автоматическое определение: {mask_bank_data(card)}")
    print(f"Автоматическое определение: {mask_bank_data(account)}")

    # 2. Виджеты
    print("\n2. Виджеты:")
    print("-" * 40)

    print(f"Форматирование даты: {get_date('2024-03-14T10:30:00.000')}")
    print(f"Маскирование в строке: {mask_account_card('Visa Platinum 7000792289606361')}")
    print(f"Маскирование счета в строке: {mask_account_card('Счет 64686473678894779589')}")

    # 3. Генераторы
    print("\n3. Генераторы:")
    print("-" * 40)

    print("Первые 5 номеров карт:")
    for i, card_num in enumerate(card_number_generator(1, 5), 1):
        print(f"  {i}. {card_num}")

    # 4. Декораторы
    print("\n4. Декораторы:")
    print("-" * 40)

    @log()
    def demo_add(a: int, b: int) -> int:
        return a + b

    result = demo_add(10, 20)
    print(f"Результат функции с декоратором: {result}")

    # 5. Пример транзакции для конвертации
    print("\n5. Конвертация валют:")
    print("-" * 40)

    sample_transaction = {
        "id": 1,
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }

    try:
        # В реальном использовании нужен API ключ
        print(f"Пример транзакции для конвертации: {sample_transaction}")
        print("Для работы конвертации нужен API ключ в файле .env")
    except Exception as e:
        print(f"Ошибка конвертации (ожидаемо без API ключа): {e}")


def main() -> None:
    """Основная функция приложения."""

    # Демонстрация всех модулей
    demo_all_modules()

    # Пример обработки файла (если он существует)
    data_file = Path("data/operations.json")
    if data_file.exists():
        print("\n" + "=" * 60)
        print("ОБРАБОТКА РЕАЛЬНЫХ ДАННЫХ")
        print("=" * 60)

        try:
            process_transactions(str(data_file))
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == "__main__":
    main()