from pickle import TRUE
from typing import Container
import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')


st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のぷしょんから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 100, 20)

st.write(f"""
### 過去　**{days}日間**のGAFA株価
""")

@st.cache

def get_data(days, tickers):
    df = pd.DataFrame()

    for company in tickers.keys():
    
    #company = 'apple'

        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df,hist])
    return df

st.sidebar.write("""
## 株価の指定範囲
""")

y_min, y_max = st.sidebar.slider(
    '株価範囲を指定してください',
    0.0, 3500.0, (0.0,3500.0)
)

tickers={
    'apple': 'AAPL',
    'meta': 'META',
    'google':'GOOGL',
    'microsoft':'MSFT',
    'netflix':'NFLX',
    'amazon': 'AMZN'
}

df = get_data(days, tickers)
companies = st.multiselect(
    '会社名を指定してください',
    list(df.index),
    ['google']
)

if not companies:
    st.error('少なくと一社は選んでください')
else:
    data = df.loc[companies]
    st.write("### 株価（USD）", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date']).rename(
        columns={'value':'stock Prices(USD)'}
    )
    chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[y_min,y_max])),
                color='Name:N'
            )
        )
    st.altair_chart(chart, use_container_width=True)
