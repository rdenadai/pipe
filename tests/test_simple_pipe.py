from src.pipe import pipe
from src.support.structures import List


def test_simple_pipe():
    @pipe
    def add(x: int) -> int:
        return x + 1

    @pipe
    def multiply(x: int) -> int:
        return x * 2

    result = 3 >> add >> multiply
    assert result == 8


def test_simple_pipe_lambda():
    data = [1, 2, 3, 4, 5]

    add_one = pipe(lambda x: x + 1)
    multiply_by_two = pipe(lambda x: x * 2)

    result = data >> add_one >> multiply_by_two >> List.to_value
    assert result == [4, 6, 8, 10, 12]


def test_simple_pipe_with_string():
    @pipe
    def to_upper(s: str) -> str:
        return s.upper()

    @pipe
    def add_exclamation(s: str) -> str:
        return s + "!"

    result = "hello" >> to_upper >> add_exclamation
    assert result == "HELLO!"


def test_simple_pipe_with_list():
    @pipe
    def square(x: int) -> int:
        return x * x

    @pipe
    def increment(x: int) -> int:
        return x + 1

    numbers = [1, 2, 3]
    result = [n >> square >> increment for n in numbers]
    assert result == [2, 5, 10]


def test_simple_pipe_with_list_without_comprehension():
    @pipe
    def square(x: int) -> int:
        print("Squaring", x)
        return x * x

    @pipe
    def increment(x: int) -> int:
        print("Incrementing", x)
        return x + 1

    result = [1, 2, 3] >> square >> increment >> List.to_value
    assert result == [2, 5, 10]


def test_simple_pipe_with_no_arguments():
    @pipe
    def greet() -> str:
        return "Hello, World!"

    result = greet()
    assert result == "Hello, World!"


def test_simple_pipe_with_mixed_python_types():
    @pipe
    def square(x: int) -> int:
        return x * x

    result = list([1, 2, 3] >> square)
    assert result == [1, 4, 9]
