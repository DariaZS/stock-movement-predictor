import sys

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

# Example: Fetch Apple stock data from last year
'''
if __name__ == '__main__':
    ticker = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    print(f"Fetching stock data for {ticker} from {start_date} to {end_date}")
    stock_data = fetch_stock_data(ticker, start_date, end_date)

    # Save data to a CSV file
    stock_data.to_csv(f"data/{ticker}_stock_data.csv")

    print(f"✅ Stock data saved to data/{ticker}_stock_data.csv")
    print(stock_data.head()) # Display first few rows of data

'''

if __name__ == '__main__':
    ticker = input("Enter the ticker symbol: ").strip().upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

    print(f"Fetching stock data for {ticker} from {start_date} to {end_date}")

    try:
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        # Save data to CSV
        csv_filename = f"data/{ticker}_stock_data.csv"
        stock_data.to_csv(csv_filename)

        print(f"✅ Data saved to {csv_filename}")
        print(stock_data.head())
    except ValueError as ve:
        print(f"❌ Invalid date format: {ve}")
    except Exception as e:
        print(f"❌ Error fetching stock data: {e}")
        