"""
Модуль декораторов для логирования работы функций.
Предоставляет декоратор log для автоматического логирования вызовов функций.
"""

import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.

    Логирует начало и конец выполнения функции, а также результаты или ошибки.
    Если filename указан, логи записываются в файл, иначе выводятся в консоль.

    Аргументы:
        filename: Опциональное имя файла для записи логов.
                 Если None, логи выводятся в консоль.

    Возвращает:
        Декоратор для функции

    Пример использования:
        >>> @log(filename="app.log")
        ... def add(a, b):
        ...     return a + b

        >>> @log()
        ... def divide(a, b):
        ...     return a / b
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Получаем текущее время для лога
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                # Вызываем оригинальную функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успешном выполнении
                log_message = f"{current_time} {func_name} ok\n"

                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as error:
                # Формируем сообщение об ошибке
                error_message = (
                    f"{current_time} {func_name} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}\n"
                )

                # Записываем лог ошибки в файл или выводим в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(error_message)
                else:
                    print(error_message, end="")

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


# Примеры функций для демонстрации работы декоратора
@log()
def example_console_log(x: int, y: int) -> int:
    """
    Пример функции с логированием в консоль.

    Аргументы:
        x: Первое число
        y: Второе число

    Возвращает:
        Сумму двух чисел
    """
    return x + y


@log(filename="example.log")
def example_file_log(text: str) -> str:
    """
    Пример функции с логированием в файл.

    Аргументы:
        text: Текст для обработки

    Возвращает:
        Текст в верхнем регистре
    """
    return text.upper()


@log()
def example_error_function() -> None:
    """
    Пример функции, которая вызывает исключение.
    """
    raise ValueError("Пример ошибки")
