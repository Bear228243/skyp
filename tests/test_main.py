"""
Тесты для модуля main.py.
Проверяет работу основного приложения и пользовательского интерфейса.
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
import os
import tempfile
import json
from src.main import TransactionApp, main


@pytest.fixture
def app():
    """Фикстура для создания экземпляра приложения."""
    return TransactionApp()


@pytest.fixture
def temp_json_file():
    """Создает временный JSON файл для тестирования."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump([
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2024-01-01T10:00:00",
                "operationAmount": {
                    "amount": "1000",
                    "currency": {"code": "RUB", "name": "руб."}
                },
                "description": "Перевод организации",
                "from": "Visa 7000792289606361",
                "to": "Счет 64686473678894779589"
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "date": "2024-01-02T11:00:00",
                "operationAmount": {
                    "amount": "50",
                    "currency": {"code": "USD", "name": "USD"}
                },
                "description": "Перевод со счета на счет",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560"
            },
            {
                "id": 3,
                "state": "PENDING",
                "date": "2024-01-03T12:00:00",
                "operationAmount": {
                    "amount": "200",
                    "currency": {"code": "EUR", "name": "EUR"}
                },
                "description": "Перевод с карты на карту",
                "from": "Maestro 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            }
        ], f)
        f.close()
        yield f.name
        os.unlink(f.name)


class TestTransactionApp:
    """Тесты для класса TransactionApp."""

    def test_init(self, app):
        """Тест инициализации приложения."""
        assert app.transactions == []
        assert app.filtered_transactions == []
        assert app.current_file_type is None
        assert app.VALID_STATUSES == ["EXECUTED", "CANCELED", "PENDING"]

    def test_print_header(self, app, capsys):
        """Тест вывода заголовка."""
        app.print_header("Тестовый заголовок")
        captured = capsys.readouterr()
        assert "Тестовый заголовок" in captured.out
        assert "=" * 60 in captured.out

    def test_print_menu(self, app, capsys):
        """Тест вывода меню."""
        app.print_menu()
        captured = capsys.readouterr()
        assert "Выберите необходимый пункт меню:" in captured.out
        assert "1. Получить информацию о транзакциях из JSON-файла" in captured.out
        assert "2. Получить информацию о транзакциях из CSV-файла" in captured.out
        assert "3. Получить информацию о транзакциях из XLSX-файла" in captured.out
        assert "0. Выход" in captured.out

    @patch('builtins.input', return_value='')
    def test_get_file_path_default(self, mock_input, app, temp_json_file):
        """Тест получения пути к файлу по умолчанию."""
        with patch('os.path.exists', return_value=True):
            path = app.get_file_path('json')
            assert path is not None

    @patch('builtins.input', return_value='custom_path.json')
    def test_get_file_path_custom(self, mock_input, app):
        """Тест получения пользовательского пути к файлу."""
        with patch('os.path.exists', return_value=True):
            path = app.get_file_path('json')
            assert path == 'custom_path.json'

    @patch('builtins.input', return_value='')
    def test_get_file_path_not_found(self, mock_input, app):
        """Тест получения пути к несуществующему файлу."""
        with patch('os.path.exists', return_value=False):
            path = app.get_file_path('json')
            assert path is None

    @patch('src.main.load_transactions_from_file')
    def test_load_transactions_success(self, mock_load, app, temp_json_file):
        """Тест успешной загрузки транзакций."""
        mock_load.return_value = [{"id": 1}, {"id": 2}]

        with patch('os.path.exists', return_value=True):
            with patch('builtins.input', return_value=temp_json_file):
                result = app.load_transactions('json')

        assert result is True
        assert len(app.transactions) == 2
        assert app.current_file_type == 'json'

    @patch('src.main.load_transactions_from_file', return_value=[])
    def test_load_transactions_empty(self, mock_load, app):
        """Тест загрузки пустого файла."""
        with patch('os.path.exists', return_value=True):
            with patch('builtins.input', return_value='test.json'):
                result = app.load_transactions('json')

        assert result is False

    def test_get_status_filter_valid(self, app):
        """Тест получения корректного статуса."""
        with patch('builtins.input', side_effect=['EXECUTED']):
            status = app.get_status_filter()
            assert status == 'EXECUTED'

    def test_get_status_filter_invalid_then_valid(self, app):
        """Тест получения статуса после неверного ввода."""
        with patch('builtins.input', side_effect=['INVALID', 'EXECUTED']):
            status = app.get_status_filter()
            assert status == 'EXECUTED'

    def test_get_status_filter_exit(self, app):
        """Тест выхода из фильтрации."""
        with patch('builtins.input', return_value='0'):
            status = app.get_status_filter()
            assert status is None

    @pytest.mark.parametrize("input_value,expected", [
        ('да', True),
        ('Да', True),
        ('yes', True),
        ('Y', True),
        ('нет', False),
        ('Нет', False),
        ('no', False),
        ('N', False),
    ])
    def test_get_yes_no(self, app, input_value, expected):
        """Параметризованный тест ответов Да/Нет."""
        with patch('builtins.input', return_value=input_value):
            result = app.get_yes_no("Тестовый вопрос?")
            assert result == expected

    def test_get_sort_order_ascending(self, app):
        """Тест получения сортировки по возрастанию."""
        with patch('builtins.input', side_effect=['возрастание']):
            order = app.get_sort_order()
            assert order == 'asc'

    def test_get_sort_order_descending(self, app):
        """Тест получения сортировки по убыванию."""
        with patch('builtins.input', side_effect=['убывание']):
            order = app.get_sort_order()
            assert order == 'desc'

    def test_get_sort_order_exit(self, app):
        """Тест отмены сортировки."""
        with patch('builtins.input', return_value='0'):
            order = app.get_sort_order()
            assert order is None

    def test_get_search_string_with_input(self, app):
        """Тест получения строки поиска."""
        with patch('builtins.input', return_value='тест'):
            search = app.get_search_string()
            assert search == 'тест'

    def test_get_search_string_empty(self, app):
        """Тест пропуска поиска."""
        with patch('builtins.input', return_value=''):
            search = app.get_search_string()
            assert search is None

    @patch('src.main.filter_by_state')
    def test_apply_filters_basic(self, mock_filter, app, temp_json_file):
        """Тест применения базовых фильтров."""
        app.transactions = [{"id": 1}, {"id": 2}]
        mock_filter.return_value = app.transactions

        with patch('builtins.input', side_effect=['EXECUTED']):
            with patch.object(app, 'get_yes_no', return_value=False):
                result = app.apply_filters()

        assert len(result) == 2

    def test_display_transactions_with_data(self, app, capsys):
        """Тест отображения транзакций."""
        transactions = [
            {
                "id": 1,
                "date": "2024-01-01T10:00:00",
                "description": "Тестовая транзакция",
                "operationAmount": {
                    "amount": "1000",
                    "currency": {"code": "RUB", "name": "руб."}
                }
            }
        ]

        app.display_transactions(transactions)
        captured = capsys.readouterr()
        assert "ВСЕГО БАНКОВСКИХ ОПЕРАЦИЙ В ВЫБОРКЕ: 1" in captured.out

    def test_display_transactions_empty(self, app, capsys):
        """Тест отображения пустого списка."""
        app.display_transactions([])
        captured = capsys.readouterr()
        assert "Не найдено ни одной транзакции" in captured.out

    @patch('builtins.input', side_effect=['0'])
    def test_run_exit(self, mock_input, app, capsys):
        """Тест выхода из приложения."""
        app.run()
        captured = capsys.readouterr()
        assert "До свидания!" in captured.out

    @patch('builtins.input', side_effect=['invalid', '0'])
    def test_run_invalid_choice(self, mock_input, app, capsys):
        """Тест неверного выбора в меню."""
        app.run()
        captured = capsys.readouterr()
        assert "Неверный выбор" in captured.out

    def test_main_function(self):
        """Тест функции main."""
        with patch('src.main.TransactionApp.run') as mock_run:
            main()
            mock_run.assert_called_once()
