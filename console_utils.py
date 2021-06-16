import colorama  # For printing colors on console
from colorama import Fore, Style

# Decorator to handle errors and retry after exceptions

colorama.init(autoreset=True)

def retry_decorator(error_message: str, exception=Exception):
    def middle_function(function):
        def wrapper_function(*args, **kwargs):
            while True:
                # If an error occurs, print an error message and ask them to retry
                try:
                    return function(*args, **kwargs)
                except exception:
                    print_error(error_message=error_message)
                    continue
                except Exception:
                    print_error(error_message="An unexpected error occurred.")
        return wrapper_function
    return middle_function


def print_seperator():
    # Prints a string of "=" to serve as a separator
    line_len = 60
    result = ""
    for _ in range(line_len):
        result += "="
    print(f"{Fore.GREEN}{result}")


def print_options():
    # User will type in a number, and the corresponding task will be executed
    print(f"{Fore.CYAN}1: Retrieve csv file from url")
    print(f"{Fore.CYAN}2: Drop row or columns from data")
    print(f"{Fore.CYAN}3: Graph columns of data")
    print(f"{Fore.CYAN}4: Save modified dataframe to a csv file")
    print(f"{Fore.CYAN}5: Exit the program")
    print_seperator()

# Print an error message in bright red
def print_error(error_message: str):
    print(f"{Fore.RED}{Style.BRIGHT}{error_message}")

# Print a success message in bright cyan
def print_success(message: str):
    print(f"{Fore.CYAN}{Style.BRIGHT}{message}")

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
