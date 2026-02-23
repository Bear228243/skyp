"""
Тесты для модуля search.
Проверяет функции поиска по регулярным выражениям и подсчета категорий.
"""

import pytest
from src.search import (
    search_transactions,
    count_transactions_by_categories,
    advanced_search_transactions
)


class TestSearchTransactions:
    """Тесты для функции search_transactions."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями для поиска."""
        return [
            {
                "id": 1,
                "description": "Перевод организации",
                "amount": "1000"
            },
            {
                "id": 2,
                "description": "Перевод со счета на счет",
                "amount": "2000"
            },
            {
                "id": 3,
                "description": "Оплата услуг ЖКХ",
                "amount": "3000"
            },
            {
                "id": 4,
                "description": "Перевод с карты на карту",
                "amount": "4000"
            },
            {
                "id": 5,
                "description": "Покупка в интернет-магазине",
                "amount": "5000"
            }
        ]

    def test_search_by_exact_word(self, sample_transactions):
        """Тест поиска по точному слову."""
        result = search_transactions(sample_transactions, "Перевод")
        assert len(result) == 3
        descriptions = [t["description"] for t in result]
        assert "Перевод организации" in descriptions
        assert "Перевод со счета на счет" in descriptions
        assert "Перевод с карты на карту" in descriptions

    def test_search_case_insensitive(self, sample_transactions):
        """Тест регистронезависимого поиска."""
        result = search_transactions(sample_transactions, "перевод")
        assert len(result) == 3

        result2 = search_transactions(sample_transactions, "ПЕРЕВОД")
        assert len(result2) == 3

    def test_search_partial_word(self, sample_transactions):
        """Тест поиска по части слова."""
        result = search_transactions(sample_transactions, "плат")
        assert len(result) == 1
        assert result[0]["description"] == "Оплата услуг ЖКХ"

    def test_search_no_results(self, sample_transactions):
        """Тест поиска без результатов."""
        result = search_transactions(sample_transactions, "несуществующееслово")
        assert len(result) == 0

    def test_search_empty_string(self, sample_transactions):
        """Тест поиска с пустой строкой."""
        result = search_transactions(sample_transactions, "")
        assert len(result) == 0

    def test_search_empty_list(self):
        """Тест поиска в пустом списке."""
        result = search_transactions([], "тест")
        assert len(result) == 0

    @pytest.mark.parametrize("search_term,expected_count", [
        ("организации", 1),
        ("счет", 1),  # Изменено с 2 на 1, так как "счет" встречается только в одной транзакции как отдельное слово
        ("карту", 1),  # Изменено с 2 на 1
        ("покупка", 1),
    ])
    def test_search_parametrized(self, sample_transactions, search_term, expected_count):
        """Параметризованный тест поиска."""
        result = search_transactions(sample_transactions, search_term)
        assert len(result) == expected_count


class TestAdvancedSearchTransactions:
    """Тесты для функции advanced_search_transactions."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Перевод с карты на карту"},
            {"id": 4, "description": "Оплата услуг ЖКХ"},
            {"id": 5, "description": "Покупка в магазине"},
        ]

    def test_regex_pattern_or(self, sample_transactions):
        """Тест регулярного выражения с оператором ИЛИ."""
        # Ищем транзакции, содержащие "организации" ИЛИ "услуг"
        pattern = r"организации|услуг"
        result = advanced_search_transactions(sample_transactions, pattern)
        assert len(result) == 2
        descriptions = [t["description"] for t in result]
        assert "Перевод организации" in descriptions
        assert "Оплата услуг ЖКХ" in descriptions

    def test_regex_pattern_starts_with(self, sample_transactions):
        """Тест регулярного выражения для поиска слов, начинающихся с определенной строки."""
        # Ищем транзакции, содержащие слова, начинающиеся с "перев"
        pattern = r"\bперев\w*"
        result = advanced_search_transactions(sample_transactions, pattern)
        assert len(result) == 3
        for t in result:
            assert "Перевод" in t["description"]

    def test_regex_pattern_ends_with(self, sample_transactions):
        """Тест регулярного выражения для поиска слов, заканчивающихся определенной строкой."""
        # Ищем транзакции, содержащие слова, заканчивающиеся на "чет"
        # Это найдет "счет" и "карту" (нет, "карту" не заканчивается на "чет")
        pattern = r"\b\w*чет\b"
        result = advanced_search_transactions(sample_transactions, pattern)
        assert len(result) == 1  # Изменено с 2 на 1, так как только "счет" подходит
        assert result[0]["description"] == "Перевод со счета на счет"

    def test_regex_pattern_contains(self, sample_transactions):
        """Тест регулярного выражения для поиска слов, содержащих подстроку."""
        # Ищем транзакции, содержащие "карт" в любом месте
        pattern = r"карт"
        result = advanced_search_transactions(sample_transactions, pattern)
        assert len(result) == 1  # "Перевод с карты на карту"
        assert result[0]["description"] == "Перевод с карты на карту"

    def test_invalid_regex_pattern(self, sample_transactions):
        """Тест с некорректным регулярным выражением."""
        # Некорректное регулярное выражение (незакрытая скобка)
        result = advanced_search_transactions(sample_transactions, "(незакрытая")
        assert len(result) == 0


class TestCountTransactionsByCategories:
    """Тесты для функции count_transactions_by_categories."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Перевод с карты на карту"},
            {"id": 4, "description": "Перевод организации"},
            {"id": 5, "description": "Оплата услуг"},
            {"id": 6, "description": "Перевод со счета на счет"},
        ]

    def test_count_single_category(self, sample_transactions):
        """Тест подсчета одной категории."""
        categories = ["Перевод организации"]
        result = count_transactions_by_categories(sample_transactions, categories)
        assert result["Перевод организации"] == 2

    def test_count_multiple_categories(self, sample_transactions):
        """Тест подсчета нескольких категорий."""
        categories = ["Перевод организации", "Перевод со счета на счет", "Оплата услуг"]
        result = count_transactions_by_categories(sample_transactions, categories)

        assert result["Перевод организации"] == 2
        assert result["Перевод со счета на счет"] == 2
        assert result["Оплата услуг"] == 1

    def test_category_not_found(self, sample_transactions):
        """Тест категории, которой нет в транзакциях."""
        categories = ["Несуществующая категория"]
        result = count_transactions_by_categories(sample_transactions, categories)
        assert result["Несуществующая категория"] == 0

    def test_empty_transactions(self):
        """Тест с пустым списком транзакций."""
        categories = ["Перевод организации"]
        result = count_transactions_by_categories([], categories)
        assert result["Перевод организации"] == 0

    def test_empty_categories(self, sample_transactions):
        """Тест с пустым списком категорий."""
        result = count_transactions_by_categories(sample_transactions, [])
        assert result == {}

    def test_case_insensitive_counting(self, sample_transactions):
        """Тест регистронезависимого подсчета."""
        categories = ["перевод организации", "ПЕРЕВОД СО СЧЕТА НА СЧЕТ"]
        result = count_transactions_by_categories(sample_transactions, categories)
        assert result["перевод организации"] == 2
        assert result["ПЕРЕВОД СО СЧЕТА НА СЧЕТ"] == 2

    @pytest.mark.parametrize("categories,expected", [
        (["Перевод организации", "Перевод со счета на счет"], {"Перевод организации": 2, "Перевод со счета на счет": 2}),
        (["Оплата услуг", "Покупка"], {"Оплата услуг": 1, "Покупка": 0}),
        (["Перевод с карты на карту"], {"Перевод с карты на карту": 1}),
    ])
    def test_count_parametrized(self, sample_transactions, categories, expected):
        """Параметризованный тест подсчета категорий."""
        result = count_transactions_by_categories(sample_transactions, categories)
        assert result == expected


def test_integration_search_and_count():
    """Интеграционный тест поиска и подсчета."""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": "Перевод организации"},
        {"id": 5, "description": "Оплата услуг"},
        {"id": 6, "description": "Перевод со счета на счет"},
    ]

    # Сначала ищем транзакции со словом "организации"
    found = search_transactions(transactions, "организации")
    assert len(found) == 2

    # Затем подсчитываем категории среди найденных
    categories = ["Перевод организации", "Перевод со счета на счет"]
    counts = count_transactions_by_categories(found, categories)

    assert counts["Перевод организации"] == 2
    assert counts["Перевод со счета на счет"] == 0