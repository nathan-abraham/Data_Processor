import colorama
import requests
from colorama import Fore, Back, Style
from console_utils import print_seperator, retry_decorator

colorama.init(autoreset=True)


@retry_decorator("Invalid file name. Please try again.", exception=OSError)
def write_csv(content):
    file_name = input(f"{Fore.LIGHTBLUE_EX}Please type in a name for the file (do not add .csv): ")

    if file_name == "exit":
        return

    csv_file = open(f"{file_name}.csv", "wb")
    csv_file.write(content)
    csv_file.close()
    return file_name


@retry_decorator("Invalid URL. Please try another one.", exception=requests.exceptions.MissingSchema)
def get_csv():
    url = input(f"{Fore.LIGHTBLUE_EX}Please type in a URL to a csv file: ")

    if url == "exit":
        return   

    request = requests.get(url)
    csv_bytes = request.content

    return write_csv(csv_bytes)
