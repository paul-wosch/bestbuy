"""Provide the Product class."""


class ProductOutOfStockError(BaseException):
    """Raised when a product is out of stock."""


class ValueMissingError(BaseException):
    """Raised when a value is missing."""


class Product:
    """Represent a specific type of product available in the store.

    - Encapsulate information about the product, including its name and price.
    - Keep track of the total quantity of a product in stock.
    - For each purchase stock quantity will be updated.
    """
    def __init__(self, name, price, quantity):
        """Validate input, create instance variables and set active to True."""
        if not name.strip():
            raise ValueMissingError("Name cannot be empty or whitespace")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number")
        if not all((price >= 0, quantity >= 0)):
            raise ValueError("Price and quantity cannot be negative")
        self.name = name
        self.price = price
        self.quantity = quantity
        if self.quantity > 0:
            self.active = True
        else:
            self.active = False

    def get_quantity(self) -> int:
        """Return total quantity of a product in stock."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set quantity for a product, deactivate product if quantity reaches 0."""
        self.quantity = quantity
        if quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return True if a product is active, otherwise False."""
        return self.active

    def activate(self):
        """Activate a product."""
        self.active = True

    def deactivate(self):
        """Deactivate a product."""
        self.active = False

    def show(self):
        """Print a string that represents the product.

        Example: "MacBook Air M2, Price: 1450, Quantity: 100"
        """
        status = "active"
        if not self.is_active():
            status = "deactivated"
        product_str = (f"{self.name}, "
                       f"Price: {self.price}, "
                       f"Quantity: {self.quantity}, "
                       f"Status: {status}")
        print(product_str)

    def buy(self, quantity) -> float:
        """Buy the given quantity of a product.

        Return the purchase's total price
        and update the product quantity in stock.

        Raise exception if product is out of stock for the given quantity.
        """
        if not self.quantity >= quantity or self.active is False:
            raise ProductOutOfStockError(f"Product '{self.name}' "
                                         f"is out of stock or deactivated")
        self.set_quantity(self.quantity - quantity)
        return self.price * quantity


def main():
    """Main function for testing when running the script under main."""


if __name__ == "__main__":
    main()
