import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from requests.api import get
import seaborn as sns
import colorama
from colorama import Fore, Style

from console_utils import choose, dummy_progress_bar, print_error, print_success, retry_decorator, print_seperator, print_success, choose_float
from time import sleep
from pandas.api.types import is_numeric_dtype
from rich.progress import Progress

colorama.init(autoreset=True)

@retry_decorator("Not a valid column heading!", KeyError)
def drop_column(df: pd.DataFrame):
    # User types in a column heading, and that heading is removed
    column = input(
        f"Type in the name of the column you want to delete (case sensitive): ")
    df.drop(column, axis=1, inplace=True)
    dummy_progress_bar(f"Deleting column \'{column}\'")


@retry_decorator("Not a valid row number!", KeyError)
def drop_row(df: pd.DataFrame):
    # User types in a row number, and that row is removed
    row = int(input(f"Type in the number of the row you want to delete: "))
    df.drop(labels=row, axis=0, inplace=True)
    dummy_progress_bar(f"Deleting row number {row}")


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
        sleep(1)
    elif drop_choice == 2:
        drop_row(df)
        sleep(1)
    elif drop_choice == 3:
        return
    else:
        print_error("Please type in a number between 1 and 3.")

@retry_decorator("Invalid file name.", exception=OSError)
def get_file_name() -> str:
    file_name = input(
        f"{Fore.LIGHTBLUE_EX}Please type in a name for the file (do not add .csv): ")

    banned_characters = ["*", "?", "\"", "\'", "#"] # These characters are not allowed in file names
    for char in file_name:
        if char in banned_characters:
            raise OSError("Invalid file name.")
    return file_name


@retry_decorator("Failed to convert dataframe to csv.")
def save_csv(df: pd.DataFrame, file_name="temp") -> None:
    # Export dataframe to csv file
    df.to_csv(f"{file_name}.csv")
    dummy_progress_bar("Saving...")

@retry_decorator("Not a valid column heading!")
def get_column(df: pd.DataFrame) -> str:
    # Get column from dataframe based on user input

    column_name = input("Please type in the name of a column: ")
    df[column_name] # Checks if the column heading is correct
    return df[column_name]

def graph_data(df: pd.DataFrame) -> None:
    column_x = get_column(df)
    column_y = get_column(df)
    plt.plot(column_x, column_y)
    plt.show()


# Remove outliers using percentile
def rmout_percentile(df: pd.DataFrame) -> None:
    for column in df:
        if is_numeric_dtype(df[column]): # If the column contains numeric values
            # Chooose min and max quantile
            min_quantile = choose_float("Please type in the value for the minimum quantile (0.05 is a good starting point): ")
            max_quantile = choose_float("Please type in a value for the maximum quantile (0.95 is a good starting point): ")

            # Create thresholds based on quantiles
            lower_threshold = df[column].quantile(min_quantile)
            upper_threshold = df[column].quantile(max_quantile)
            
            # Set up progress bar
            with Progress() as progress:
                task = progress.add_task("[green]Removing...", total=df.shape[0])

                # Iterate through rows and remove values that are greater or less than thresholds
                for index, row in df.iterrows():
                    if row[column] > upper_threshold or row[column] < lower_threshold:
                        df.drop(labels=index, axis=0, inplace=True)
                    progress.update(task, advance=1)
            print_success("Done")
                
        else:
            continue


# Remove outliers using standard deviation
def rmout_std(df: pd.DataFrame) -> None:
    # Similar process to percentile
    for column in df:
        if is_numeric_dtype(df[column]):
            std = df[column].std()

            # Decide thresholds based on 3 standard deviations
            lower_threshold = df[column].mean() - 3 * std
            upper_threshold = df[column].mean() + 3 * std

            with Progress() as progress:
                task = progress.add_task("[green]Removing...", total=df.shape[0])
                for index, row in df.iterrows():
                    if row[column] > upper_threshold or row[column] < lower_threshold:
                        df.drop(labels=index, axis=0, inplace=True)
                    progress.update(task, advance=1)
            print_success("Done")
        else:
            continue

def remove_outliers(df: pd.DataFrame) -> None:
    # Print options
    print(f"{Fore.CYAN}1: Remove outliers using percentile")
    print(f"{Fore.CYAN}2: Remove outliers using standard deviation")
    print(f"{Fore.CYAN}3: Go back")
    print_seperator()

    choice = choose()
    if choice == 1:
        rmout_percentile(df)
    elif choice == 2:
        rmout_std(df)
    elif choice == 3:
        return
    else:
        print_error("Please type in a number between 1 and 3.")
        sleep(1)