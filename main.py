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
    return data

# Example: Fetch Apple stock data from last year
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

    