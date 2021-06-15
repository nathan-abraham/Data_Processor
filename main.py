import colorama
import pandas as pd
from colorama import Fore, Back, Style

import csv_utils
import data_processor
import console_utils



test_url = "http://winterolympicsmedals.com/medals.csv"

if __name__ == "__main__":
    console_utils.startup()
    df = None
    while True:
        console_utils.print_options()
        choice = console_utils.choose()
        if choice == 1:
            file_name = csv_utils.get_csv()
            df = pd.read_csv(f"{file_name}.csv")
        elif choice == 2:
            data_processor.drop_data(df)
        elif choice == 3:
            pass
        elif choice == 5:
            break
        console_utils.print_seperator()
    
    
