import pandas as pd

from connection_utils import ConnectionUtility
from instrument_utility import InstrumentUtility
from historic_utility import HistoricUtility

# Initialize utilities
instrument_utility = InstrumentUtility()
connection_utility = ConnectionUtility()
smart_api = connection_utility.get_client_session()
historic_utility = HistoricUtility(smart_api_client=smart_api)

# List of tickers
tickers = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BEL", "BPCL",
    "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DRREDDY",
    "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK",
    "INFY", "JSWSTEEL", "KOTAKBANK", "MARUTI", "NTPC",
    "NESTLEIND", "POWERGRID", "RELIANCE", "SBILIFE", "SHRIRAMFIN",
    "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS",
    "TATASTEEL", "TECHM", "TITAN", "TRENT", "ULTRACEMCO", "WIPRO",
]

# Backtest date range
backtest_start_date = "2024-06-01 09:15"
backtest_end_date = "2025-01-06 15:15"

# Fetch daily data for a ticker
def get_daily_data(symbol, start_date, end_date):
    data = historic_utility.fetch_candle_data(
        symbol=symbol, fromdate=start_date, todate=end_date, interval="ONE_DAY"
    )
    if data is not None and not data.empty:
        data["gap"] = ((data["open"] / data["close"].shift(1)) - 1) * 100
        data["avg_vol"] = data["volume"].rolling(10).mean().shift(1)
    return data

# Identify top gap symbols for each trading day
def get_top_gap_symbols(symbols_data):
    top_gap_symbols_data = {}

    for date in symbols_data[next(iter(symbols_data))].index.to_list():
        temp = pd.Series(dtype='float64')
        for ticker in symbols_data:
            try:
                temp.loc[ticker] = symbols_data[ticker].loc[date, "gap"]
            except KeyError:
                # Skip if data for the specific date or ticker is unavailable
                continue
        
        # Filter tickers with absolute gap > 1.5 and select top 5 by magnitude
        filtered_tickers = (
            temp[abs(temp) > 1.5]
            .sort_values(ascending=False)[:5]
            .index.to_list()
        )

        print(f"Top 5 gap stocks on {date}")
        print(filtered_tickers)

        top_gap_symbols_data[date] = filtered_tickers

    return top_gap_symbols_data

# Fetch historical data for all tickers
hist_data_tickers = {}
for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    df = get_daily_data(
        symbol=ticker, start_date=backtest_start_date, end_date=backtest_end_date
    )
    if df is not None:
        hist_data_tickers[ticker] = df

# Get the top gap symbols
if hist_data_tickers:
    top_gap_symbols = get_top_gap_symbols(hist_data_tickers)
