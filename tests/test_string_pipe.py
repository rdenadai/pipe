from src.support.structures import List, Set, String, Tuple


def test_simple_string_pipe():
    data = ["apple", "banana", "cherry"]
    result = data >> String.upper >> List.to_value
    assert result == ["APPLE", "BANANA", "CHERRY"]


def test_simple_string_pipe_to_lower():
    data = ["APPLE", "BANANA", "CHERRY"]
    result = data >> String.lower >> Set.to_value
    assert result == {"apple", "banana", "cherry"}


def test_simple_string_pipe_capitalize():
    data = ["apple", "banana", "cherry"]
    result = data >> String.capitalize >> Tuple.to_value
    assert result == ("Apple", "Banana", "Cherry")


def test_complex_string_pipe():
    data = ["  hello world  ", "  python programming  "]
    result = data >> String.strip >> String.title >> List.to_value
    assert result == ["Hello World", "Python Programming"]


def test_multistep_string_pipe():
    data = ["  hello world  ", "  python programming  "]
    result = data >> String.strip >> String.upper >> String.split >> List.to_value
    assert result == [["HELLO", "WORLD"], ["PYTHON", "PROGRAMMING"]]
