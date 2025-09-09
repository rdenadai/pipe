from src.pipe import pipe
from src.support.structures import List, Set


def test_big_pipeline():
    data = [
        (1, "apple"),
        (2, "banana"),
        (3, "cherry"),
        (4, "date"),
        (5, "elderberry"),
        (6, "fig"),
        (7, "grape"),
        (8, "honeydew"),
        (9, "kiwi"),
        (10, "lemon"),
        (11, "mango"),
        (12, "nectarine"),
        (13, "orange"),
        (14, "papaya"),
        (15, "quince"),
        (16, "raspberry"),
        (17, "strawberry"),
        (18, "tangerine"),
    ]

    @pipe.filter
    def filter_even_ids(item: tuple[int, str]) -> bool:
        return item[0] % 2 == 0

    @pipe
    def extract_fruit_name(item: tuple[int, str]) -> str:
        return item[1]

    @pipe
    def to_uppercase(item: str) -> str:
        return item.upper()

    @pipe
    def append_exclamation(item: str) -> str:
        return f"{item}!"

    @pipe.reduce(initializer="")
    def concatenate(acc: str, item: str) -> str:
        print(f"Acc: {acc} | Item: {item}")
        return acc + item + " "

    result = (
        data
        >> filter_even_ids
        >> extract_fruit_name
        >> to_uppercase
        >> append_exclamation
        >> List.to_value
        >> concatenate
        >> pipe(str.strip)
        >> Set.to_value
    )

    assert result == {"BANANA! DATE! FIG! HONEYDEW! LEMON! NECTARINE! PAPAYA! RASPBERRY! TANGERINE!"}
    assert isinstance(result, set)
