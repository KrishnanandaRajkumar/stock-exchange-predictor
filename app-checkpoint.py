import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
import matplotlib.pyplot as plt

# Load the trained model
model = joblib.load("tesla_stock_predictor_model.pkl")

# Streamlit app
st.title("Stock Market Predictor")

# Input multiple stock symbols
st.write("### Enter Stock Symbols (comma-separated)")
stock_symbols_input = st.text_input("e.g., TSLA, AAPL, GOOGL", "TSLA")

# Split the input into a list of stock symbols
stock_symbols = [symbol.strip() for symbol in stock_symbols_input.split(",")]

# Date range selection
st.write("### Select Date Range for Predictions")
start_date = st.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))

# Fetch data and make predictions
if st.button("Predict"):
    try:
        # Initialize a dictionary to store predictions for all symbols
        all_predictions = {}

        # Loop through each stock symbol
        for symbol in stock_symbols:
            # Fetch stock data
            data = yf.download(symbol, start=start_date, end=end_date)
            
            # Check if data is empty
            if data.empty:
                st.warning(f"No data found for {symbol}. Skipping this symbol.")
                continue

            # Feature engineering
            data['MA_7'] = data['Close'].rolling(window=7).mean()
            data['MA_30'] = data['Close'].rolling(window=30).mean()
            data['Daily_Return'] = data['Close'].pct_change()
            data.dropna(inplace=True)

            # Prepare features
            X = data.drop(columns=['Close'])
            predictions = model.predict(X)

            # Store predictions in the dictionary
            all_predictions[symbol] = pd.DataFrame({
                'Date': data.index,
                'Predicted Price': predictions
            })

        # Check if any predictions were made
        if not all_predictions:
            st.error("No valid data found for any of the symbols. Please try again.")
        else:
            # Display predictions for all symbols
            st.write("### Predicted Stock Prices")

            # Show the graph
            st.write("#### Graph of Predicted Prices")
            fig, ax = plt.subplots(figsize=(12, 6))
            for symbol, predictions_df in all_predictions.items():
                ax.plot(predictions_df['Date'], predictions_df['Predicted Price'], label=symbol)
            ax.set_title("Predicted Stock Prices")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend()
            st.pyplot(fig)

            # Show the table for each symbol
            for symbol, predictions_df in all_predictions.items():
                st.write(f"#### Table of Predicted Prices for {symbol}")
                st.dataframe(predictions_df)

                # Show key statistics
                st.write(f"#### Key Statistics for {symbol}")
                st.write(f"- **Mean Predicted Price**: {predictions_df['Predicted Price'].mean():.2f}")
                st.write(f"- **Minimum Predicted Price**: {predictions_df['Predicted Price'].min():.2f}")
                st.write(f"- **Maximum Predicted Price**: {predictions_df['Predicted Price'].max():.2f}")

    except Exception as e:
        st.error(f"An error occurred: {e}")