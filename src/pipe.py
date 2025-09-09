from __future__ import annotations

from collections import deque
from collections.abc import Callable, Generator, Iterator, Mapping, Sequence, Set
from functools import partial
from typing import Any


class pipe:
    def __init__(self, func: Callable[..., Any]) -> None:
        self._func = func
        self._name = func.__name__ if hasattr(func, "__name__") else func.__class__.__name__

    def __rshift__(self, other: Any) -> Any:
        result = self._func
        if callable(result) and not isinstance(result, (pipe, partial)):
            result = result()
        self._func = other._func
        self._name = other._name
        return self.__rrshift__(result)

    def __rrshift__(self, other: Any) -> Generator[Any, None, None] | Any:
        if (
            (isinstance(other, (Iterator, Sequence)) and self.__not_str_bytes(other))
            or isinstance(other, Mapping)
            or isinstance(other, Set)
        ) and not hasattr(self._func, "_materialize"):
            return self.__stream__(other)
        return self._func(other)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._func(*args, **kwargs)

    @staticmethod
    def filter(func: Callable[..., bool]) -> pipe:
        def __filter(data: Any) -> Generator[Any, None, None]:
            result = func(data)
            result = next(result) if isinstance(result, Generator) else result
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

            return pipe(__reduce)

        if func is not None:
            return __reduce_dec(func)
        return __reduce_dec

    def __stream__(self, other: Any) -> Generator[Any, None, None]:
        def __generator_result(item: Any) -> Generator[Any, None, None]:
            result = self._func(item)
            if isinstance(result, Generator):
                yield from result
            else:
                yield result

        if isinstance(other, Mapping):
            yield from __generator_result(other)
        elif getattr(self._func, "__name__", None) == "__reduce":
            yield deque((next(__generator_result(item)) for item in other), maxlen=1).pop()
        else:
            for item in other:
                yield from __generator_result(item)

    def __not_str_bytes(self, item: Any) -> bool:
        return not isinstance(item, (str, bytes, bytearray))
