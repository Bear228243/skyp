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


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "description": "Перевод организации", "amount": "1000"},
        {"id": 2, "description": "Перевод со счета на счет", "amount": "2000"},
        {"id": 3, "description": "Оплата услуг ЖКХ", "amount": "3000"},
        {"id": 4, "description": "Перевод с карты на карту", "amount": "4000"},
        {"id": 5, "description": "Покупка в интернет-магазине", "amount": "5000"},
    ]


class TestSearchTransactions:
    """Тесты для функции search_transactions."""

    def test_search_exact_word(self, sample_transactions):
        """Тест поиска по точному слову."""
        result = search_transactions(sample_transactions, "Перевод")
        assert len(result) == 3

    def test_search_case_insensitive(self, sample_transactions):
        """Тест регистронезависимого поиска."""
        result = search_transactions(sample_transactions, "перевод")
        assert len(result) == 3

    def test_search_partial(self, sample_transactions):
        """Тест поиска по части слова."""
        result = search_transactions(sample_transactions, "плат")
        assert len(result) == 1
        assert result[0]["description"] == "Оплата услуг ЖКХ"

    def test_search_no_results(self, sample_transactions):
        """Тест поиска без результатов."""
        result = search_transactions(sample_transactions, "несуществующее")
        assert len(result) == 0

    def test_search_empty_string(self, sample_transactions):
        """Тест с пустой строкой."""
        result = search_transactions(sample_transactions, "")
        assert len(result) == 0

    def test_search_empty_list(self):
        """Тест с пустым списком."""
        result = search_transactions([], "тест")
        assert len(result) == 0

    def test_search_missing_description(self):
        """Тест при отсутствии описания."""
        transactions = [{"id": 1}, {"id": 2, "description": "тест"}]
        result = search_transactions(transactions, "тест")
        assert len(result) == 1
        assert result[0]["id"] == 2

    @pytest.mark.parametrize("term,expected", [
        ("организации", 1),
        ("счет", 1),  # Изменено с 2 на 1 - только одна транзакция содержит "счет" как слово
        ("карту", 1),  # Изменено с 2 на 1 - только одна транзакция содержит "карту" как слово
        ("покупка", 1),
    ])
    def test_search_parametrized(self, sample_transactions, term, expected):
        """Параметризованный тест поиска."""
        result = search_transactions(sample_transactions, term)
        assert len(result) == expected


class TestAdvancedSearchTransactions:
    """Тесты для функции advanced_search_transactions."""

    @pytest.fixture
    def adv_transactions(self):
        """Фикстура для расширенного поиска."""
        return [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Перевод с карты на карту"},
            {"id": 4, "description": "Оплата услуг ЖКХ"},
            {"id": 5, "description": "Покупка в магазине"},
        ]

    def test_regex_or(self, adv_transactions):
        """Тест оператора ИЛИ."""
        result = advanced_search_transactions(adv_transactions, r"организации|услуг")
        assert len(result) == 2

    def test_regex_starts_with(self, adv_transactions):
        """Тест поиска слов, начинающихся с..."""
        result = advanced_search_transactions(adv_transactions, r"\bперев\w*")
        assert len(result) == 3

    def test_regex_ends_with(self, adv_transactions):
        """Тест поиска слов, заканчивающихся на..."""
        result = advanced_search_transactions(adv_transactions, r"\b\w*чет\b")
        assert len(result) == 1  # "счет"

    def test_regex_contains(self, adv_transactions):
        """Тест поиска подстроки."""
        result = advanced_search_transactions(adv_transactions, r"карт")
        assert len(result) == 1  # "карты" и "карту"

    def test_invalid_regex(self, adv_transactions):
        """Тест с некорректным regex."""
        result = advanced_search_transactions(adv_transactions, "[")
        assert len(result) == 0

    def test_empty_pattern(self, adv_transactions):
        """Тест с пустым шаблоном."""
        result = advanced_search_transactions(adv_transactions, "")
        assert len(result) == 0


class TestCountTransactionsByCategories:
    """Тесты для функции count_transactions_by_categories."""

    @pytest.fixture
    def cat_transactions(self):
        """Фикстура для подсчета категорий."""
        return [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Перевод с карты на карту"},
            {"id": 4, "description": "Перевод организации"},
            {"id": 5, "description": "Оплата услуг"},
            {"id": 6, "description": "Перевод со счета на счет"},
        ]

    def test_count_single_category(self, cat_transactions):
        """Тест подсчета одной категории."""
        result = count_transactions_by_categories(cat_transactions, ["Перевод организации"])
        assert result["Перевод организации"] == 2

    def test_count_multiple_categories(self, cat_transactions):
        """Тест подсчета нескольких категорий."""
        categories = ["Перевод организации", "Перевод со счета на счет", "Оплата услуг"]
        result = count_transactions_by_categories(cat_transactions, categories)
        assert result["Перевод организации"] == 2
        assert result["Перевод со счета на счет"] == 2
        assert result["Оплата услуг"] == 1

    def test_category_not_found(self, cat_transactions):
        """Тест отсутствующей категории."""
        result = count_transactions_by_categories(cat_transactions, ["Несуществующая"])
        assert result["Несуществующая"] == 0

    def test_empty_transactions(self):
        """Тест с пустым списком транзакций."""
        result = count_transactions_by_categories([], ["тест"])
        assert result["тест"] == 0

    def test_empty_categories(self, cat_transactions):
        """Тест с пустым списком категорий."""
        result = count_transactions_by_categories(cat_transactions, [])
        assert result == {}

    def test_case_insensitive(self, cat_transactions):
        """Тест регистронезависимости."""
        result = count_transactions_by_categories(cat_transactions, ["перевод организации"])
        assert result["перевод организации"] == 2
