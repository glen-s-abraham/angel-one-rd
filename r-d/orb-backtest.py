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
    "EICHERMOT",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "INDUSINDBK",
    "INFY",
    "JSWSTEEL",
    "KOTAKBANK",
    "MARUTI",
    "NTPC",
    "NESTLEIND",
    "POWERGRID",
    "RELIANCE",
    "SBILIFE",
    "SHRIRAMFIN",
    "SBIN",
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

# Backtest date range
backtest_start_date = "2023-01-07 09:15"
backtest_end_date = "2025-01-07 15:15"


# Fetch daily data for a ticker
def get_daily_data(symbol, start_date, end_date):
    try:
        data = historic_utility.fetch_candle_data(
            symbol=symbol, fromdate=start_date, todate=end_date, interval="ONE_DAY"
        )
        if data is not None and not data.empty:
            data["gap"] = ((data["open"] / data["close"].shift(1)) - 1) * 100
            data["avg_vol"] = data["volume"].rolling(10).mean().shift(1)
        return data
    except Exception as e:
        print(f"Error fetching daily data for {symbol}: {e}")
        return None


# Fetch intraday data for a specific date
def get_intraday_data(symbol, date_stamp, interval="FIVE_MINUTE"):
    try:
        data = historic_utility.fetch_candle_data(
            symbol=symbol,
            fromdate=date_stamp.strftime("%Y-%m-%d") + " 09:15",
            todate=date_stamp.strftime("%Y-%m-%d") + " 15:15",
            interval=interval,
        )
        return data
    except Exception as e:
        print(f"Error fetching intraday data for {symbol} on {date_stamp}: {e}")
        return None


# Identify top gap symbols for each trading day
def get_top_gap_symbols(symbols_data):
    top_gap_symbols_data = {}

    for date in symbols_data[next(iter(symbols_data))].index:
        temp = pd.Series(dtype="float64")
        for ticker, df in symbols_data.items():
            if date in df.index:
                temp.loc[ticker] = df.at[date, "gap"]

        # Filter tickers with absolute gap > 1.5 and select top 5 by magnitude
        filtered_tickers = (
            temp[abs(temp) > 1.5].sort_values(ascending=False)[:5].index.to_list()
        )

        print(f"Top 5 gap stocks on {date}: {filtered_tickers}")
        top_gap_symbols_data[date] = filtered_tickers

    return top_gap_symbols_data


# Perform the backtest
def backtest(sorted_symbols, candle_data):
    date_stats = {}

    for date, tickers in sorted_symbols.items():
        date_stats[date] = {}

        for ticker in tickers:
            try:
                intraday_df = get_intraday_data(ticker, date)
                if intraday_df is None or intraday_df.empty:
                    continue

                high_price = intraday_df.iloc[0]["high"]
                low_price = intraday_df.iloc[0]["low"]
                open_price = None
                direction = None

                for i in range(1, len(intraday_df)):
                    current_row = intraday_df.iloc[i]

                    if (
                        current_row["volume"]
                        > 2 * candle_data[ticker].loc[date, "avg_vol"] / 75
                    ):
                        if open_price is None and current_row["high"] > high_price:
                            open_price = (
                                0.8 * intraday_df.iloc[i + 1]["open"]
                                + 0.2 * intraday_df.iloc[i + 1]["high"]
                            )
                            direction = "Long"

                        elif open_price is None and current_row["low"] < low_price:
                            open_price = (
                                0.8 * intraday_df.iloc[i + 1]["open"]
                                + 0.2 * intraday_df.iloc[i + 1]["low"]
                            )
                            direction = "Short"

                        if open_price:
                            if (
                                direction == "Long"
                                and current_row["high"] > high_price * 1.05
                            ):
                                date_stats[date][ticker] = (
                                    (high_price * 1.05 / open_price) - 1
                                ) * 100
                                break
                            elif direction == "Long" and current_row["low"] < low_price:
                                date_stats[date][ticker] = (
                                    (low_price / open_price) - 1
                                ) * 100
                                break
                            elif (
                                direction == "Short"
                                and current_row["low"] < low_price * 0.95
                            ):
                                date_stats[date][ticker] = (
                                    1 - (low_price * 0.95 / open_price)
                                ) * 100
                                break
                            elif (
                                direction == "Short"
                                and current_row["high"] > high_price
                            ):
                                date_stats[date][ticker] = (
                                    1 - (high_price / open_price)
                                ) * 100
                                break

            except Exception as e:
                print(f"Error backtesting {ticker} on {date}: {e}")

    return date_stats


# Fetch historical data for all tickers
hist_data_tickers = {}
for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    df = get_daily_data(ticker, backtest_start_date, backtest_end_date)
    if df is not None:
        hist_data_tickers[ticker] = df

# Get the top gap symbols
if hist_data_tickers:
    top_gap_symbols = get_top_gap_symbols(hist_data_tickers)

# Run the backtest
# Run the backtest
if top_gap_symbols:
    backtest_results = backtest(top_gap_symbols, hist_data_tickers)
    print("Backtest Results:")
    print(backtest_results)

    # Convert dictionary keys to strings
    backtest_results_str = {
        str(date): tickers for date, tickers in backtest_results.items()
    }

    # Save results to a file
    with open("backtest_results.json", "w") as file:
        import json

        json.dump(backtest_results_str, file, indent=4)
        print("Backtest results saved to backtest_results.json")
