import sys
from collections.abc import Generator
from io import StringIO

from src.pipe import pipe
from src.support.structures import Print, to_value


def test_print_pipe():
    @pipe
    def greet() -> str:
        return "Hello, World!"

    captured_output = StringIO()
    sys.stdout = captured_output
    _ = greet >> Print
    assert captured_output.getvalue() == "Hello, World!\n"


def test_print_pipe_with_generator():
    @pipe
    def greet() -> Generator[str, None, None]:
        yield "Hello, World!"

    captured_output = StringIO()
    sys.stdout = captured_output
    _ = greet >> Print >> to_value
    assert captured_output.getvalue() == "Hello, World!\n"
