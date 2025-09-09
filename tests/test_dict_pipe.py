from collections.abc import Generator

from src.pipe import pipe
from src.support.structures import Dict


def test_dict_pipe_simple():
    @pipe
    def increment_value(item: dict[str, int]) -> dict[str, int]:
        return {k: v + 1 for k, v in item.items()}

    data = {"a": 1, "b": 2, "c": 3}
    result = data >> increment_value >> Dict.to_value
    assert result == {"a": 2, "b": 3, "c": 4}


def test_dict_pipe_with_partial():
    @pipe
    def add_one(x: int) -> int:
        return x + 1

    @pipe
    def multiply_by_two(x: int) -> int:
        return x * 2

    result = 3 >> add_one >> multiply_by_two >> Dict.to_value
    assert result == {8: 8}


def test_dict_pipe_simple_with_generator():
    @pipe
    def increment_value(item: dict[str, int]) -> Generator[dict[str, int], None, None]:
        yield {k: v + 1 for k, v in item.items()}

    data = {"a": 1, "b": 2, "c": 3}
    result = dict(next(increment_value(data)))  # type: ignore
    print(result)
    result = data >> increment_value >> Dict.to_value
    assert result == {"a": 2, "b": 3, "c": 4}
