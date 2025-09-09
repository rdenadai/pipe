# pipe ( >> )

A Python library for creating elegant, lazy-evaluated data processing pipelines using a functional approach.

## Description

pipe allows you to chain operations on data in a highly readable and efficient manner, inspired by shell pipes and functional programming concepts. It uses the right-shift operator >> to pass data through a series of transformations.

The library is built around lazy evaluation. When you pipe an iterable (like a list, tuple, or generator) through a series of operations, the computations are performed one item at a time, which is highly memory-efficient for large datasets.

## Installation

To install the project and its development dependencies, clone the repository and run the following command in the project's root directory:

```bash
pip install -e .[dev]
```

## Core Concepts

- **pipe object**: A wrapper around a function that makes it "pipe-able".

- **>> operator**: The core of the library. It is used to chain operations, passing the output of the left-hand side as the input to the right-hand side.

- **Lazy Evaluation**: For iterables, operations are not executed immediately on the entire collection. Instead, they are processed as a stream, one element at a time. This means you can process data collections that are larger than your available memory.

- **Materialization**: The process of consuming the entire lazy stream to produce a concrete final result, such as a list, set, or a single value. Functions decorated with @materialize will consume the stream.

## Usage

### Basic Pipelining

You can chain multiple operations together. The data flows from left to right.

```python
from src.pipe import pipe
from src.support.structures import List

add_one = pipe(lambda x: x + 1)
multiply_by_two = pipe(lambda x: x * 2)

data = [1, 2, 3, 4, 5]
result = data >> add_one >> multiply_by_two >> List.to_value
print(result)
# Output: [4, 6, 8, 10, 12]
```

### Filtering

Use pipe.filter to select items from an iterable that satisfy a condition.

```python
from src.pipe import pipe
from src.support.structures import List

@pipe.filter
def is_even(x: int) -> bool:
    return x % 2 == 0

data = range(10)
result = data >> is_even >> List.to_value
print(result)
# Output: [0, 2, 4, 6, 8]
```

### Reducing

Use pipe.reduce to apply a function cumulatively to the items of a sequence, reducing the sequence to a single value.

```python
from src.pipe import pipe
from src.support.structures import to_value

add = lambda x, y: x + y

data = [1, 2, 3, 4]
# The result of the final reduction is the output
result = data >> pipe.reduce(add) >> to_value
print(result)
# Output: 10
```

> You can also provide an initializer value.

### Materializing to Data Structures

The pipeline remains a lazy generator until it's "materialized". The src.support.structures module provides helpers to convert the final stream into common data structures.

```python
from src.pipe import pipe
from src.support.structures import Dict, List, Set, String, Tuple

data = [("a", 1), ("b", 2), ("a", 1)]

# To List
list_result = data >> List.to_value
print(f"List: {list_result}")
# Output: List: [('a', 1), ('b', 2), ('a', 1)]

# To Tuple
tuple_result = data >> Tuple.to_value
print(f"Tuple: {tuple_result}")
# Output: Tuple: (('a', 1), ('b', 2), ('a', 1))

# To Set (duplicates are removed)
set_result = data >> Set.to_value
print(f"Set: {set_result}")
# Output: Set: {('a', 1), ('b', 2)}

# To Dict (duplicates are overridden)
dict_result = data >> Dict.to_value
print(f"Dict: {dict_result}")
# Output: Dict: {'a': 1, 'b': 2}

# To String
string_result = "hello" >> String.to_value
print(f"String: {string_result}")
# Output: String: hello
```

### Using Partial Functions

The Parcial helper allows you to create partial functions within a pipeline, fixing some arguments of a function.

```python
from src.pipe import pipe
from src.support.structures import List, Parcial

def power(exponent: int, x: int) -> int:
    return x**exponent

square = Parcial(power, 2)

data = [1, 2, 3, 4]
result = data >> square >> List.to_value
assert result == [1, 4, 9, 16]
print(result)
# Output: [1, 4, 9, 16]
```
