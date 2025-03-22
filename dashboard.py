import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="📈 Stock Dashboard", layout="wide")

st.title("📊 Stock Price Dashboard")
st.markdown("Visualize stock trends, moving averages, and volatility.")

# Sidebar Inputs
tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL, TSLA, NVDA")
start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date", pd.to_datetime("2024-01-01"))

if st.button("Fetch & Plot"):
    tickers_list = [t.strip().upper() for t in tickers.split(",")]
    data_dict = {}

    for ticker in tickers_list:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            if df.empty:
                st.warning(f"No data found for {ticker}")
                continue

            df['MA7'] = df['Close'].rolling(window=7).mean()
            df['MA30'] = df['Close'].rolling(window=30).mean()
            df['Returns'] = df['Close'].pct_change()
            df['Volatility'] = df['Returns'].rolling(window=30).std()
            data_dict[ticker] = df

            # Individual Plot
            st.subheader(f"{ticker} Price + MAs")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df.index, df['Close'], label='Close')
            ax.plot(df.index, df['MA7'], linestyle='--', label='7-Day MA')
            ax.plot(df.index, df['MA30'], linestyle='--', label='30-Day MA')
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            # Volatility Plot
            st.subheader(f"{ticker} Volatility")
            fig2, ax2 = plt.subplots(figsize=(10, 3))
            ax2.plot(df.index, df['Volatility'], color='red', label='30-Day Volatility')
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Volatility")
            ax2.legend()
            ax2.grid(True)
            st.pyplot(fig2)

            # CSV Download button
            csv = df.to_csv(index = True).encode('utf-8')
            st.download_button(
                label=f"📥 Download {ticker} data as CSV",
                data = csv,
                file_name=f"{ticker}_stock_data.csv",
                mime='text/csv',
            )

        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")

    # Multi-Stock Comparison Plot
    if len(data_dict) > 1:
        st.subheader("📊 Normalized Stock Comparison")
        fig, ax = plt.subplots(figsize=(12, 5))
        for t, d in data_dict.items():
            norm = d["Close"] / d["Close"].iloc[0] * 100
            ax.plot(d.index, norm, label=t)
        ax.set_title("Normalized Closing Prices (Start = 100)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)