import pandas as pd
import numpy as np
import os
import pickle
from datetime import datetime, timedelta

def compute_moving_averages(folder_path):
    # List to hold dataframes for each file
    dfs_list = []

    # Get a list of pickle files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

    for file in files:
        # Load the pickle file
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        # Ensure the data is a pandas dataframe
        if not isinstance(data, pd.DataFrame):
            continue

        # Compute moving averages
        data['MA_50'] = data['Close'].rolling(window=50).mean()
        data['MA_100'] = data['Close'].rolling(window=100).mean()
        data['MA_200'] = data['Close'].rolling(window=200).mean()

        # Get the last month data from the 16th to the 15th of the previous month
        end_date = datetime.now().replace(day=16)
        start_date = (end_date - timedelta(days=30)).replace(day=16)
        last_month_data = data[(data.index >= start_date) & (data.index < end_date)]

        # Append the result to the list
        dfs_list.append(last_month_data)

    # Concatenate all dataframes
    final_df = pd.concat(dfs_list)

    # Sort the dataframe
    sorted_df = final_df.sort_index()

    return sorted_df

# Replace 'your_folder_path' with the actual folder path containing the pickle files
folder_path = 'your_folder_path'
result_df = compute_moving_averages(folder_path)

# To print the result, uncomment the following line:
# print(result_df)

# Note: The function assumes that the index of each dataframe in the pickle files is datetime.
# If the index is not datetime, you would need to convert it before filtering the last month's data.
# Also, the code does not handle possible errors such as file read errors, or missing 'Close' columns.
