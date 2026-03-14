"""
Дополнительные тесты для модуля search.
Проверяет граничные случаи и обработку исключений.
"""

from unittest.mock import patch

import pytest

from src.search import (
    advanced_search_transactions,
    count_transactions_by_categories,
    search_transactions,
)


class TestSearchAdditional:
    """Дополнительные тесты для функций поиска."""

    @patch('src.search.re.compile')
    def test_search_transactions_compile_exception(self, mock_compile, sample_transactions):
        """Тест обработки исключения при компиляции regex в search_transactions."""
        mock_compile.side_effect = Exception("Test error")
        result = search_transactions(sample_transactions, "тест")
        assert result == []

    def test_search_transactions_with_none_transactions(self):
        """Тест с None вместо списка транзакций."""
        result = search_transactions(None, "тест")  # type: ignore
        assert result == []

    def test_search_transactions_with_none_search_string(self, sample_transactions):
        """Тест с None вместо строки поиска."""
        result = search_transactions(sample_transactions, None)  # type: ignore
        assert result == []

    def test_search_transactions_empty_transactions(self):
        """Тест с пустым списком транзакций."""
        result = search_transactions([], "тест")
        assert result == []

    def test_search_transactions_empty_search_string(self, sample_transactions):
        """Тест с пустой строкой поиска."""
        result = search_transactions(sample_transactions, "")
        assert result == []

    @patch('src.search.re.search')
    def test_count_categories_search_exception(self, mock_search, sample_transactions):
        """Тест обработки исключения в re.search при подсчете категорий."""
        mock_search.side_effect = Exception("Test error")
        result = count_transactions_by_categories(sample_transactions, ["тест"])
        assert result == {"тест": 0}

    def test_count_categories_with_none_transactions(self):
        """Тест с None вместо списка транзакций."""
        result = count_transactions_by_categories(None, ["тест"])  # type: ignore
        assert result == {"тест": 0}

    def test_count_categories_with_none_categories(self, sample_transactions):
        """Тест с None вместо списка категорий."""
        with pytest.raises(TypeError):
            count_transactions_by_categories(sample_transactions, None)

    def test_count_categories_empty_transactions(self):
        """Тест с пустым списком транзакций."""
        result = count_transactions_by_categories([], ["тест"])
        assert result == {"тест": 0}

    def test_count_categories_empty_categories(self, sample_transactions):
        """Тест с пустым списком категорий."""
        result = count_transactions_by_categories(sample_transactions, [])
        assert result == {}

    def test_count_categories_with_empty_descriptions(self):
        """Тест с пустыми описаниями транзакций."""
        transactions = [
            {"id": 1, "description": ""},
            {"id": 2},  # без description
            {"id": 3, "description": "тест"}
        ]
        result = count_transactions_by_categories(transactions, ["тест"])
        assert result["тест"] == 1

    @patch('src.search.re.compile')
    def test_advanced_search_re_error(self, mock_compile, sample_transactions):
        """Тест обработки ошибки регулярного выражения."""
        from re import error
        mock_compile.side_effect = error("Test regex error")
        result = advanced_search_transactions(sample_transactions, "[")
        assert result == []

    @patch('src.search.re.compile')
    def test_advanced_search_general_exception(self, mock_compile, sample_transactions):
        """Тест обработки общего исключения."""
        mock_compile.side_effect = Exception("Test error")
        result = advanced_search_transactions(sample_transactions, "тест")
        assert result == []

    def test_advanced_search_empty_pattern(self, sample_transactions):
        """Тест с пустым шаблоном."""
        result = advanced_search_transactions(sample_transactions, "")
        assert result == []

    def test_advanced_search_empty_transactions(self):
        """Тест с пустым списком транзакций."""
        result = advanced_search_transactions([], "тест")
        assert result == []

    def test_advanced_search_with_none_pattern(self, sample_transactions):
        """Тест с None вместо шаблона."""
        result = advanced_search_transactions(sample_transactions, None)  # type: ignore
        assert result == []

    def test_advanced_search_with_none_transactions(self):
        """Тест с None вместо списка транзакций."""
        result = advanced_search_transactions(None, "тест")  # type: ignore
        assert result == []
