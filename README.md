# Домашнее задание 4: Обработка банковских операций

## Описание
Модуль для фильтрации и сортировки банковских операций по статусу и дате.

## Установка
1. Клонируйте репозиторий.
2. Убедитесь, что установлен Python 3.8+.

## Использование
```python
from src.processing import filter_by_state, sort_by_date

data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

executed = filter_by_state(data)  # Только EXECUTED
sorted_data = sort_by_date(data)  # Сортировка по дате (новые сверху)