"""
Тесты для модуля decorators.
Проверяет корректность работы декоратора log.
"""

import os
import tempfile
import pytest
from src.decorators import log


@pytest.fixture
def temp_log_file():
    """
    Фикстура создает временный файл для тестирования логирования в файл.

    Возвращает:
        Путь к временному файлу
    """
    # Создаем временный файл
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
    temp_file.close()

    # Возвращаем путь к файлу для использования в тестах
    yield temp_file.name

    # Удаляем временный файл после выполнения теста
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def sample_function():
    """
    Фикстура возвращает простую функцию для тестирования.
    """

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    return add


@pytest.fixture
def error_function():
    """
    Фикстура возвращает функцию, которая вызывает исключение.
    """

    @log()
    def raise_error() -> None:
        raise ValueError("Тестовая ошибка")

    return raise_error


class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_to_console_success(self, capsys, sample_function):
        """
        Тест логирования успешного выполнения в консоль.

        Проверяет, что при успешном выполнении функции
        в консоль выводится корректное сообщение.
        """
        # Вызываем функцию
        result = sample_function(2, 3)

        # Проверяем результат
        assert result == 5

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()

        # Проверяем формат лог-сообщения
        assert "add ok" in captured.out
        assert "error" not in captured.out

    def test_log_to_console_error(self, capsys, error_function):
        """
        Тест логирования ошибки в консоль.

        Проверяет, что при возникновении ошибки
        в консоль выводится сообщение об ошибке.
        """
        try:
            error_function()
        except ValueError:
            pass  # Ожидаемое исключение

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()

        # Проверяем формат лог-сообщения об ошибке
        assert "raise_error error" in captured.out
        assert "ValueError" in captured.out
        assert "Inputs" in captured.out

    def test_log_to_file_success(self, temp_log_file):
        """
        Тест логирования успешного выполнения в файл.

        Проверяет, что при успешном выполнении функции
        лог записывается в указанный файл.
        """

        # Создаем функцию с логированием в файл
        @log(filename=temp_log_file)
        def multiply(x: int, y: int) -> int:
            return x * y

        # Вызываем функцию
        result = multiply(4, 5)

        # Проверяем результат
        assert result == 20

        # Читаем содержимое файла
        with open(temp_log_file, 'r', encoding='utf-8') as file:
            log_content = file.read()

        # Проверяем формат лог-сообщения
        assert "multiply ok" in log_content
        assert "error" not in log_content

    def test_log_to_file_error(self, temp_log_file):
        """
        Тест логирования ошибки в файл.

        Проверяет, что при возникновении ошибки
        лог ошибки записывается в указанный файл.
        """

        # Создаем функцию с логированием в файл, которая вызывает ошибку
        @log(filename=temp_log_file)
        def divide_by_zero() -> float:
            return 10 / 0

        try:
            divide_by_zero()
        except ZeroDivisionError:
            pass  # Ожидаемое исключение

        # Читаем содержимое файла
        with open(temp_log_file, 'r', encoding='utf-8') as file:
            log_content = file.read()

        # Проверяем формат лог-сообщения об ошибке
        assert "divide_by_zero error" in log_content
        assert "ZeroDivisionError" in log_content
        assert "Inputs" in log_content

    def test_function_arguments_preserved(self, sample_function):
        """
        Тест сохранения аргументов функции.

        Проверяет, что декоратор корректно передает
        аргументы в оригинальную функцию.
        """
        # Тестируем различные комбинации аргументов
        assert sample_function(0, 0) == 0
        assert sample_function(-1, 1) == 0
        assert sample_function(10, 20) == 30

    def test_function_return_value_preserved(self, sample_function):
        """
        Тест сохранения возвращаемого значения.

        Проверяет, что декоратор корректно возвращает
        результат оригинальной функции.
        """
        result = sample_function(7, 3)
        assert result == 10
        assert isinstance(result, int)

    def test_exception_propagation(self, error_function):
        """
        Тест пробрасывания исключений.

        Проверяет, что декоратор не подавляет исключения,
        а пробрасывает их дальше.
        """
        with pytest.raises(ValueError, match="Тестовая ошибка"):
            error_function()

    def test_multiple_calls_logging(self, temp_log_file):
        """
        Тест логирования множественных вызовов.

        Проверяет, что каждый вызов функции
        записывается в лог отдельной строкой.
        """

        @log(filename=temp_log_file)
        def counter() -> int:
            return 42

        # Вызываем функцию несколько раз
        for _ in range(3):
            counter()

        # Читаем содержимое файла
        with open(temp_log_file, 'r', encoding='utf-8') as file:
            log_lines = file.readlines()

        # Проверяем, что есть 3 записи в логе
        assert len(log_lines) == 3

        # Проверяем, что каждая запись содержит нужную информацию
        for line in log_lines:
            assert "counter ok" in line

    def test_log_with_keyword_arguments(self, capsys):
        """
        Тест логирования функций с keyword-аргументами.

        Проверяет, что декоратор корректно обрабатывает
        функции с именованными аргументами.
        """

        @log()
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        # Вызываем функцию с keyword-аргументами
        result = greet(name="Alice", greeting="Hi")

        # Проверяем результат
        assert result == "Hi, Alice!"

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        assert "greet ok" in captured.out

    def test_log_without_arguments(self, capsys):
        """
        Тест логирования функций без аргументов.

        Проверяет, что декоратор корректно обрабатывает
        функции без аргументов.
        """

        @log()
        def get_answer() -> int:
            return 42

        # Вызываем функцию без аргументов
        result = get_answer()

        # Проверяем результат
        assert result == 42

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        assert "get_answer ok" in captured.out


def test_decorator_import():
    """
    Тест корректности импорта декоратора.

    Проверяет, что декоратор можно импортировать
    и он является вызываемым объектом.
    """
    from src.decorators import log
    assert callable(log)

    # Проверяем, что декоратор возвращает функцию
    decorator = log()
    assert callable(decorator)


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_parametrized_success_cases(a, b, expected, capsys):
    """
    Параметризованный тест успешных случаев.

    Проверяет различные комбинации входных данных
    для функций с декоратором log.
    """

    @log()
    def parametrized_add(x: int, y: int) -> int:
        return x + y

    result = parametrized_add(a, b)
    assert result == expected

    # Проверяем лог
    captured = capsys.readouterr()
    assert "parametrized_add ok" in captured.out


@pytest.mark.parametrize("error_type", [
    ValueError,
    TypeError,
    ZeroDivisionError,
    RuntimeError,
])
def test_parametrized_error_cases(error_type, capsys):
    """
    Параметризованный тест случаев с ошибками.

    Проверяет различные типы исключений
    при использовании декоратора log.
    """

    @log()
    def raise_specific_error():
        raise error_type("Тестовое сообщение об ошибке")

    try:
        raise_specific_error()
    except error_type:
        pass  # Ожидаемое исключение

    # Проверяем лог ошибки
    captured = capsys.readouterr()
    assert "raise_specific_error error" in captured.out
    assert error_type.__name__ in captured.out
