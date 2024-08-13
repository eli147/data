import streamlit as st
import requests
import pandas as pd


def run():
    st.title('Time Series Data')
    api_key = 'DE76ZJ5LM8Q0ZR5K'

    symbol = st.text_input('Enter the stock symbol', 'AAPL')

    if api_key and symbol:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()

        if 'Time Series (Daily)' in data:
            # Extract the time series data
            time_series = data['Time Series (Daily)']

            # Convert the data into a DataFrame
            df = pd.DataFrame(time_series).T
            df.index.name = 'Date'
            df.reset_index(inplace=True)

            # Display the DataFrame in the app
            st.dataframe(df)
        else:
            st.write('Error fetching data. Please check your API key and symbol.')

        st.write('Use the sidebar to navigate to other pages.')