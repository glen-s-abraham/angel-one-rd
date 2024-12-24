import urllib.request
import json
from enum import Enum
from typing import Literal, List


class MarketType(Enum):
    NSE_CM = 1  # NSE Cash Market
    NSE_FO = 2  # NSE Futures & Options
    BSE_CM = 3  # BSE Cash Market
    BSE_FO = 4  # BSE Futures & Options
    MCX_FO = 5  # MCX Futures & Options
    NCX_FO = 7  # NCX Futures & Options
    CDE_FO = 13  # CDE Futures & Options

    @classmethod
    def from_name(cls, name):
        """Get the integer value corresponding to the given name."""
        try:
            return cls[name.upper()].value
        except KeyError:
            raise ValueError(f"Invalid market type: {name}")


class MarketMode(Enum):
    LTP = 1  # Last Traded Price
    QUOTE = 2  # Quote
    SNAP_QUOTE = 3  # Snap Quote
    DEPTH_20 = 4  # 20-Depth

    @classmethod
    def from_name(cls, name):
        """Get the integer value corresponding to the given name."""
        try:
            return cls[name.upper().replace("-", "_")].value
        except KeyError:
            raise ValueError(f"Invalid data type: {name}")


class InstrumentUtility:
    def __init__(self):
        self.instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        self.instruments_list = []

    def fetch_instruments(self):
        """Fetch the instruments list from the specified URL."""
        try:
            with urllib.request.urlopen(self.instrument_url) as response:
                self.instruments_list = json.loads(response.read().decode("utf-8"))
                print(
                    f"Data fetched successfully. Total instruments: {len(self.instruments_list)}"
                )
        except urllib.error.URLError as e:
            print(f"Failed to fetch data: {e.reason}")
            self.instruments_list = []
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            self.instruments_list = []

    def token_lookup(self, symbol, exchange="NSE", segment="EQ"):
        """Look up the token for a given symbol, exchange, and segment."""
        if not self.instruments_list:
            print("Instrument list is empty. Fetching data...")
            self.fetch_instruments()

        if not self.instruments_list:
            print("Unable to fetch instruments list. Token lookup failed.")
            return None

        symbol_filter = (
            lambda x: x["name"] == symbol
            and x["exch_seg"] == exchange
            and x["symbol"].split("-")[-1] == segment
        )

        matches = list(filter(symbol_filter, self.instruments_list))
        if matches:
            return matches[0].get("token", None)  # Return the token of the first match
        else:
            print(
                f"No match found for symbol: {symbol}, exchange: {exchange}, segment: {segment}"
            )
            return None

    def symbol_lookup(self, token):
        """Look up the symbol for a given token."""
        if not self.instruments_list:
            print("Instrument list is empty. Fetching data...")
            self.fetch_instruments()

        if not self.instruments_list:
            print("Unable to fetch instruments list. Symbol lookup failed.")
            return None

        symbol_filter = lambda x: str(x["token"]) == str(token)

        matches = list(filter(symbol_filter, self.instruments_list))
        if matches:
            return matches[0].get("name", None)  # Return the name of the first match
        else:
            print(f"No match found for token: {token}")
            return None

    def build_stream_token_param(
        self, exchange_type: MarketType, stock_symbols: List[str] = []
    ):
        if not isinstance(exchange_type, MarketType):
            raise ValueError(
                f"Invalid exchange_type: {exchange_type}. Must be a valid MarketType."
            )

        token_param = {
            "exchangeType": exchange_type.value,
            "tokens": [],
        }
        for symbol in stock_symbols:
            token_param["tokens"].append(self.token_lookup(symbol=symbol))

        return token_param
