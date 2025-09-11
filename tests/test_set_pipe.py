from typing import Any

from src.pipe import pipe
from src.support.structures import Set


def test_set_pipe_simple():
    @pipe
    def increment_value(item: int) -> int:
        return item + 1

    data = {1, 2, 3}
    result = data >> increment_value >> Set.to_value
    assert result == {2, 3, 4}


def test_set_pipe_empty():
    @pipe
    def any_transformation(item: Any) -> Any:
        return item

    data = set()
    result = data >> any_transformation >> Set.to_value
    assert result == set()
    assert isinstance(result, set)


def test_set_pipe_with_mixed_types():
    @pipe
    def to_string(item: Any) -> str:
        return str(item)

    data = {2.5, True, None}
    result = data >> to_string >> Set.to_value
    assert all(item in {"2.5", "True", "None"} for item in result)
    assert len(result) == 3
    assert isinstance(result, set)


def test_set_pipe_function_with_multiple_arguments():
    data = {"fruits": (("apple", 5), ("banana", 3), ("cherry", 7)), "vegetables": (("carrot", 4), ("broccoli", 6))}

    @pipe
    def extract_names(item: dict[str, tuple[tuple[str, int], ...]]) -> set[str]:
        return {name for category in item.values() for name, _ in category}

    result = data >> extract_names >> Set.to_value
    assert result == {"apple", "banana", "cherry", "carrot", "broccoli"}
    assert isinstance(result, set)
