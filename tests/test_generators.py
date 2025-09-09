import random

from src.pipe import pipe
from src.support.structures import List, to_value


def test_generator_shopping_cart_big_pipeline():
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
    cart.add_product(Product("Mouse", 25.50))
    cart.add_product(Product("Keyboard", 45.00))
    cart.add_product(Product("Monitor", 150.75))

    @pipe
    def apply_discount(product: Product) -> Product:
        product.price *= 0.9  # Apply a 10% discount
        yield product

    @pipe.filter
    def filter_expensive_products(product: Product) -> bool:
        yield product.price > 50

    @pipe.reduce(initializer=0.0)
    def sum_prices(x: float, y: Product) -> float:
        yield x + y.price

    discounts = cart.products >> apply_discount >> List.to_value
    assert all(
        abs(p.price - original_price * 0.9) < 1e-2
        for p, original_price in zip(discounts, [999.99, 25.50, 45.00, 150.75])
    )

    filtered_expensive = cart.products >> apply_discount >> filter_expensive_products >> List.to_value
    assert len(filtered_expensive) == 2  # Laptop and Monitor
    assert all(p.price > 50 for p in filtered_expensive)

    total = cart.products >> apply_discount >> filter_expensive_products >> sum_prices >> to_value

    assert round(total, 2) - 838.88  # Total price after discount for Laptop and Monitor


def test_random_number_generator():
    @pipe
    def random_number(N: int) -> int:
        yield random.randint(1, 100)

    numbers = range(5) >> random_number >> List.to_value
    assert len(numbers) == 5
    assert all(1 <= num <= 100 for num in numbers)
    # [69, 34, 2, 17, 90]  # Example output, will vary each run
