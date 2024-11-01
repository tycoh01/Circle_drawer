import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from stocktrends import Renko

# Step 1: Fetch NVIDIA historical data
nvidia_data = yf.download("NVDA", start="2023-01-01", end="2024-11-1")

# Step 2: Calculate MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    data['EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

# Step 3: Prepare DataFrame for Renko Calculation
def prepare_renko_data(data):
    macd_data = data[['MACD']].dropna().copy()  # Keep only MACD and drop NaN values
    # Create OHLC columns by setting them to MACD values
    macd_data['open'] = macd_data['MACD']
    macd_data['high'] = macd_data['MACD']
    macd_data['low'] = macd_data['MACD']
    macd_data['close'] = macd_data['MACD']
    macd_data.reset_index(inplace=True)  # Reset index to ensure Renko calculations work correctly
    macd_data.rename(columns={'Date': 'date'}, inplace=True)  # Rename index to date if necessary
    macd_data['date'] = pd.to_datetime(macd_data['date'])  # Ensure the date column is in datetime format
    return macd_data

# Step 4: Calculate Renko for MACD with a Fixed Brick Size
def calculate_renko(data, brick_size=0.5):
    # Include 'date' column while passing data to Renko
    renko_df = Renko(data[['date', 'open', 'high', 'low', 'close']])
    renko_df.brick_size = brick_size
    renko_data = renko_df.get_ohlc_data()
    return renko_data

# Step 5: Plot Renko Chart and Print Colors
def plot_and_print_renko(renko_data):
    colors = {'up': 'green', 'down': 'red'}
    fig, ax = plt.subplots(figsize=(12, 6))
    brick_colors = []

    for i, row in renko_data.iterrows():
        color = colors['up'] if row['uptrend'] else colors['down']
        ax.bar(row['date'], row['close'] - row['open'], width=0.5, bottom=row['open'], color=color)
        brick_colors.append(color)

    #ax.set_title('Renko Chart of MACD for NVIDIA')
    #plt.xlabel('Date')
    #plt.ylabel('MACD Value')
    #plt.grid()
    #plt.show()

    # Print the Renko brick colors
    print("Renko Brick Colors: ", brick_colors)

# Combine Steps
nvidia_macd_data = calculate_macd(nvidia_data)
prepared_renko_data = prepare_renko_data(nvidia_macd_data)
renko_data_macd = calculate_renko(prepared_renko_data, brick_size=0.5)
plot_and_print_renko(renko_data_macd)
