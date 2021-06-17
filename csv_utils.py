import colorama
import requests
from colorama import Fore, Back, Style
from console_utils import print_seperator, retry_decorator, dummy_progress_bar
from rich.progress import track
from time import sleep

colorama.init(autoreset=True)


@retry_decorator("Invalid file name. Please try again.", exception=OSError)
def write_csv(content):
    # Get input for the name of the file
    file_name = input(
        f"{Fore.LIGHTBLUE_EX}Please type in a name for the file (do not add .csv): ")

    if file_name == "exit":
        return

    # Create a new csv file with that name in 'write' mode
    csv_file = open(f"{file_name}.csv", "wb")

    dummy_progress_bar("Writing csv...")

    # Write the content to the file, close it, then return the file name
    csv_file.write(content)

    csv_file.close()
    return file_name


@retry_decorator("Invalid URL. Please try another one.", exception=requests.exceptions.MissingSchema)
def get_csv():
    # Get URL from the user
    url = input(f"{Fore.LIGHTBLUE_EX}Please type in a URL to a csv file: ")

    if url == "exit":
        return

    # Send a request to a website
    request = requests.get(url)
    dummy_progress_bar("Retrieving csv...")
    # Get raw csv raw bytes
    csv_bytes = request.content

    # Write content to csv file and return the result
    return write_csv(csv_bytes)
