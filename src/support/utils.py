from collections.abc import Callable, Generator, ItemsView, Iterator, Mapping, Sequence
from collections.abc import Set as _Set
from typing import Any, Optional, Type, TypeVar

from src.pipe import pipe

T = TypeVar("T")

BASIC_TYPES = (int, float, str, bool)
STRUCTURAL_TYPES = (Sequence, Iterator, Mapping, _Set, ItemsView)


def materialize(func: Callable[..., Any]) -> pipe:
    func._materialize = True  # type: ignore
    return pipe(func)


def from_generator(data: Any) -> Any:
    # data is a generator that could contain one single value or multiple values
    if isinstance(data, Generator):
        data = list(data)
        if len(data) == 1:
            return data[0]
        return data
    return data


def create_converter(target_type: Type[T], special_logic: Optional[Callable[[Any], T]] = None) -> Callable[[Any], T]:
    """Factory to create 'to_value' conversion methods."""

    @materialize
    def to_value(data: Any) -> T:
        data = from_generator(data)
        if isinstance(data, target_type):
            return data
        if special_logic:
            return special_logic(data)
        # We need special handling for strings to avoid converting them to a set of characters
        if not isinstance(data, STRUCTURAL_TYPES) or isinstance(data, BASIC_TYPES):
            return target_type([data])  # type: ignore
        return target_type(data)  # type: ignore

    return to_value


def proxy_str_method(method_name: str, sep: Optional[str] = None) -> Callable[..., Any]:
    @materialize
    def method(data: Any, *args: Any, **kwargs: Any) -> Any:
        data = from_generator(data)
        if isinstance(data, str):
            return getattr(data, method_name)(*args, **kwargs)
        elif isinstance(data, STRUCTURAL_TYPES):
            return [getattr(s, method_name)(*args, **kwargs) for s in data if isinstance(s, str)]
        return getattr(data, method_name)(*args, **kwargs)

    return method
