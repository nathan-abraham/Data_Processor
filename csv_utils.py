import colorama
import requests
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

def retry_decorator(error_message: str, exception=Exception):
    def middle_function(function):
        def wrapper_function(*args, **kwargs):
            while True:
                try:
                    function(*args, **kwargs)
                except exception:
                    print(f"{Fore.RED}{Style.BRIGHT}{error_message}")
                    continue
                except Exception:
                    print(f"{Fore.RED}{Style.BRIGHT}An unexpected error occurred.")
                break
        return wrapper_function
    return middle_function

@retry_decorator("Invalid file name. Please try again.", exception=OSError)
def write_csv(content):
    file_name = input("Please type in a name for the file (do not add .csv): ")

    if file_name == "exit":
        return

    csv_file = open(f"{file_name}.csv", "wb")
    csv_file.write(content)
    csv_file.close()


@retry_decorator("Invalid URL. Please try another one.", exception=requests.exceptions.MissingSchema)
def get_csv():
    url = input("Please type in a URL to a csv file: ")

    if url == "exit":
        return   

    request = requests.get(url)
    csv_bytes = request.content

    write_csv(csv_bytes)
