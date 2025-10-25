"""Provide the Product class."""


class Product:
    """Represent a specific type of product available in the store.

    - Encapsulate information about the product, including its name and price.
    - Keep track of the total quantity of a product in stock.
    - For each purchase stock quantity will be updated.
    """
    def __int__(self, name, price, quantity):
        """Validate input, create instance variables and set active to True."""
        if not all({name, price, quantity}):
            raise ValueError
        if not isinstance(price, (int, float)) or isinstance(quantity, int):
            raise TypeError
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        """Return total quantity of a product in stock."""
        pass

    def set_quantity(self, quantity):
        """Set quantity for a product, deactivate product if quantity reaches 0."""
        pass

    def is_active(self) -> bool:
        """Return True if a product is active, otherwise False."""
        pass

    def activate(self):
        """Activate a product."""
        pass

    def deactivate(self):
        """Deactivate a product."""
        pass

    def show(self):
        """Print a string that represents the product.

        Example: "MacBook Air M2, Price: 1450, Quantity: 100"
        """
        pass

    def buy(self, quantity) -> float:
        """Buy the given quantity of a product.

        Return the purchase's total price
        and update the product quantity in stock.

        Raise exception if product is out of stock for the given quantity.
        """
        pass
