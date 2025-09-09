from src.pipe import pipe
from src.support.structures import to_value


def test_reduce_basic():
    add = lambda x, y: x + y

    data = [1, 2, 3, 4]
    result = data >> pipe.reduce(add) >> to_value
    assert result == 10  # 1 + 2 + 3 + 4 = 10


def test_reduce_numbers():
    @pipe.reduce
    def sum_numbers(x: int, y: int) -> int:
        return x + y

    data = [1, 2, 3, 4, 5]
    result = data >> sum_numbers >> to_value
    assert result == 15


def test_reduce_strings():
    @pipe.reduce
    def concat_strings(x: str, y: str) -> str:
        return x + y

    data = ["Hello, ", "world", "!"]
    result = data >> concat_strings >> to_value
    assert result == "Hello, world!"


def test_reduce_with_initializer():
    @pipe.reduce(initializer=10)
    def multiply(x: int, y: int) -> int:
        return x * y

    data = [1, 2, 3, 4]
    result = data >> multiply >> to_value
    assert result == 240  # 10 * 1 * 2 * 3 * 4 = 240


def test_reduce_big_data():
    @pipe.reduce
    def sum_numbers(x: int, y: int) -> int:
        return x + y

    data = range(1, 10001)  # Sum of first 10,000 natural numbers
    result = data >> sum_numbers >> to_value
    assert result == 50005000  # (10000 * (10000 + 1)) / 2 = 50005000


def test_reduce_sum_of_shopping_cart():
    class Product:
        __slots__ = ("name", "price")

        def __init__(self, name: str, price: float) -> None:
            self.name = name
            self.price = price

    class ShoppingCart:
        def __init__(self) -> None:
            self.products = []

        def add_product(self, product: Product) -> None:
            self.products.append(product)

    cart = ShoppingCart()
    cart.add_product(Product("Laptop", 999.99))
    cart.add_product(Product("Mouse", 49.99))
    cart.add_product(Product("Keyboard", 79.99))
    cart.add_product(Product("Monitor", 199.99))
    cart.add_product(Product("USB Cable", 9.99))

    @pipe.reduce(initializer=0.0)
    def sum_prices(total: float, product: Product) -> float:
        return total + product.price

    total_price = cart.products >> sum_prices >> to_value
    assert total_price == 1339.95  # 999.99 + 49.99 + 79.99 + 199.99 + 9.99 = 133
