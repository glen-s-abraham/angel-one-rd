import pandas as pd
import datetime as dt
from instrument_utility import InstrumentUtility
from SmartApi import SmartConnect


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
        response = self.__smart_api_client.getCandleData(params)
        if "data" not in response or not response["data"]:
            raise Exception("No data found in response")

        # Convert response data to a DataFrame
        df = pd.DataFrame(
            response["data"], columns=["date", "open", "high", "low", "close", "volume"]
        )
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index)  # Ensure date column is datetime type
        df.index = df.index.tz_localize(None)

        return df

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
        if days is not None:
            # Calculate fromdate and todate based on days
            todate = dt.datetime.today().strftime("%Y-%m-%d %H:%M")
            print(todate)
            fromdate = (dt.datetime.today() - dt.timedelta(days=int(days))).strftime(
                "%Y-%m-%d %H:%M"
            )
            print(fromdate)
        elif fromdate is None or todate is None:
            raise ValueError(
                "Either 'days' or both 'fromdate' and 'todate' must be provided"
            )

        return self.__fetch_candle_data(symbol, fromdate, todate, exchange, interval)
