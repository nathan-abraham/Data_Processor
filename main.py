import colorama
import pandas as pd
from time import sleep
from colorama import Fore, Back, Style

import csv_utils
import data_processor
import console_utils

colorama.init(autoreset=True)
test_url = "http://winterolympicsmedals.com/medals.csv"

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
                console_utils.print_success("Dataframe succesfully loaded.")
            sleep(1)
        elif csv_loaded and choice == 2:
            data_processor.drop_data(df)
        elif csv_loaded and choice == 3:
            data_processor.get_file_name()
        elif choice == 4:
            if df.empty:
                console_utils.print_error("Load in a csv file first!")
            else:
                file_name = data_processor.get_file_name()
                data_processor.save_csv(df, file_name=file_name)
            sleep(1)
        elif choice == 5:
            break
        elif choice > 5:
            console_utils.print_error("Enter a number between 1 and 5")
            sleep(1)
        else:
            console_utils.print_error("Load in a csv file first!")
            sleep(1)
        console_utils.print_seperator()
