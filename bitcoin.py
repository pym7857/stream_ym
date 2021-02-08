import streamlit as st
from cryptocmd import CmcScraper
import plotly.express as px
from datetime import datetime

st.write('# 비트코인 Web App :) ')

st.sidebar.header('Menu')

name = st.sidebar.selectbox('Name', ['BTC', 'ETH', 'USDT']) # selectbox의 이름은 Name, 내용물은 ['BTC', 'ETH', 'USDT']

# streamlit은 날짜입력도 지원합니다.
start_date = st.sidebar.date_input('Start date', datetime(2021, 1, 1))
end_date = st.sidebar.date_input('End date', datetime(2021, 1, 7))

# CmcScraper : Coinmarketapp.com의 코인 데이터를 크롤링한다. (https://coinmarketcap.com)
scraper = CmcScraper(name, start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y')) # '%d-%m-%Y' 와 같이 거꾸로 해주어야 합니다.
df = scraper.get_dataframe()

fig_close = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title='Price')
fig_volume = px.line(df, x='Date', y=['Volume'], title='Volume')

st.plotly_chart(fig_close)
st.plotly_chart(fig_volume)