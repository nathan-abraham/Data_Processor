from csv_utils import retry_decorator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from csv_utils import retry_decorator
from console_utils import choose


def drop_data(df: pd.DataFrame):
	print(f"1: Remove column from dataset")
	print(f"2: Remove row from dataset")
	print(f"3: Go back")
	drop_choice = choose()

	if drop_choice == 1:
		column = input("Type in the name of the column you want to delete (case sensitive): ")
		df.drop(column, axis=1, inplace=True)	
	elif drop_choice == 2:
		row = int(input("Type in the number of the row you want to delete: "))
		df.drop(lables=row, axis=0, inplace=True)
	elif drop_choice == 3:
		return
	


