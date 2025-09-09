from collections.abc import ItemsView, Iterator, Mapping, Sequence
from collections.abc import Set as _Set
from functools import partial
from typing import Any

from src.pipe import pipe
from src.support.utils import from_generator, materialize

STRUCTURAL_TYPES = (Sequence, Iterator, Mapping, _Set, ItemsView)

Parcial = lambda func, *args, **kwargs: pipe(partial(func, *args, **kwargs))
Print = pipe(print)


@materialize
def to_value(data: Any) -> Any:
    return from_generator(data)


class List:
    @materialize
    @staticmethod
    def to_value(data: Any) -> list:
        if isinstance(data, list):
            return data
        elif not isinstance(data, STRUCTURAL_TYPES):
            return [data]
        return list(data)


class Dict:
    @materialize
    @staticmethod
    def to_value(data: Any) -> dict:
        data = from_generator(data)
        if isinstance(data, dict):
            return data
        elif isinstance(data, (Sequence, Iterator)):
            return dict(data)
        else:
            return {data: data}


class Set:
    @materialize
    @staticmethod
    def to_value(data: Any) -> set:
        if isinstance(data, set):
            return data
        elif not isinstance(data, STRUCTURAL_TYPES):
            return {data}
        return set(data)


class String:
    @materialize
    @staticmethod
    def to_value(data: Any) -> str:
        return str(from_generator(data))


class Tuple:
    @materialize
    @staticmethod
    def to_value(data: Any) -> tuple:
        if isinstance(data, tuple):
            return data
        elif not isinstance(data, STRUCTURAL_TYPES):
            return (data,)
        return tuple(data)
