import pandas as pd
import datetime as dt
from instrument_utility import InstrumentUtility
from SmartApi import SmartConnect
import time


class HistoricUtility:
    def __init__(self, smart_api_client: SmartConnect):
        self.__instrument_utility = InstrumentUtility()
        self.__smart_api_client = smart_api_client

    def __build_request_params(
        self, symbol, fromdate, todate, exchange="NSE", interval="ONE_HOUR"
    ):
        """Build request parameters for fetching candle data."""
        symbol_token = self.__instrument_utility.token_lookup(symbol=symbol)
        if symbol_token is None:
            raise ValueError("Invalid Symbol")

        return {
            "exchange": exchange,
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": fromdate,
            "todate": todate,
        }

    def __fetch_candle_data(
        self, symbol, fromdate, todate, exchange="NSE", interval="ONE_HOUR"
    ):
        """Fetch candle data for a given symbol and parameters."""
        params = self.__build_request_params(
            symbol=symbol,
            fromdate=fromdate,
            todate=todate,
            exchange=exchange,
            interval=interval,
        )
        response = self.__smart_api_client.getCandleData(
            params,
        )

        if "data" not in response or not response["data"]:
            raise Exception("No data found in response")
        return response["data"]

    def fetch_candle_data(
        self,
        symbol,
        fromdate=None,
        todate=None,
        days=None,
        exchange="NSE",
        interval="ONE_HOUR",
    ):
        """
        Fetch candle data for a symbol.
        - If `days` is provided, calculate `fromdate` and `todate` automatically.
        - Otherwise, use the given `fromdate` and `todate`.
        """
        df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])

        if days is not None:
            # Calculate fromdate and todate based on days
            todate = dt.datetime.today().strftime("%Y-%m-%d %H:%M")
            fromdate = (dt.datetime.today() - dt.timedelta(days=int(days))).strftime(
                "%Y-%m-%d %H:%M"
            )
            fromdate = dt.datetime.strptime(fromdate, "%Y-%m-%d %H:%M")
            fromdate = dt.datetime(fromdate.year, fromdate.month, fromdate.day, 9, 15)
            fromdate = (dt.datetime.today() - dt.timedelta(days=int(days))).strftime(
                "%Y-%m-%d %H:%M"
            )

        elif fromdate is None or todate is None:
            raise ValueError(
                "Either 'days' or both 'fromdate' and 'todate' must be provided"
            )

        while True:
            # Wait out to override throttling
            time.sleep(0.5)

            print(f"Fetching data from {fromdate}-{todate}")

            # Fetch data for the current range
            data = None
            try:
                data = self.__fetch_candle_data(
                    symbol, fromdate, todate, exchange, interval
                )
            except:
                print("no data")
                data = None

            if not data:
                break

            # Create a temporary DataFrame
            temp_df = pd.DataFrame(
                data, columns=["date", "open", "high", "low", "close", "volume"]
            )
            temp_df["date"] = pd.to_datetime(
                temp_df["date"].str[:16], format="%Y-%m-%dT%H:%M"
            )

            # Append the temporary DataFrame to the main DataFrame
            df = pd.concat([temp_df, df], ignore_index=True)

            # Update the `todate` for the next iteration to fetch older data
            todate = temp_df["date"].iloc[0] - dt.timedelta(seconds=1)
            todate = todate.strftime("%Y-%m-%d %H:%M")

            # Break if all data is fetched
            if temp_df["date"].iloc[0] <= pd.to_datetime(fromdate):
                break

        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index)  # Ensure date column is datetime type
        df.index = df.index.tz_localize(None)  # Remove timezone information
        return df
