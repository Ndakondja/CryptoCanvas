import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta


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
    global data_cache

    crypto_close_prices = pd.DataFrame()

    # Ensure bitcoin_df's 'Date' column is in datetime format
    bitcoin_df = data_cache.get("coin_Bitcoin.csv")
    if bitcoin_df is not None:
        bitcoin_df['Date'] = pd.to_datetime(bitcoin_df['Date'])
        filtered_bitcoin_df = bitcoin_df[(bitcoin_df['Date'] >= start_date) & (bitcoin_df['Date'] <= end_date)]
        crypto_close_prices['Bitcoin'] = filtered_bitcoin_df.set_index('Date')['Close']

    for coin in selected_coins:
        fileName = "coin_" + coin + ".csv"
        coin_df = data_cache.get(fileName)

        if coin_df is not None:
            # Ensure coin_df's 'Date' column is in datetime format
            coin_df['Date'] = pd.to_datetime(coin_df['Date'])
            filtered_coin_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]

            # Merge operation
            merged_df = filtered_bitcoin_df.merge(filtered_coin_df[['Date', 'Close']], on='Date', how='outer', suffixes=('', f'_{coin}'))
            crypto_close_prices[coin] = merged_df.set_index('Date')[f'Close_{coin}']

    correlation_matrix = crypto_close_prices.corr()

    if 'Bitcoin' in correlation_matrix.columns:
        return correlation_matrix
    else:
        raise ValueError("Bitcoin data not found. Ensure 'coin_Bitcoin.csv' is present and contains the required data.")

   

directory_path = "crypto_data"
data = load_data(directory_path)
def compute_rolling_volatility(selected_coins, start_date, end_date, window=20):
    global data_cache

    crypto_close_prices = pd.DataFrame()

    for coin in selected_coins:
        file_name = f"coin_{coin}.csv"
        coin_df = data_cache.get(file_name)
      
        if coin_df is not None and 'Date' in coin_df.columns:
            # Convert 'Date' to datetime, and filter based on the date range
            coin_df['Date'] = pd.to_datetime(coin_df['Date'], errors='coerce')
            filtered_coin_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]

            # Check if DataFrame is empty after filtering
            if not filtered_coin_df.empty:
                # Calculate the closing prices and merge with the main DataFrame
                filtered_coin_df.set_index('Date', inplace=True)
                crypto_close_prices[coin] = filtered_coin_df['Close']
            else:
                print(f"No data available for {coin} in the specified date range.")
        else:
            print(f"Data for {coin} not found or 'Date' column missing.")

    if not crypto_close_prices.empty:
        # Compute daily returns
        crypto_returns = crypto_close_prices.pct_change().dropna()

        # Compute rolling volatility
        rolling_volatility = crypto_returns.rolling(window).std()
        return rolling_volatility.dropna()
    else:
        print("No valid data available for computing volatility.")
        return None




HARDCODED_COINS = ['Bitcoin', 'Ethereum', 'XRP', 'Litecoin', 'Cardano']

def load_selected_coins_data(selected_coins, start_date, end_date):
    global data_cache
    coins_to_load = selected_coins if selected_coins else HARDCODED_COINS
    all_coins_data = []

    for coin in coins_to_load:
        file_name = f"coin_{coin}.csv"
        
        if file_name in data_cache:
            coin_df = data_cache[file_name]
            coin_df['Date'] = pd.to_datetime(coin_df['Date'])
            
            filtered_df = coin_df[(coin_df['Date'] >= pd.to_datetime(start_date)) & 
                                  (coin_df['Date'] <= pd.to_datetime(end_date))].copy()
            filtered_df['Coin'] = coin
            
            all_coins_data.append(filtered_df[['Date', 'Close', 'Coin']])
        else:
            print(f"No data found for {coin}.")

    combined_df = pd.concat(all_coins_data)
    combined_df.set_index('Date', inplace=True)
    return combined_df



def calculate_start_date(time_range, end_date_str="2021-07-06"):
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    if time_range == 'Last 6 Months':
        start_date = end_date - timedelta(days=6*30)  # Approximately 6 months
    elif time_range == 'Last 12 Months':
        start_date = end_date - timedelta(days=12*30)  # Approximately 12 months
    elif time_range == 'Last 24 Months':
        start_date = end_date - timedelta(days=2*365)  # 2 years
    elif time_range == 'Last 48 Months':
        start_date = end_date - timedelta(days=4*365)  # 4 years
    else:
        # Default case, can be adjusted as needed
        start_date = end_date - timedelta(days=6*30)

    return start_date.strftime('%Y-%m-%d'), end_date_str

def calculate_avg_market_cap(selected_coins, start_date, end_date):
    global data_cache
    market_cap_data = []

    # Calculate average market capitalizations
    for coin in selected_coins:
        file_name = f"coin_{coin}.csv"
        coin_df = data_cache.get(file_name)

        if coin_df is not None:
            coin_df['Date'] = pd.to_datetime(coin_df['Date'])
            filtered_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]

            if 'Marketcap' in filtered_df.columns:
                avg_market_cap = filtered_df['Marketcap'].mean()
                market_cap_data.append({'coin': coin, 'avgMarketCap': avg_market_cap})
            else:
                print(f"Marketcap data not found for {coin}.")

    # Check if market_cap_data is empty
    if not market_cap_data:
        print("No market cap data found for the selected coins and date range.")
        return []

    # Normalize the average market capitalizations
    max_market_cap = max(data['avgMarketCap'] for data in market_cap_data)
    for data in market_cap_data:
        data['avgMarketCap'] = data['avgMarketCap'] / max_market_cap if max_market_cap > 0 else 0

    return market_cap_data


cc = calculate_avg_market_cap('Bitcoin', '2021-01-01', '2021-12-31')
print(cc)
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







