"""
Дополнительные тесты для модуля search.
Проверяет граничные случаи и обработку ошибок.
"""

import pytest
from src.search import (
    search_transactions,
    count_transactions_by_categories,
    advanced_search_transactions
)


class TestSearchTransactionsEdgeCases:
    """Тесты граничных случаев для search_transactions."""

    def test_search_with_none_transactions(self):
        """Тест с None вместо списка транзакций."""
        result = search_transactions(None, "тест")  # type: ignore
        assert result == []

    def test_search_with_none_search_string(self, sample_transactions):
        """Тест с None вместо строки поиска."""
        result = search_transactions(sample_transactions, None)  # type: ignore
        assert result == []

    def test_search_with_missing_description(self):
        """Тест транзакций без описания."""
        transactions = [
            {"id": 1, "amount": "1000"},
            {"id": 2, "description": "Есть описание", "amount": "2000"}
        ]
        result = search_transactions(transactions, "описание")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_search_with_special_characters(self):
        """Тест поиска со специальными символами."""
        transactions = [
            {"id": 1, "description": "Транзакция с $pecial символами"},
            {"id": 2, "description": "Обычная транзакция"}
        ]
        result = search_transactions(transactions, "$pecial")
        assert len(result) == 1
        assert result[0]["id"] == 1


class TestAdvancedSearchTransactionsEdgeCases:
    """Тесты граничных случаев для advanced_search_transactions."""

    def test_advanced_search_with_empty_pattern(self, sample_transactions):
        """Тест с пустым шаблоном."""
        result = advanced_search_transactions(sample_transactions, "")
        assert result == []

    def test_advanced_search_with_invalid_regex(self, sample_transactions):
        """Тест с некорректным регулярным выражением."""
        result = advanced_search_transactions(sample_transactions, "[")
        assert result == []

    def test_advanced_search_with_complex_regex(self):
        """Тест со сложным регулярным выражением."""
        transactions = [
            {"id": 1, "description": "Тест 123"},
            {"id": 2, "description": "Пример ABC"},
            {"id": 3, "description": "Другой тест 456"}
        ]
        # Ищем цифры
        result = advanced_search_transactions(transactions, r"\d+")
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_advanced_search_with_unicode(self):
        """Тест с юникод символами."""
        transactions = [
            {"id": 1, "description": "Кириллица"},
            {"id": 2, "description": "English"}
        ]
        result = advanced_search_transactions(transactions, r"Кириллица")
        assert len(result) == 1
        assert result[0]["id"] == 1


class TestCountTransactionsByCategoriesEdgeCases:
    """Тесты граничных случаев для count_transactions_by_categories."""

    def test_count_with_none_transactions(self):
        """Тест с None вместо списка транзакций."""
        categories = ["Категория 1", "Категория 2"]
        result = count_transactions_by_categories(None, categories)  # type: ignore
        assert result == {"Категория 1": 0, "Категория 2": 0}

    def test_count_with_none_categories(self, sample_transactions):
        """Тест с None вместо списка категорий."""
        result = count_transactions_by_categories(sample_transactions, None)  # type: ignore
        assert result == {}

    def test_count_with_duplicate_categories(self, sample_transactions):
        """Тест с дублирующимися категориями в списке."""
        categories = ["Перевод организации", "Перевод организации"]
        result = count_transactions_by_categories(sample_transactions, categories)
        # Должен подсчитать отдельно для каждой записи
        assert result["Перевод организации"] == 2

    def test_count_with_partial_matches(self):
        """Тест с частичным совпадением категорий."""
        transactions = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод со счета на счет"},
            {"id": 3, "description": "Перевод с карты на карту"}
        ]
        categories = ["Перевод"]  # Должно совпасть со всеми
        result = count_transactions_by_categories(transactions, categories)
        assert result["Перевод"] == 3

    def test_count_with_empty_descriptions(self):
        """Тест с пустыми описаниями."""
        transactions = [
            {"id": 1, "description": ""},
            {"id": 2, "description": None},
            {"id": 3}  # Без поля description
        ]
        categories = ["Тест"]
        result = count_transactions_by_categories(transactions, categories)
        assert result["Тест"] == 0

    def test_count_logging_error(self, caplog):
        """Тест логирования ошибки."""
        with caplog.at_level('ERROR'):
            # Передаем некорректные данные, чтобы вызвать ошибку
            result = count_transactions_by_categories("not a list", ["test"])  # type: ignore
            assert "Ошибка при подсчете категорий" in caplog.text