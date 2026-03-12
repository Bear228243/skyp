"""
Основной модуль для запуска приложения с пользовательским интерфейсом.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Добавляем src в путь Python
sys.path.insert(0, str(Path(__file__).parent))

from src.widget import format_transaction  # noqa: E402
from src.processing import filter_by_state, sort_by_date  # noqa: E402
from src.generators import filter_by_currency  # noqa: E402
from src.utils import load_transactions_from_file  # noqa: E402
from src.external_api import get_amount_in_rubles  # noqa: E402
from src.search import search_transactions, count_transactions_by_categories  # noqa: E402


class TransactionApp:
    """Класс для управления приложением."""

    VALID_STATUSES: List[str] = ["EXECUTED", "CANCELED", "PENDING"]

    def __init__(self) -> None:
        self.transactions: List[Dict[str, Any]] = []
        self.filtered_transactions: List[Dict[str, Any]] = []
        self.current_file_type: Optional[str] = None

    def print_header(self, text: str) -> None:
        """Выводит заголовок с разделителями."""
        print("\n" + "=" * 60)
        print(f" {text}")
        print("=" * 60)

    def print_menu(self) -> None:
        """Выводит главное меню."""
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")
        print("0. Выход")

    def get_file_path(self, file_type: str) -> Optional[str]:
        """Получает путь к файлу от пользователя."""
        print(f"\nВведите путь к {file_type.upper()} файлу (или нажмите Enter для использования файла по умолчанию):")

        default_paths: Dict[str, str] = {
            'json': 'data/operations.json',
            'csv': 'data/transactions.csv',
            'xlsx': 'data/transactions_excel.xlsx'
        }

        user_input: str = input("> ").strip()

        if not user_input:
            # Используем путь по умолчанию
            default: Optional[str] = default_paths.get(file_type)
            if default and os.path.exists(default):
                return default
            else:
                print(f"Файл по умолчанию {default} не найден.")
                return None

        return user_input if os.path.exists(user_input) else None

    def load_transactions(self, file_type: str) -> bool:
        """
        Загружает транзакции из файла.

        Args:
            file_type: Тип файла ('json', 'csv', 'xlsx')

        Returns:
            True если загрузка успешна, иначе False
        """
        file_path: Optional[str] = self.get_file_path(file_type)

        if not file_path:
            print("\n❌ Файл не найден или указан неверный путь.")
            return False

        print(f"\n📂 Загрузка транзакций из файла: {file_path}")
        self.transactions = load_transactions_from_file(file_path)

        if not self.transactions:
            print("❌ Не удалось загрузить транзакции из файла.")
            return False

        self.current_file_type = file_type
        print(f"✅ Успешно загружено {len(self.transactions)} транзакций.")
        return True

    def get_status_filter(self) -> Optional[str]:
        """
        Получает статус для фильтрации от пользователя.

        Returns:
            Выбранный статус или None если пользователь хочет выйти
        """
        while True:
            print("\n" + "-" * 40)
            print("Введите статус, по которому необходимо выполнить фильтрацию.")
            print(f"Доступные статусы: {', '.join(self.VALID_STATUSES)}")
            print("(или '0' для возврата в главное меню)")

            status: str = input("> ").strip().upper()

            if status == '0':
                return None

            if status in self.VALID_STATUSES:
                print(f"\n✅ Операции отфильтрованы по статусу '{status}'")
                return status
            else:
                print(f"\n❌ Статус операции '{status}' недоступен.")

    def get_yes_no(self, question: str) -> bool:
        """
        Задает вопрос с ответом Да/Нет.

        Args:
            question: Вопрос для пользователя

        Returns:
            True если ответ 'да', иначе False
        """
        while True:
            answer: str = input(f"{question} (Да/Нет): ").strip().lower()
            if answer in ['да', 'yes', 'y', 'д']:
                return True
            elif answer in ['нет', 'no', 'n', 'н']:
                return False
            else:
                print("Пожалуйста, ответьте 'Да' или 'Нет'.")

    def get_sort_order(self) -> Optional[str]:
        """
        Получает порядок сортировки от пользователя.

        Returns:
            'asc' для возрастания, 'desc' для убывания, None для отмены
        """
        while True:
            print("\nОтсортировать по возрастанию или по убыванию?")
            print("(введите 'возрастание' или 'убывание', или '0' для отмены)")

            order: str = input("> ").strip().lower()

            if order == '0':
                return None

            if order in ['возрастание', 'asc', 'по возрастанию']:
                return 'asc'
            elif order in ['убывание', 'desc', 'по убыванию']:
                return 'desc'
            else:
                print("Пожалуйста, введите 'возрастание' или 'убывание'.")

    def get_search_string(self) -> Optional[str]:
        """
        Получает строку для поиска от пользователя.

        Returns:
            Строка для поиска или None для отмены
        """
        print("\nВведите слово для поиска в описании транзакций")
        print("(или нажмите Enter для пропуска):")

        search: str = input("> ").strip()
        return search if search else None

    def apply_filters(self) -> List[Dict[str, Any]]:
        """
        Применяет все выбранные фильтры к транзакциям.

        Returns:
            Отфильтрованный список транзакций
        """
        if not self.transactions:
            return []

        result: List[Dict[str, Any]] = self.transactions.copy()

        # 1. Фильтрация по статусу
        status: Optional[str] = self.get_status_filter()
        if status is None:
            return []  # Пользователь хочет вернуться в меню

        result = filter_by_state(result, status)

        # 2. Сортировка по дате
        if self.get_yes_no("\nОтсортировать операции по дате?"):
            order: Optional[str] = self.get_sort_order()
            if order:
                descending: bool = (order == 'desc')
                result = sort_by_date(result, descending)
                print(f"✅ Транзакции отсортированы по {'убыванию' if descending else 'возрастанию'}")

        # 3. Фильтрация по рублевым транзакциям
        if self.get_yes_no("\nВыводить только рублевые транзакции?"):
            rub_transactions: List[Dict[str, Any]] = list(filter_by_currency(result, "RUB"))
            print(f"✅ Оставлено {len(rub_transactions)} рублевых транзакций")
            result = rub_transactions

        # 4. Поиск по описанию
        if self.get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании?"):
            search_string: Optional[str] = self.get_search_string()
            if search_string:
                result = search_transactions(result, search_string)
                print(f"✅ Найдено {len(result)} транзакций по слову '{search_string}'")

        return result

    def display_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        """
        Отображает список транзакций в отформатированном виде.

        Args:
            transactions: Список транзакций для отображения
        """
        if not transactions:
            print("\n❌ Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return

        print("\n" + "=" * 60)
        print(f"📊 ВСЕГО БАНКОВСКИХ ОПЕРАЦИЙ В ВЫБОРКЕ: {len(transactions)}")
        print("=" * 60)

        for i, transaction in enumerate(transactions, 1):
            print(f"\n{i}. {format_transaction(transaction)}")

            # Дополнительная информация о конвертации валют
            try:
                amount_in_rub: float = get_amount_in_rubles(transaction)
                if amount_in_rub:
                    print(f"   (в рублях: {amount_in_rub:.2f} RUB)")
            except Exception:
                pass

    def run(self) -> None:
        """Запускает основное приложение."""

        self.print_header("ПРИВЕТ! Добро пожаловать в программу работы с банковскими транзакциями")

        while True:
            self.print_menu()
            choice: str = input("> ").strip()

            if choice == '0':
                print("\n👋 До свидания!")
                break

            # Выбор типа файла
            file_type: Optional[str] = None
            if choice == '1':
                file_type = 'json'
            elif choice == '2':
                file_type = 'csv'
            elif choice == '3':
                file_type = 'xlsx'
            else:
                print("\n❌ Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 0 для выхода.")
                continue

            # Загрузка транзакций
            if not self.load_transactions(file_type):
                continue

            print(f"\n✅ Для обработки выбран {file_type.upper()}-файл.")

            # Применение фильтров
            filtered: List[Dict[str, Any]] = self.apply_filters()

            # Отображение результатов
            print("\n" + "-" * 40)
            print("📋 РАСПЕЧАТЫВАЮ ИТОГОВЫЙ СПИСОК ТРАНЗАКЦИЙ...")
            self.display_transactions(filtered)

            # Подсчет категорий (дополнительная информация)
            if filtered:
                categories: List[str] = ["Перевод организации", "Перевод со счета на счет",
                                         "Перевод с карты на карту", "Открытие вклада"]
                category_counts: Dict[str, int] = count_transactions_by_categories(filtered, categories)

                print("\n" + "-" * 40)
                print("📊 СТАТИСТИКА ПО КАТЕГОРИЯМ:")
                for category, count in category_counts.items():
                    if count > 0:
                        print(f"  • {category}: {count}")

            input("\nНажмите Enter для продолжения...")


def main() -> None:
    """Основная функция приложения."""
    app: TransactionApp = TransactionApp()
    app.run()


if __name__ == "__main__":
    main()
