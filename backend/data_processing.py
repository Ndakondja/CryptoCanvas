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
    crypto_close_prices = pd.DataFrame()

    # Load Bitcoin data
    bitcoin_df = data_cache.get("coin_Bitcoin.csv")
    if bitcoin_df is not None:
        bitcoin_df['Date'] = pd.to_datetime(bitcoin_df['Date'])
        filtered_bitcoin_df = bitcoin_df[(bitcoin_df['Date'] >= start_date) & (bitcoin_df['Date'] <= end_date)]
        crypto_close_prices['Bitcoin'] = filtered_bitcoin_df.set_index('Date')['Close']

    # Load data for other selected coins
    for coin in selected_coins:
        if coin == 'Bitcoin':  # Skip Bitcoin as it's already added
            continue
        coin_df = data_cache.get(f"coin_{coin}.csv")
        if coin_df is not None:
            coin_df['Date'] = pd.to_datetime(coin_df['Date'])
            filtered_coin_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]
            crypto_close_prices[coin] = filtered_coin_df.set_index('Date')['Close']

    # Compute and return the correlation matrix
    return crypto_close_prices.corr()


   

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
    elif time_range == 'BTC Halving 2016-07-09':
        # Specific dates for the Bitcoin Halving event
        start_date = datetime.strptime("2016-04-09", '%Y-%m-%d')
        end_date = datetime.strptime("2016-10-09", '%Y-%m-%d')
    elif time_range == 'BTC Halving 2020-05-11':
        # Specific dates for the Bitcoin Halving event
        start_date = datetime.strptime("2020-03-11", '%Y-%m-%d')
        end_date = datetime.strptime("2020-08-11", '%Y-%m-%d')

    else:
        # Default case, can be adjusted as needed
        start_date = end_date - timedelta(days=6*30)

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def calculate_avg_market_cap(selected_coins, start_date, end_date):
    global data_cache
    market_cap_data = []

    # Calculate total market cap for all coins in the cache over the period
    total_market_cap = 0
    for coin_file in data_cache.keys():
        coin_df = data_cache[coin_file]
        coin_df['Date'] = pd.to_datetime(coin_df['Date'])
        filtered_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]

        if 'Marketcap' in filtered_df.columns:
            total_market_cap += filtered_df['Marketcap'].sum()

    # Calculate and normalize average market caps for selected coins
    for coin in selected_coins:
        file_name = f"coin_{coin}.csv"
        coin_df = data_cache.get(file_name)

        if coin_df is not None:
            coin_df['Date'] = pd.to_datetime(coin_df['Date'])
            filtered_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]

            if 'Marketcap' in filtered_df.columns:
                avg_market_cap = filtered_df['Marketcap'].mean()
                normalized_market_cap = (avg_market_cap / total_market_cap) * 100 if total_market_cap > 0 else 0
                market_cap_data.append({'coin': coin, 'avgMarketCap': normalized_market_cap})
            else:
                print(f"Marketcap data not found for {coin}.")

    return market_cap_data

import pandas as pd

def calculate_coin_stats(selected_coins, start_date, end_date):
    global data_cache
    coin_stats = []

    for coin in selected_coins:
        file_name = f"coin_{coin}.csv"
        coin_df = data_cache.get(file_name)

        if coin_df is not None:
            coin_df['Date'] = pd.to_datetime(coin_df['Date'])
            filtered_df = coin_df[(coin_df['Date'] >= start_date) & (coin_df['Date'] <= end_date)]

            if not filtered_df.empty and 'Close' in filtered_df.columns:
                average_price = filtered_df['Close'].mean()
                std_dev = filtered_df['Close'].std()

                # Percentage growth calculation
                start_price = filtered_df.iloc[0]['Close']
                end_price = filtered_df.iloc[-1]['Close']
                percentage_growth = ((end_price - start_price) / start_price) * 100

                coin_stats.append({
                    'coin': coin,
                    'average_price': average_price,
                    'std_dev': std_dev,
                    'percentage_growth': percentage_growth
                })
            else:
                print(f"Price data not found for {coin} in the specified date range.")
        else:
            print(f"Data for {coin} not found.")

    return coin_stats

# Example usage:
selected_coins = ['Bitcoin', 'Ethereum', 'XRP']
start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2021-12-31')
stats = calculate_coin_stats(selected_coins, start_date, end_date)
print(stats)



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








