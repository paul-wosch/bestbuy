"""Provide the Store class."""
from products import Product


class Store:
    """Manage a collection of products and enable bulk purchases."""
    def __init__(self, product_list):
        """Initialize a store instance."""
        self.product_list = product_list

    def add_product(self, product):
        """Add a product to the store."""
        self.product_list.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.product_list.remove(product)

    def get_total_quantity(self) -> int:
        """Return the total amount of items in the store."""
        return sum([item.quantity for item in self.product_list])

    def get_all_products(self) -> list[Product]:
        """Returns all products in the store with an active state."""
        return [item for item in self.product_list if item.is_active()]

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """Buy the given products and return total price for order."""
        total_price = sum([Product.buy(item, count) for item, count in shopping_list])
        return total_price


def main():
    """Main function for testing."""


if __name__ == "__main__":
    main()