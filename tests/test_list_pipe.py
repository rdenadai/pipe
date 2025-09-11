from collections.abc import Generator
from math import sqrt

from src.pipe import pipe
from src.support.structures import List, Parcial


def test_list_pipe_parcial_basic():
    def power(exponent: int, x: int) -> int:
        return x**exponent

    square = Parcial(power, 2)

    data = [1, 2, 3, 4]
    result = data >> square >> List.to_value
    assert result == [1, 4, 9, 16]


def test_list_pipe():
    @pipe
    def add(x: int) -> int:
        return x + 1

    result = [1, 2, 3] >> add >> List.to_value
    assert result == [2, 3, 4]


def test_list_pipe_with_multiple_functions():
    @pipe
    def add(x: int) -> int:
        return x + 1

    @pipe
    def multiply(x: int) -> int:
        return x * 2

    result = (1, 2, 3) >> add >> multiply >> List.to_value
    assert result == [4, 6, 8]


def test_list_pipe_with_strings():
    @pipe
    def to_upper(s: str) -> str:
        return s.upper()

    result = ["hello", "world"] >> to_upper >> List.to_value
    assert result == ["HELLO", "WORLD"]


def test_list_pipe_with_generator():
    @pipe
    def square(x: int) -> Generator[int, None, None]:
        yield x * x

    @pipe
    def root(x: int) -> Generator[float, None, None]:
        yield sqrt(x)

    result = (1, 2, 3) >> square >> root >> List.to_value
    assert result == [1.0, 2.0, 3.0]


def test_list_pipe_with_starting_generator():
    @pipe
    def generate_numbers() -> Generator[int, None, None]:
        for i in range(1, 4):
            yield i

    @pipe
    def square(x: int) -> Generator[int, None, None]:
        print("Squaring", x)
        yield x * x

    @pipe
    def root(x: int) -> Generator[float, None, None]:
        print("Rooting", x)
        yield sqrt(x)

    result = (i for i in range(1, 4)) >> square >> root >> List.to_value
    assert result == [1.0, 2.0, 3.0]

    result = generate_numbers >> square >> root >> List.to_value
    assert result == [1.0, 2.0, 3.0]


def test_list_pipe_with_function_returning_list():
    @pipe
    def items() -> list[int]:
        return [1, 2, 3, 4]

    @pipe
    def add_one(x: int) -> int:
        return x + 1

    result = items >> add_one >> List.to_value
    assert result == [2, 3, 4, 5]


def test_list_pipe_with_range():
    @pipe
    def add_one(x: int) -> int:
        return x + 1

    result = range(5) >> add_one >> List.to_value
    assert result == [1, 2, 3, 4, 5]


def test_list_pipe_partial_function():
    @pipe
    def multiply(x: int, factor: int) -> int:
        return x * factor

    multiply_by_3 = Parcial(multiply, factor=3)

    result = 3 >> multiply_by_3 >> List.to_value
    assert result == [9]


def test_list_pipe_function_with_multiple_arguments():
    data = {"fruits": (("apple", 5), ("banana", 3), ("cherry", 7)), "vegetables": (("carrot", 4), ("broccoli", 6))}

    @pipe
    def extract_names(item: dict[str, tuple[tuple[str, int], ...]]) -> list[str]:
        return list((name for category in item.values() for name, _ in category))

    result = data >> extract_names >> List.to_value
    assert result == ["apple", "banana", "cherry", "carrot", "broccoli"]
    assert isinstance(result, list)
