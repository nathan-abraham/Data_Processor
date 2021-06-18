import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import colorama
from colorama import Fore

from console_utils import choose, dummy_progress_bar, print_error, print_success, retry_decorator, print_seperator, print_success, choose_float, choose_int, choose_str
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
def get_column(df: pd.DataFrame, msg="Please type in the name of a column: "):
    # Get column from dataframe based on user input

    column_name = input(msg)
    df[column_name] # Checks if the column heading is correct
    return df[column_name]

@retry_decorator("Not a valid numeric column heading!")
def get_numeric_column(df: pd.DataFrame, msg="Please type in the name of a column with numeric data: "):
    # Get column from dataframe based on user input

    column_name = input(msg)
    if not is_numeric_dtype(df[column_name]):
        raise ValueError() # Checks if the column heading is correct
    return df[column_name]

@retry_decorator("Not a valid column heading!")
def get_column_name(df: pd.DataFrame):
    column_name = input("Please type in the name of a column: ")
    df[column_name] # Checks if the column heading is correct
    return column_name

def graph_count_plot(df: pd.DataFrame) -> None:
    # Initialize figure
    plt.figure(figsize=(12, 6))

    # Get the name of the column
    column_name = get_column_name(df)

    # Get the titel of the graph
    title = choose_str("Please type in the title of this graph: ")
    plt.title(title) 

    sns.set_style("dark")
    ax = sns.countplot(x=column_name, data=df)

    # Rotate labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")

    plt.show()

def graph_histogram(df: pd.DataFrame) -> None:
    # Get column and bumber of bins
    column = get_column(df)
    num_bins = choose_int("Please type in the number of bins in the histogram: ")

    # Get title
    title = choose_str("Please type in the title of this graph: ")
    plt.title(title) 

    # Plot histogram and show it
    plt.hist(column, num_bins)
    plt.show()

def graph_pie(df: pd.DataFrame) -> None:
    # Get column
    column = get_column(df)

    # Get the pie chart labels and corresponding values (slices)
    labels = list(column.unique())
    slices = list(column.value_counts())

    # Get title of graph
    title = choose_str("Please type in the title of this graph: ")
    plt.title(title) 

    # Plot pie chart and show it
    plt.pie(slices, labels=labels)
    plt.show()

def graph_line(df: pd.DataFrame) -> None:
    # Get x and y columns
    x_column = get_column(df, msg="Please type in the name of the column that represents the x-axis: ")
    y_column = get_numeric_column(df, msg="Please type in the name of the column that represents the y-axis: ")

    # Plot first 500 points to save time
    if x_column.shape[0] > 500 or y_column.shape[0] > 500:
        x_column.drop(list(range(500, x_column.shape[0])), inplace=True)
        y_column.drop(list(range(500, y_column.shape[0])), inplace=True)

    # Get title
    title = choose_str("Please type in the title of this graph: ")
    plt.title(title) 

    # Plot line plot and show it
    plt.plot(x_column, y_column)
    plt.show()


def graph_data(df: pd.DataFrame) -> None:
    # Print options
    print(f"{Fore.CYAN}1: Create a countplot from a column")
    print(f"{Fore.CYAN}2: Create a histogram from a column")
    print(f"{Fore.CYAN}3: Create a pie chart from a column")
    print(f"{Fore.CYAN}4: Create a line plot from two columns")
    print(f"{Fore.CYAN}5: Go back")

    # Get use choice
    choice = choose()

    if choice == 1:
        graph_count_plot(df)
    elif choice == 2:
        graph_histogram(df)
    elif choice == 3:
        graph_pie(df)
    elif choice == 4:
        graph_line(df)
    elif choice == 5:
        return
    else:
        print_error("Please type in a number between 1 and 5.")

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
            # Get standard deviation for this column
            std = df[column].std()

            # Decide thresholds based on 3 standard deviations
            lower_threshold = df[column].mean() - 3 * std
            upper_threshold = df[column].mean() + 3 * std

            # Initialize progress bar
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

    # Filter outlier in different ways based on user input
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

@retry_decorator("Please type in y or n")
def get_ascending() -> bool:
    ascending = input("Do you want to sort in ascending order (y or n)? ").lower()
    return ascending == "y"

#@retry_decorator("Failed to sort columns. Please try again.", exception=KeyError)
def sort_column(df: pd.DataFrame):
    column_name = get_column_name(df)
    ascending = get_ascending()
    df.columns = df.columns.str.strip()
    df.sort_values(by=column_name, inplace=True, ascending=ascending, axis=0)
    dummy_progress_bar("Sorting...")

def sort_indices(df: pd.DataFrame):
    # Get whether they want ascending or not
    ascending = get_ascending()

    # Strip columns of whitespace
    df.columns = df.columns.str.strip()

    # Sort by indices
    df.sort_index(inplace=True, ascending=ascending)

    # Display progress bar
    dummy_progress_bar("Sorting...")


def sort_data(df: pd.DataFrame) -> None:
    # Print options
    print(f"{Fore.CYAN}1: Sort data in a particular column")
    print(f"{Fore.CYAN}2: Sort data by row indices")
    print(f"{Fore.CYAN}3: Go back")
    print_seperator()

    # Get the number choice from the user
    choice = choose()

    # Execute different functions based on what they typed in
    if choice == 1:
        sort_column(df)
    elif choice == 2:
        sort_indices(df)
    elif choice == 3:
        return
    else:
        print_error("Please type in a number between 1 and 4.")
        sleep(1)

