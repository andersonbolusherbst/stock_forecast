import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START ="2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")
st.subheader("This is an example of Time-Series Forecasting")

stocks = ("AAPL","GOOGL","TSLA","GME","NFLX","ARKK","NDAQ","SPX","BTC-USD","ETH-USD","ADA-USD","CL=F") #Could swap IEX stock info here
selected_stock = st.selectbox("Select dataset for prediction", stocks)

n_years =st.slider("Years of prediction:",1, 4)
period = n_years * 365 


#cache data
@st.cache
def load_data(ticker):
    data = yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data...")
data = load_data(selected_stock)
data_load_state = st.text("Loading data... complete!")

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#forecasting with fbprohet
df_train =data[['Date','Close']]
df_train = df_train.rename(columns={"Date":"ds","Close":"y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.subheader('The Forecast')
fig1 =plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.subheader('Forecast Components')
fig2=m.plot_components(forecast)
st.write(fig2)
