import colorama
import pandas as pd
from time import sleep
from colorama import Fore, Back, Style

import csv_utils
import data_processor
import console_utils



test_url = "http://winterolympicsmedals.com/medals.csv"

if __name__ == "__main__":
    # Load startup
    console_utils.startup()

    # Initializing dataframe variable
    df = None
    loaded = False
    while True:
        console_utils.print_options() # Print options
        choice = console_utils.choose() # Get input from user

        # Do different things based on input
        if choice == 1:
            # Get CSV file
            file_name = csv_utils.get_csv()

            # Create dataframe from csv
            if df != None:
                df = pd.read_csv(f"{file_name}.csv", error_bad_lines=False)
                loaded = True
        elif loaded and choice == 2:
            data_processor.drop_data(df)
        elif loaded and choice == 3:
            pass
        elif choice == 5:
            break
        elif choice > 5:
            print("Enter a number between 1 and 5")
            sleep(1)
        else:
            print("Load in a csv file first!")
            sleep(1)
        console_utils.print_seperator()
    
    
