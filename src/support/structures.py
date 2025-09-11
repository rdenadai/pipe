from collections.abc import Iterator, Sequence
from functools import partial
from typing import Any, Callable

from src.pipe import pipe
from src.support.utils import STRUCTURAL_TYPES, create_converter, from_generator, materialize

Parcial = lambda func, *args, **kwargs: pipe(partial(func, *args, **kwargs))
Print = pipe(print)


@materialize
def to_value(data: Any) -> Any:
    return from_generator(data)


class List:
    to_value = create_converter(list, lambda data: [data] if not isinstance(data, STRUCTURAL_TYPES) else list(data))


class Dict:
    to_value = create_converter(
        dict,
        lambda data: dict(data) if isinstance(data, (Sequence, Iterator)) else {data: data},
    )


class Set:
    to_value = create_converter(set)


class Tuple:
    to_value = create_converter(tuple, lambda data: (data,) if not isinstance(data, STRUCTURAL_TYPES) else tuple(data))


class String:
    @materialize
    @staticmethod
    def to_value(data: Any) -> str:
        return str(from_generator(data))

    @staticmethod
    def _proxy_str_method(method_name: str) -> Callable[..., Any]:
        @materialize
        def method(data: Any, *args: Any, **kwargs: Any) -> Any:
            s = str(from_generator(data))
            return getattr(s, method_name)(*args, **kwargs)

        return method

    upper = _proxy_str_method("upper")
    lower = _proxy_str_method("lower")
    capitalize = _proxy_str_method("capitalize")
    title = _proxy_str_method("title")
    strip = _proxy_str_method("strip")
    split = _proxy_str_method("split")
