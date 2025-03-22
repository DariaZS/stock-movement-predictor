import sys

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


# Function to get stock data
def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock price data using Yahoo Finance.
    :param ticker: Stock ticker symbol (e.g., 'AAPL' for Apple)
    :param start_date: Start date for historical data (format: 'YYYY-MM-DD')
    :param end_date: End date for historical data (format: 'YYYY-MM-DD')
    :return: DataFrame containing stock prices
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start = start_date, end = end_date)
    
    if data.empty:
        print(f"❌ No data found for {ticker}! Check the ticker symbol and dates.")
        sys.exit(1)
    return data

def plot_stock_data(ticker, df):
    """
    Plot Stock Price Moving Averages and Volatility"""
    df['MA7'] = df['Close'].rolling(window=7).mean()
    df['MA30'] = df['Close'].rolling(window=30).mean()
    df['Returns'] = df['Close'].pct_change()
    df['Volatility'] = df['Returns'].rolling(window=30).std()
    
    # --- Plot Price and Moving Averages ---
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label = "Closing Price", linewidth = 1.5)
    plt.plot(df.index, df['MA7'], label = "7-Day MA", linestyle = '--')
    plt.plot(df.index, df['MA30'], label = "3-Day MA", linestyle = '--')
    plt.title(f"{ticker} Stock Price + Moving Averages")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Plot Volatility ---
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Volatility'], color = 'red', label = "30-Day Volatility")
    plt.title(f"{ticker} Rolling Volatility")
    plt.xlabel('Date')
    plt.ylabel('Standard Deviation of Returns')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_multi_stock_comparison(stock_dict):
    """
    Plot normalized closing prices for multiple stocks on a single chart.
    :param stock_dict: Dictionary of {ticker: dataframe}"""

    plt.figure(figsize = (12, 6))

    for ticker, df in stock_dict.items():
        # Noramlize prices to start at 100
        norm_price = df['Close'] / df['Close'].iloc[0]*100
        plt.plot(df.index, norm_price, label=ticker)
    plt.title("Normalized Stock Price Comparison")
    plt.xlabel("Date")
    plt.ylabel("normalized Price (Start = 100)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()







if __name__ == '__main__':
    stock_data_dict = {}

    tickers_input = input("Enter the ticker symbols, comma-separated, e.g. AAPL, TSLA, GOOGL: ").strip()
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

    tickers = [ticker.strip() for ticker in tickers_input.split(",")]
    print(f"Fetching stock data for {', '.join(tickers)} from {start_date} to {end_date}") 

    for ticker in tickers:
        try:
            stock_data = fetch_stock_data(ticker, start_date, end_date)
            # Save data to CSV
            csv_filename = f"data/{ticker}_stock_data.csv"
            stock_data.to_csv(csv_filename)

            print(f"✅ Data saved to {csv_filename}")
            
            # Store for multi-stock comparison
            stock_data_dict[ticker] = stock_data

            # Plot individual stock data
            plot_stock_data(ticker, stock_data)
        except ValueError as ve:
            print(f"❌ Invalid date format: {ve}")
        except Exception as e:
            print(f"❌ Error fetching stock data: {e}")
    
    if len(stock_data_dict) >1 :
        plot_multi_stock_comparison(stock_data_dict)