import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the trained model
model = joblib.load("tesla_stock_predictor_model.pkl")

# Streamlit app
st.title("Stock Market Predictor")

# Input stock symbol
stock_symbol = st.text_input("Enter Stock Symbol (e.g., TSLA):", "TSLA")

# Fetch data and make predictions
if st.button("Predict"):
    data = yf.download(stock_symbol, start="2020-01-01", end="2023-01-01")
    data["MA_7"] = data["Close"].rolling(window=7).mean()
    data["MA_30"] = data["Close"].rolling(window=30).mean()
    data["Daily_Return"] = data["Close"].pct_change()
    data.dropna(inplace=True)

    # Prepare features
    X = data.drop(columns=["Close"])
    predictions = model.predict(X)

    # Display predictions
    st.write("Predictions:")
    st.line_chart(predictions)
