import pandas as pd
import csv_utils


def startup():
    print("Welcome to the command line data processor!")

    # User will type in a number, and the corresponding task will be executed
    print("1: Retrieve csv file from url")
    print("2: Drop row or columns from data")


test_url = "http://winterolympicsmedals.com/medals.csv"

if __name__ == "__main__":
    choice = int(
        input("Type in the number corresponding to the task you want to do: "))
    if choice == 1:
        csv_utils.get_csv()
    if choice == 2:
        pass
    if choice == 3:
        pass
