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


def test_set_pipe_with_mixed_types():
    @pipe
    def to_string(item: Any) -> str:
        return str(item)

    data = {2.5, True, None}
    result = data >> to_string >> Set.to_value
    assert all(item in {"2.5", "True", "None"} for item in result)
