"""Command line user interface to manage a store."""
import os
from products import Product
from store import Store

CLI_MENU_ITEMS = ["List all products in store",
                  "Show total amount in store",
                  "Make an order (not implemented)",
                  "Quit"
                  ]
CLI_MENU_START_INDEX = 1

# Initial stock of inventory
product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                Product("Google Pixel 7", price=500, quantity=250)
               ]


# ---------------------------------------------------------------------
# CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------
class InvalidChoiceError(BaseException):
    """Raised when an invalid menu choice was made."""
    def __init__(self, message, choice):
        self.message = message
        self.choice = choice


class UserInputMustBeIntError(BaseException):
    """Raised when user input must be a whole number."""
    def __init__(self, message="", input=""):
        self.message = message
        self.choice = input


# ---------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------
def test():
    """Print 'test' for testing purposes."""
    print("test")


def do_nothing():
    """Dummy function."""
    pass

def not_implemented():
    """Another dummy function."""
    print("Not implemented")


def wait_for_enter_key():
    """Stop program until the enter key is pressed."""
    input("\nPress enter to continue...")


def clear_screen():
    """Clear the console from previous text output."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ---------------------------------------------------------------------
# CLI MENU COMMANDS
# ---------------------------------------------------------------------
def list_products(store):
    """List available products."""
    products = store.get_all_products()
    for i, product in enumerate(products):
        print(f"{i + CLI_MENU_START_INDEX:>3}. ", end="")
        product.show()


def show_total_amount_of_store_items(store):
    """Print the total amount of all store items."""
    item_count = store.get_total_quantity()
    print(f"Total of {item_count} items in store.")


def make_order():
    """Let the user make an oder."""
    pass


def quit():
    """Print 'Bye!'"""
    print("Bye!")


# ---------------------------------------------------------------------
# INPUT PROMPTS
# ---------------------------------------------------------------------
def ask_for_user_choice(prompt="Please choose a number: ", accept_int_only=True):
    """Prompt the user to enter their choice and return this value."""
    choice = input(f"{prompt}").strip()
    if accept_int_only and not choice.isdigit():
        raise UserInputMustBeIntError("Choice must be a whole number!", choice)
    if accept_int_only:
        return int(choice)
    return choice


# ---------------------------------------------------------------------
# FUNCTION DISPATCHER
# ---------------------------------------------------------------------
def create_dispatch_table(items: list[str], start=CLI_MENU_START_INDEX):
    """Return a dynamically created dispatch table."""
    return {start + i: item for i, item in enumerate(items)}


def dispatch(dispatch_table, choice: int | str):
    """Call a function utilizing the given dispatch table, and user choice."""
    value = dispatch_table.get(choice)
    if not value:
        raise InvalidChoiceError("Invalid choice!", choice)
    if isinstance(value, tuple):
        action = value[0]
        arg = value[1]
        action(arg)
    else:
        action = value
        action()


# ---------------------------------------------------------------------
# CLI MENU LOGIC
# ---------------------------------------------------------------------
def show_menu():
    """Display a CLI menu."""
    print("   Store Menu")
    print("   ----------")
    for i, menu_item in enumerate(CLI_MENU_ITEMS):
        print(f"{CLI_MENU_START_INDEX + i}. {menu_item}")
    print()


def start(store):
    """Provide the main program flow."""
    dispatch_table = {1: (list_products, store),
                      2: (show_total_amount_of_store_items, store),
                      3: not_implemented,
                      4: quit
                      }
    choice = None
    while True:
        clear_screen()
        show_menu()
        try:
            choice = ask_for_user_choice()
            print()
            dispatch(dispatch_table, choice)
        except (InvalidChoiceError, UserInputMustBeIntError) as e:
            print(f"{e.message} - '{e.choice}'")
        if choice == 4:
            break
        wait_for_enter_key()


def choose_product():
    """Return the selected product from a list of products."""
    pass


def main():
    """Run the store."""
    best_buy = Store(product_list)
    # list_products(best_buy)
    start(best_buy)


if __name__ == "__main__":
    main()