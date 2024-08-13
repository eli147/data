import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

def run():
    st.title('Alpha Vantage Time Series Dashboard')

    # API Key and Symbol Input
    api_key = 'DE76ZJ5LM8Q0ZR5K'
    symbol = st.text_input('Enter the stock symbol', 'AAPL')

    if api_key and symbol:
        # Fetch data from Alpha Vantage API
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()

        if 'Time Series (Daily)' in data:
            # Extract and process time series data
            time_series = data['Time Series (Daily)']
            df = pd.DataFrame(time_series).T
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df.index.name = 'Date'
            df.reset_index(inplace=True)

            # Ensure the Date column is in datetime format
            df['Date'] = pd.to_datetime(df['Date'])

            # Display data table
            st.subheader('Time Series Data')
            st.dataframe(df)

            # Plotting
            st.subheader('Stock Price Trend')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['4. close'], mode='lines', name='Close Price'))
            fig.update_layout(title=f'{symbol} Stock Price Trend', xaxis_title='Date', yaxis_title='Price')
            st.plotly_chart(fig)

            # Additional Analytics (Optional)
            st.subheader('Basic Statistics')
            st.write(df.describe())

        else:
            st.write('Error fetching data. Please check your API key and symbol.')

    st.sidebar.title('Navigation')
    st.sidebar.write('Use this dashboard to explore stock data. Enter a stock symbol and API key to get started.')
