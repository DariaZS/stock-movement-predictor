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

def plot_stock_data(ticker, stock_data):
    """
    Plot the closing stock price overtime.
    :param ticker: Stock ticker symbol
    :param stock_data: DataFrame containing stock data
    """
    plt.figure(figsize = ( 10, 5 ))
    plt.plot(stock_data.index, stock_data['Close'], label = f"{ticker} Closing Price")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f"{ticker} Stock Price Over Time")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    tickers_input = input("Enter the ticker symbols, comma-separated, e.g. APPL, TSLA, GOOGL: ").strip()
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
            
            # Plot the stock data
            plot_stock_data(ticker, stock_data)
        except ValueError as ve:
            print(f"❌ Invalid date format: {ve}")
        except Exception as e:
            print(f"❌ Error fetching stock data: {e}")
        