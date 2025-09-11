from collections.abc import Iterator, Sequence
from functools import partial
from typing import Any

from src.pipe import pipe
from src.support.utils import STRUCTURAL_TYPES, create_converter, from_generator, materialize, proxy_str_method

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

    upper = proxy_str_method("upper")
    lower = proxy_str_method("lower")
    capitalize = proxy_str_method("capitalize")
    title = proxy_str_method("title")
    strip = proxy_str_method("strip")
    split = proxy_str_method("split")
