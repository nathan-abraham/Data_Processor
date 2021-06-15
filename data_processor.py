import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore, Style

from console_utils import choose, retry_decorator, print_seperator

@retry_decorator("Not a valid column heading!", KeyError)
def drop_column(df):
	# User types in a column heading, and that heading is removed
	column = input(f"Type in the name of the column you want to delete (case sensitive): ")
	df.drop(column, axis=1, inplace=True)	

@retry_decorator("Not a valid row number!", KeyError)
def drop_row(df):
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

	drop_choice = choose() # Get input for what the user wants to do

	# Execute different functions based on input
	if drop_choice == 1:
		drop_column(df)
	elif drop_choice == 2:
		drop_row(df)
	elif drop_choice == 3:
		return
	


