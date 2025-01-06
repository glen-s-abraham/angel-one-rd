import pandas as pd

from connection_utils import ConnectionUtility
from instrument_utility import InstrumentUtility
from historic_utility import HistoricUtility

instrument_utility = InstrumentUtility()

connection_utility = ConnectionUtility()

smart_api = connection_utility.get_client_session()

historic_utility = HistoricUtility(smart_api_client=smart_api)

tickers = [
    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIANPAINT",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BEL",
    "BPCL",
    "BHARTIARTL",
    "BRITANNIA",
    "CIPLA",
    "COALINDIA",
    "DRREDDY",
    "DUMMYITC",
    "EICHERMOT",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "Tc",
    "INDUSINDBK",
    "INFY",
    "JSWSTEEL",
    "KOTAKBANK",
    "iT",
    "MARUTI",
    "NTPC",
    "NESTLEIND",
    "oNncc",
    "POWERGRID",
    "RELIANCE",
    "SBILIFE",
    "SHRIRAMFIN",
    "sBIN",
    "SUNPHARMA",
    "TCS",
    "TATACONSUM",
    "TATAMOTORS",
    "TATASTEEL",
    "TECHM",
    "TITAN",
    "TRENT",
    "ULTRACEMCO",
    "WIPRO",
]


backtest_start_date = "2024-06-01 09:15"
backtest_end_date = "2025-01-06 15:15"


def get_daily_data(symbol, start_date, end_date):
    data = historic_utility.fetch_candle_data(
        symbol=symbol, fromdate=start_date, todate=end_date, interval="ONE_DAY"
    )
    data["gap"] = ((data["open"] / data["close"].shift(1)) - 1) * 100
    data["avg_vol"] = data["volume"].rolling(10).mean().shift(1)
    return data


def get_top_gap_symbols(symbols_data):
    top_gap_symbols_data = {}
    for date in symbols_data[tickers[0]].index.to_list():
        temp = pd.Series()
        for ticker in symbols_data:
            try:
                temp.loc[ticker] = symbols_data[ticker].loc[date, "gap"]
            except:
                print(date,ticker)
        filtered_tickers = (
            abs(temp[abs(temp) > 1.5]).sort_values(ascending=False)[:5].index.to_list()
        )

        print(f"top 5 gap stocks on {date}")
        print(filtered_tickers)
        top_gap_symbols_data[date] = filtered_tickers
    return top_gap_symbols_data


hist_data_tickers = {}

for ticker in tickers:
    df = get_daily_data(
        symbol=tickers[0], start_date=backtest_start_date, end_date=backtest_end_date
    )
    hist_data_tickers[ticker] = df

get_top_gap_symbols(hist_data_tickers)