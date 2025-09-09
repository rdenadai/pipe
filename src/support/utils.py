from collections.abc import Callable, Generator
from typing import Any

from src.pipe import pipe


def materialize(func: Callable[..., Any]) -> pipe:
    func._materialize = True  # type: ignore
    return pipe(func)


def from_generator(data: Any) -> Any:
    return next(data) if isinstance(data, Generator) else data
