import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# Load data function
# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
#     df = df.sort_values('Date')
#     df.set_index('Date', inplace=True)
#     return df

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce')
    df.dropna(subset=['Date'], inplace=True)
    df = df.sort_values('Date')
    df.set_index('Date', inplace=True)
    return df

# Check stationarity
def check_stationarity(series):
    result = adfuller(series)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    if result[1] > 0.05:
        print("Series is NON-stationary.")
    else:
        print("Series is stationary.")

# Plot price series
def plot_price_series(df):
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['Price'], label='Brent Oil Price')
    plt.title('Brent Oil Price Over Time')
    plt.xlabel('Year')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()