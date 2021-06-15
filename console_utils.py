import colorama  # For printing colors on console
from colorama import Fore, Style

# Decorator to handle errors and retry after exceptions


def retry_decorator(error_message: str, exception=Exception):
    def middle_function(function):
        def wrapper_function(*args, **kwargs):
            while True:
                # If an error occurs, print an error message and ask them to retry
                try:
                    return function(*args, **kwargs)
                except exception:
                    print(f"{Fore.RED}{Style.BRIGHT}{error_message}")
                    continue
                except Exception:
                    print(f"{Fore.RED}{Style.BRIGHT}An unexpected error occurred.")
        return wrapper_function
    return middle_function


def print_seperator():
    # Prints a string of "=" to serve as a separator
    line_len = 45
    result = ""
    for _ in range(line_len):
        result += "="
    print(f"{Fore.GREEN}{result}")


def print_options():
    # User will type in a number, and the corresponding task will be executed
    print(f"{Fore.CYAN}1: Retrieve csv file from url")
    print(f"{Fore.CYAN}2: Drop row or columns from data (not fully implemented yet)")
    print(f"{Fore.CYAN}5: Exit the program")
    print_seperator()


def startup():
    # Print opening message and initialize colors
    colorama.init(autoreset=True)
    print(f"{Fore.BLUE}Welcome to the command line data processor!")
    print_seperator()


@retry_decorator("Please type in a valid integer.", exception=ValueError)
def choose() -> int:
    # Get number indicating what the user wants to do
    choice = int(input(
        f"{Fore.WHITE}{Style.BRIGHT}Type in the number corresponding to the task you want to do: {Style.RESET_ALL}"))
    return choice
