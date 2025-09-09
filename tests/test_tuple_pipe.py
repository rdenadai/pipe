from collections.abc import Generator

from src.pipe import pipe
from src.support.structures import Tuple


def test_tuple_pipe_simple():
    @pipe
    def increment_value(item: int) -> int:
        return item + 1

    data = (1, 2, 3)
    result = data >> increment_value >> Tuple.to_value
    assert result == (2, 3, 4)


def test_tuple_pipe_with_mixed_types():
    @pipe
    def to_string(item: str) -> str:
        return str(item)

    data = (2.5, True, None)
    result = data >> to_string >> Tuple.to_value
    assert all(item in ("2.5", "True", "None") for item in result)


def test_tuple_pipe_with_generator():
    @pipe
    def increment_value(item: int) -> Generator[int, None, None]:
        yield item + 1

    data = (1, 2, 3)
    result = data >> increment_value >> Tuple.to_value
    assert result == (2, 3, 4)


def test_tuple_pipe_with_partial():
    @pipe
    def add_one(x: int) -> int:
        return x + 1

    @pipe
    def multiply_by_two(x: int) -> int:
        return x * 2

    result = 3 >> add_one >> multiply_by_two >> Tuple.to_value
    assert result == (8,)
