import pytest
from typing import List, Dict, Any


@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с тестовыми номерами карт"""
    return [
        "7000792289606361",
        "7158300734726758",
        "6831982476737658",
        "8990922113665229",
        "5999414228426353",
    ]


@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с тестовыми номерами счетов"""
    return [
        "64686473678894779589",
        "35383033474447895560",
        "73654108430135874305",
    ]


@pytest.fixture
def sample_dates() -> List[str]:
    """Фикстура с тестовыми датами"""
    return [
        "2024-03-14T10:30:00.000",
        "2023-12-01T15:45:30.123",
        "2022-08-20T08:00:00.000",
    ]


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-14T10:30:00.000",
            "amount": "100.00",
            "currency": "USD",
            "description": "Transaction 1",
            "from": "Visa 7000792289606361",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 2,
            "state": "PENDING",
            "date": "2024-02-01T15:45:30.123",
            "amount": "200.50",
            "currency": "EUR",
            "description": "Transaction 2",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-12-25T08:00:00.000",
            "amount": "50.75",
            "currency": "RUB",
            "description": "Transaction 3",
            "from": "Maestro 6831982476737658",
            "to": "Счет 73654108430135874305"
        },
        {
            "id": 4,
            "state": "CANCELED",
            "date": "2023-11-10T12:00:00.000",
            "amount": "300.00",
            "currency": "USD",
            "description": "Transaction 4",
        },
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2023-10-05T09:15:45.000",
            "amount": "150.25",
            "currency": "EUR",
            "description": "Transaction 5",
        }
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций"""
    return []