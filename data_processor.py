import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests.api import get
import seaborn as sns
import colorama
from colorama import Fore, Style

from console_utils import choose, print_success, retry_decorator, print_seperator, print_success

colorama.init(autoreset=True)

@retry_decorator("Not a valid column heading!", KeyError)
def drop_column(df: pd.DataFrame):
    # User types in a column heading, and that heading is removed
    column = input(
        f"Type in the name of the column you want to delete (case sensitive): ")
    df.drop(column, axis=1, inplace=True)


@retry_decorator("Not a valid row number!", KeyError)
def drop_row(df: pd.DataFrame):
    # User types in a row number, and that row is removed
    row = int(input(f"Type in the number of the row you want to delete: "))
    df.drop(labels=row, axis=0, inplace=True)


def drop_data(df: pd.DataFrame):
    print_seperator()

    # Print options
    print(f"{Fore.CYAN}1: Remove column from dataset")
    print(f"{Fore.CYAN}2: Remove row from dataset")
    print(f"{Fore.CYAN}3: Go back")
    print_seperator()

    drop_choice = choose()  # Get input for what the user wants to do

    # Execute different functions based on input
    if drop_choice == 1:
        drop_column(df)
    elif drop_choice == 2:
        drop_row(df)
    elif drop_choice == 3:
        return

@retry_decorator("Invalid file name.", exception=OSError)
def get_file_name() -> str:
    file_name = input(
        f"{Fore.LIGHTBLUE_EX}Please type in a name for the file (do not add .csv): ")
    banned_characters = ["*", "?", "\"", "\'", "#"]
    for char in file_name:
        if char in banned_characters:
            raise OSError("Invalid file name.")
    return file_name


@retry_decorator("Failed to convert dataframe to csv.")
def save_csv(df: pd.DataFrame, file_name="temp") -> None:
    df.to_csv(f"{file_name}.csv")
    print_success("File sucessfully created.")
