from src.support.structures import Dict, List, Set, String, Tuple


def test_convert_dict_to_list():
    data = {"a": 1, "b": 2, "c": 3}
    result = data >> List.to_value
    assert result == ["a", "b", "c"]


def test_convert_dict_to_list_items():
    data = {"a": 1, "b": 2, "c": 3}.items()
    result = data >> List.to_value
    assert result == [("a", 1), ("b", 2), ("c", 3)]


def test_convert_list_to_dict():
    data = [("a", 1), ("b", 2), ("c", 3)]
    result = data >> Dict.to_value
    assert result == {"a": 1, "b": 2, "c": 3}


def test_convert_list_to_set():
    data = [1, 2, 2, 3, 4, 4, 5]
    result = data >> Set.to_value
    assert result == {1, 2, 3, 4, 5}


def test_convert_list_to_tuple():
    data = [1, 2, 3, 4, 5]
    result = data >> Tuple.to_value
    assert result == (1, 2, 3, 4, 5)


def test_convert_list_to_string():
    data = ["hello", "world"]
    result = data >> String.to_value
    assert result == "['hello', 'world']"


def test_convert_set_to_list():
    data = {1, 2, 3, 4, 5}
    result = data >> List.to_value
    assert result == [1, 2, 3, 4, 5]


def test_convert_tuple_to_list():
    data = (1, 2, 3, 4, 5)
    result = data >> List.to_value
    assert result == [1, 2, 3, 4, 5]


def test_convert_string_to_list():
    data = "hello"
    result = data >> List.to_value
    assert result == ["h", "e", "l", "l", "o"]
