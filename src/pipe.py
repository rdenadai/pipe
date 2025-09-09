from __future__ import annotations

from collections import deque
from collections.abc import Callable, Generator, Iterator, Mapping, Sequence, Set
from functools import partial
from typing import Any


class pipe:
    __slots__ = ("_func", "_name", "_is_reduce", "_reduce_final")

    def __init__(self, func: Callable[..., Any]) -> None:
        self._func = func
        self._name = func.__name__ if hasattr(func, "__name__") else func.__class__.__name__

    def __rshift__(self, other: Any) -> Any:
        result = self._func
        if callable(result) and not isinstance(result, (pipe, partial)):
            result = result()
        return self.__execute__(other._func, result)  # type: ignore[union-attr]

    def __rrshift__(self, other: Any) -> Generator[Any, None, None] | Any:
        return self.__execute__(self._func, other)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._func(*args, **kwargs)

    @staticmethod
    def filter(predicate: Callable[..., bool]) -> pipe:
        def __filter(data: Any) -> Generator[Any, None, None]:
            result = predicate(data)
            if isinstance(result, Generator):
                result = next(result)
            if result:
                yield data

        return pipe(__filter)

    @staticmethod
    def reduce(
        func: Callable[..., Any] | None = None,
        *,
        initializer: Any = None,
    ) -> Callable[[Callable[..., Any]], pipe]:
        _initializer = initializer

        def __reduce_dec(func: Callable[..., Any]) -> pipe:
            def __reduce(data: Any) -> Any:
                nonlocal _initializer
                if _initializer is None:
                    _initializer = data
                    yield data
                else:
                    result = func(_initializer, data)
                    _initializer = next(result) if isinstance(result, Generator) else result
                    yield _initializer

            __reduce.__is_reduce__ = True  # type: ignore[attr-defined]
            return pipe(__reduce)

        if func is not None:
            return __reduce_dec(func)
        return __reduce_dec

    def __execute__(self, func: Callable[..., Any], other: Any) -> Any:
        if (
            (isinstance(other, (Iterator, Sequence)) and self.__not_str_bytes(other))
            or isinstance(other, Mapping)
            or isinstance(other, Set)
        ) and not hasattr(func, "_materialize"):
            return self.__stream__(func, other)
        return func(other)

    def __stream__(self, func: Callable[..., Any], other: Any) -> Generator[Any, None, None]:
        def __generator_result(func: Callable[..., Any], item: Any) -> Generator[Any, None, None]:
            result = func(item)
            if isinstance(result, Generator):
                yield from result
            else:
                yield result

        if isinstance(other, Mapping):
            yield from __generator_result(func, other)
        elif getattr(func, "__is_reduce__", False):
            yield deque((next(__generator_result(func, item)) for item in other), maxlen=1).pop()
        else:
            for item in other:
                yield from __generator_result(func, item)

    def __not_str_bytes(self, item: Any) -> bool:
        return not isinstance(item, (str, bytes, bytearray))
