"""
Тесты для модуля generators.
Проверяет корректность работы функций-генераторов для обработки транзакций.
"""

import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    """Фикстура предоставляет пример данных транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 3
        for transaction in usd_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_rub_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 2
        for transaction in rub_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "RUB"

    @pytest.mark.parametrize("currency_code,expected_count", [
        ("USD", 3),  # Должно найти 3 транзакции в USD
        ("RUB", 2),  # Должно найти 2 транзакции в RUB
        ("EUR", 0),  # Не должно найти транзакций в EUR
    ])
    def test_filter_parametrized(self, sample_transactions, currency_code, expected_count):
        """Параметризованный тест для фильтрации по разным валютам."""
        transactions = list(filter_by_currency(sample_transactions, currency_code))
        assert len(transactions) == expected_count


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_descriptions_generation(self, sample_transactions):
        """Тест генерации описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]
        assert descriptions == expected_descriptions


class TestCardNumberGenerator:
    """Тесты для функции card_number_generator."""

    @pytest.mark.parametrize("start,stop,expected_output", [
        (1, 5, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]),
        (1234, 1234, ["0000 0000 0000 1234"]),
    ])
    def test_card_number_generation(self, start, stop, expected_output):
        """Параметризованный тест генерации номеров карт."""
        generated_numbers = list(card_number_generator(start, stop))
        assert generated_numbers == expected_output