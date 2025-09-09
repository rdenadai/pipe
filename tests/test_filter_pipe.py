from src.pipe import pipe
from src.support.structures import List


def test_filter_basic():
    data = range(10)

    @pipe.filter
    def is_even(x: int) -> bool:
        return x % 2 == 0

    result = data >> is_even >> List.to_value
    assert result == [0, 2, 4, 6, 8]


def test_filter_strings():
    @pipe.filter
    def is_long_string(s: str) -> bool:
        return len(s) > 3

    data = ["hi", "hello", "hey", "greetings"]
    result = data >> is_long_string >> List.to_value
    assert result == ["hello", "greetings"]


def test_filter_numbers():
    @pipe.filter
    def is_even(n: int) -> bool:
        return n % 2 == 0

    data = [1, 2, 3, 4, 5, 6]
    result = data >> is_even >> List.to_value
    assert result == [2, 4, 6]


def test_filter_objects():
    class Person:
        __slots__ = ("name", "age")

        def __init__(self, name: str, age: int) -> None:
            self.name = name
            self.age = age

    @pipe.filter
    def is_adult(person: Person) -> bool:
        return person.age >= 18

    data = [Person("Alice", 17), Person("Bob", 20), Person("Charlie", 15), Person("David", 22)]
    result = data >> is_adult >> List.to_value
    assert [person.name for person in result] == ["Bob", "David"]


def test_filter_huge_data():
    @pipe.filter
    def is_multiple_of_five(n: int) -> bool:
        return n % 5 == 0

    data = range(1, 10001)  # Numbers from 1 to 10,000
    result = data >> is_multiple_of_five >> List.to_value
    assert result == [i for i in range(1, 10001) if i % 5 == 0]
