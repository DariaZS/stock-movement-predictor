import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
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
            st.subheader(f"{ticker} Price + Moving Averages (Interactive)")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA7'], mode='lines', name='7-Day MA'))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA30'], mode='lines', name='30-Day MA'))

            fig.update_layout(title=f"{ticker} Stock Price", xaxis_title="Date", yaxis_title="Price", hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)




            # Volatility Plot
            st.subheader(f"{ticker} Volatility (Interactive)")

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df['Volatility'], mode='lines', name='30-Day Volatility', line=dict(color='red')))
            fig2.update_layout(title=f"{ticker} Rolling Volatility", xaxis_title="Date", yaxis_title="Volatility", hovermode="x unified")

            st.plotly_chart(fig2, use_container_width=True)

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