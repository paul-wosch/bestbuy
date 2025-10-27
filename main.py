"""Command line user interface to manage a store."""
import os
from products import Product
from store import Store

CLI_MENU_ITEMS = ["List all products in store",
                  "Show total amount in store",
                  "Make an order",
                  "Quit"
                  ]
CLI_MENU_START_INDEX = 1
HEADER_INDENT = 0

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
    def __init__(self, message="", user_input=""):
        self.message = message
        self.choice = user_input


class CancelDialog(BaseException):
    """Raised when user cancels cli dialog."""
    def __init__(self):
        self.message = "Action cancelled. Going back to menu..."


class NoProductsError(BaseException):
    """Raised when there are no Products in store."""
    def __init__(self):
        self.message = "Currently no products in store. Come back later!"


# ---------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------
def test():
    """Print 'test' for testing purposes."""
    print("test")


def do_nothing():
    """Dummy function."""


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
    """Print products and return them as a list."""
    products = store.get_all_products()
    if not products:
        raise NoProductsError
    for i, product in enumerate(products):
        print(f"{i + CLI_MENU_START_INDEX:>3}. ", end="")
        product.show()
    return products


def show_total_amount_of_store_items(store):
    """Print the total amount of all store items."""
    item_count = store.get_total_quantity()
    print(f"Total of {item_count} items in store.")


def make_order(store):
    """Let the user make an order."""
    shopping_cart = []
    chosen_product = None
    should_place_order = False
    error_message_no_integer = "Choice must be a whole number or '..'!"
    # -----------------------------------------------------------------
    # Show the products menu
    while True:
        clear_screen()
        print_title()
        print_subtitle("Make order")
        print()
        if shopping_cart:
            print(f"{'0':>3}. PLACE ORDER")
        list_products(store)
        # -----------------------------------------------------------------
        # Create dispatch table
        products = store.get_all_products()
        dispatch_table = create_dispatch_table(products)
        print()
        # -----------------------------------------------------------------
        # Prompt for product
        while True:
            prompt = "Select a product "
            if shopping_cart:
                prompt += "or 'PLACE ORDER' "
            prompt += "(Enter '..' to cancel): "
            try:
                chosen_product_index = ask_for_user_choice(prompt, nested_call=True)
            except UserInputMustBeIntError:
                print(error_message_no_integer)
                continue
            except CancelDialog as exc:
                cleanup_on_cancel_order(shopping_cart)
                raise CancelDialog from exc
            if chosen_product_index == 0:
                should_place_order = True
                break
            if not dispatch_table.get(chosen_product_index):
                print("Please select one of the above products.")
            else:
                chosen_product = dispatch_table[chosen_product_index]
                if chosen_product.available_qty == 0:
                    print("Currently there are no items available for sale. Try again later.")
                else:
                    break
        # -----------------------------------------------------------------
        # Prompt for quantity
        if not should_place_order:
            while True:
                prompt = "Enter the number of items you want to buy (Type '..' to cancel): "
                try:
                    chosen_product_qty = ask_for_user_choice(prompt, nested_call=True)
                except UserInputMustBeIntError:
                    print(error_message_no_integer)
                    continue
                except CancelDialog as exc:
                    cleanup_on_cancel_order(shopping_cart)
                    raise CancelDialog from exc
                if chosen_product_qty <= chosen_product.available_qty:
                    shopping_cart.append((chosen_product, chosen_product_qty))
                    print(f"{chosen_product_qty} x '{chosen_product.name}' added to shopping cart.")
                    chosen_product.allocate(chosen_product_qty)
                    break
                print("Quantity larger than available items in stock.")
            wait_for_enter_key()
        # -----------------------------------------------------------------
        # Finally place the order
        if should_place_order:
            buy(store, shopping_cart)
            break


def cleanup_on_cancel_order(shopping_cart):
    """Reallocate availability for products in shopping card."""
    for product, quantity in shopping_cart:
        product.deallocate(quantity)


def buy(store, shopping_cart):
    """Finally place the order."""
    print("Placing order...")
    total = store.order(shopping_cart)
    if total:
        print(f"Order made! Total payment: ${total:,}")
    else:
        print("There was a problem placing your order!")


def say_goodbye():
    """Print 'Bye!'"""
    print("Bye!")


# ---------------------------------------------------------------------
# INPUT PROMPTS
# ---------------------------------------------------------------------
def ask_for_user_choice(prompt="Please choose a number: ",
                        accept_int_only=True,
                        nested_call=False):
    """Prompt the user to enter their choice and return this value."""
    choice = input(f"{prompt}").strip()
    if nested_call and choice == "..":
        raise CancelDialog()
    if accept_int_only and not choice.isdigit():
        raise UserInputMustBeIntError("Choice must be a whole number!", choice)
    if accept_int_only:
        return int(choice)
    return choice


# ---------------------------------------------------------------------
# FUNCTION DISPATCHER
# ---------------------------------------------------------------------
def create_dispatch_table(items: list[str], start_index=CLI_MENU_START_INDEX) -> dict:
    """Return a dynamically created dispatch table."""
    return {start_index + i: item for i, item in enumerate(items)}


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
def indent(n=HEADER_INDENT):
    """Return whitespace characters for the given amount."""
    return f"{' ' * n}"


def print_title(title="BESTBYE STORE"):
    """Print a title for the CLI."""
    print(f"{indent()}{title}")
    print(f"{indent()}-------------")


def print_subtitle(subtitle):
    """Print the given subtitle."""
    print(f"{indent()}{subtitle}")


def show_menu():
    """Display a CLI menu."""
    for i, menu_item in enumerate(CLI_MENU_ITEMS):
        print(f"{CLI_MENU_START_INDEX + i:>3}. {menu_item}")
    print()


def cli_input_listener(dispatch_table):
    """Listen for user input utilizing the provided dispatch table.

    Return the user choice."""
    choice = None
    while True:
        clear_screen()
        print_title()
        print_subtitle("Main menu")
        print()
        show_menu()
        try:
            choice = ask_for_user_choice()
            print()
            dispatch(dispatch_table, choice)
        except (InvalidChoiceError, UserInputMustBeIntError) as e:
            print(f"{e.message} - '{e.choice}'")
        except NoProductsError as e:
            print(f"{e.message}")
        except CancelDialog as e:
            print(f"{e.message}")
        if choice == 4:
            break
        wait_for_enter_key()
    return choice


def start(store):
    """Provide the main program flow."""
    dispatch_table = {1: (list_products, store),
                      2: (show_total_amount_of_store_items, store),
                      3: (make_order, store),
                      4: say_goodbye
                      }
    cli_input_listener(dispatch_table)


def choose_product():
    """Return the selected product from a list of products."""


def main():
    """Run the store."""
    best_buy = Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
