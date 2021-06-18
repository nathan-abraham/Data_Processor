import colorama
import pandas as pd
from time import sleep
from colorama import Fore, Back, Style
from rich import console

import csv_utils
import data_processor
import console_utils

colorama.init(autoreset=True)
test_url = "http://winterolympicsmedals.com/medals.csv"
test2_url = "https://raw.githubusercontent.com/nathan-abraham/Safety-Data-Analysis/main/datasets/air_quality_index_india.csv"

if __name__ == "__main__":
    # Load startup
    console_utils.startup()

    # Initializing dataframe variable
    df = pd.DataFrame()
    csv_loaded = False

    # The function sleep(n) causes a delay for n seconds    
    while True:
        console_utils.print_options()  # Print options
        choice = console_utils.choose()  # Get input from user

        # Do different things based on input
        if choice == 1:
            # Get CSV file
            file_name = csv_utils.get_csv()

            # Create dataframe from csv
            if file_name != None:
                df = pd.read_csv(f"{file_name}.csv", error_bad_lines=False)
                csv_loaded = True
                console_utils.dummy_progress_bar("Loading dataframe...")
            sleep(1)
        elif choice == 2:
            df = csv_utils.load_csv_from_file()
            console_utils.dummy_progress_bar("Loading dataframe...")
            csv_loaded = True
        elif csv_loaded and choice == 3:
            data_processor.drop_data(df)
        elif csv_loaded and choice == 4:
            data_processor.graph_data(df)
        elif csv_loaded and choice == 5:
            data_processor.remove_outliers(df)
            sleep(1)
        elif csv_loaded and choice == 6:
            data_processor.sort_data(df)
        elif choice == 7:
            if df.empty:
                console_utils.print_error("Load in a csv file first!")
            else:
                file_name = data_processor.get_file_name()
                data_processor.save_csv(df, file_name=file_name)
            sleep(1)
        elif choice == 8:
            break
        elif choice > 8:
            console_utils.print_error("Enter a number between 1 and 6")
            sleep(1)
        else:
            console_utils.print_error("Load in a csv file first!")
            sleep(1)
        console_utils.print_seperator()
