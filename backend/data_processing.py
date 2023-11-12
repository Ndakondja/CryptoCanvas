import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def readInAllCSVFiles():{

}
def get_coin_names():
    all_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
    
    coin_names = [file.split("_")[1].split(".")[0] for file in all_files]

    return coin_names



data_cache = None

def load_data(directory_path):
    """
    Load and cache cleaned data. If data is already cached, return the cached data.

    Args:
    - directory_path (str): Path to the directory containing the CSV files.

    Returns:
    - dict: A dictionary where keys are filenames and values are cleaned DataFrames.
    """
    global data_cache
    if data_cache is None:
        data_cache = read_and_clean_data(directory_path)
    return data_cache

def read_and_clean_data(directory_path):
    """
    Read all CSV files in the given directory and clean the data.

    Args:
    - directory_path (str): Path to the directory containing the CSV files.

    Returns:
    - dict: A dictionary where keys are filenames and values are cleaned DataFrames.
    """
    data_cache = {}

    # List all files in the directory
    all_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    for filename in all_files:
        # Ensure it's a CSV file
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)

            # Read the file into a DataFrame
            df = pd.read_csv(file_path)

            # Clean the data (customize as per your needs)
            df = clean_dataframe(df)

            # Store in the dictionary
            data_cache[filename] = df

    return data_cache

def clean_dataframe(df):
    # Handle missing values (you can customize this)
    df.dropna(inplace=True)

    # Convert data types if necessary (customize based on your dataset)
    # Example: df['column_name'] = df['column_name'].astype('desired_dtype')

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    return df
def compute_bitcoin_correlation(selected_coins, start_date, end_date):
    """
    Compute the correlation of Bitcoin with the selected coins within the given date range.

    Args:
    - selected_coins (list): List of selected coin names.
    - start_date (str): Start date in the format 'YYYY-MM-DD'.
    - end_date (str): End date in the format 'YYYY-MM-DD'.

    Returns:
    - Series: Correlation values of Bitcoin against the selected coins.
    """
    
    # Use the cached data
    global data_cache

    # Prepare a DataFrame for closing prices
    crypto_close_prices = pd.DataFrame()

    # Always include Bitcoin
    bitcoin_df = data_cache.get("coin_Bitcoin.csv")
    if bitcoin_df is not None:
        filtered_bitcoin_df = bitcoin_df[(bitcoin_df['Date'] >= start_date) & (bitcoin_df['Date'] <= end_date)]
        filtered_bitcoin_df.loc[:, 'Date'] = pd.to_datetime(filtered_bitcoin_df['Date'])

        crypto_close_prices['Bitcoin'] = filtered_bitcoin_df.set_index('Date')['Close']

    # Add closing prices of selected coins from cached data with the "coin_" prefix
    for coin in selected_coins:
        fileName = "coin_" + coin + ".csv"
        coin_df = data_cache.get(fileName)
      
        if coin_df is not None:
            filtered_coin_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]
            filtered_coin_df.loc[:, 'Date'] = pd.to_datetime(filtered_coin_df['Date'])

            
            # Merge the dataframes on 'Date'
            merged_df = filtered_bitcoin_df.merge(filtered_coin_df[['Date', 'Close']], on='Date', how='outer', suffixes=('', f'_{coin}'))
            # Fill NaNs with 0
            merged_df[f'Close_{coin}'].fillna(0, inplace=True)
            
            # Add to the main DataFrame
            crypto_close_prices[coin] = merged_df.set_index('Date')[f'Close_{coin}']

    # Compute the correlation matrix
    correlation_matrix = crypto_close_prices.corr()


    # Check if 'Bitcoin' exists in the columns
    if 'Bitcoin' in correlation_matrix.columns:
        # Extract the correlation values for Bitcoin
        return correlation_matrix
    else:
        raise ValueError("Bitcoin data not found. Ensure 'coin_Bitcoin.csv' is present and contains the required data.")


   

directory_path = "crypto_data"
data = load_data(directory_path)
def compute_rolling_volatility(selected_coins, start_date, end_date, window=20):
    """
    Compute the rolling volatility for the selected coins within the given date range.

    Args:
    - selected_coins (list): List of selected coin names.
    - start_date (str): Start date in the format 'YYYY-MM-DD'.
    - end_date (str): End date in the format 'YYYY-MM-DD'.
    - window (int): Rolling window for computing volatility. Default is 20 days.

    Returns:
    - DataFrame: Rolling volatilities of the selected coins.
    """
    global data_cache

    # Prepare a DataFrame for closing prices
    crypto_close_prices = pd.DataFrame()

    for coin in selected_coins:
        file_name = "coin_" + coin + ".csv"
        coin_df = data_cache.get(file_name)
      
        if coin_df is not None:
            filtered_coin_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]
            filtered_coin_df.loc[:, 'Date'] = pd.to_datetime(filtered_coin_df['Date'])
            
            crypto_close_prices[coin] = filtered_coin_df.set_index('Date')['Close']

    # Compute daily returns
    crypto_returns = crypto_close_prices.pct_change().dropna()

    # Compute rolling volatility
    rolling_volatility = crypto_returns.rolling(window).std()
    rolling_volatility = rolling_volatility.dropna()
    return rolling_volatility



def volatility():
    selected_coins = ["Cardano", "XRP", "Litecoin", "Ethereum", "Bitcoin"] 
    start_date = "2021-01-01"
    end_date = "2021-12-31" 
    volatility= compute_rolling_volatility(selected_coins,start_date,end_date) 
    return volatility
    
def correlationMatrix():
    selected_coins = ["Cardano", "XRP", "Litecoin", "Ethereum", "Bitcoin"] 
    start_date = "2021-01-01"
    end_date = "2021-12-31" 
    correlations = compute_bitcoin_correlation(selected_coins, start_date, end_date)
    return correlations







