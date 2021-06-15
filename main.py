import colorama
import pandas as pd
import csv_utils
from colorama import Fore, Back, Style

def print_seperator():
    line_len = 30
    result = ""
    for _ in range(line_len):
        result += "="
    print(result)

def print_options():
    # User will type in a number, and the corresponding task will be executed
    print("1: Retrieve csv file from url")
    print("2: Drop row or columns from data")
    print("5: Exit the program")
    print_seperator()

def startup():
    colorama.init(autoreset=True)
    print("Welcome to the command line data processor!")
    print_seperator()

test_url = "http://winterolympicsmedals.com/medals.csv"

if __name__ == "__main__":
    startup()
    while True:
        print_options()
        choice = int(input("Type in the number corresponding to the task you want to do: "))
        if choice == 1:
            csv_utils.get_csv()
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 5:
            break
        print_seperator()
    
    
