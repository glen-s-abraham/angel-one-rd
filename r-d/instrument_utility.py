import urllib.request
import json


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


# Example usage
if __name__ == "__main__":
    utility = InstrumentUtility()

    # Example usage
    token = utility.token_lookup("INFY")
    if token:
        print(f"Token for INFY: {token}")

    symbol = utility.symbol_lookup("1594")
    if symbol:
        print(f"Symbol for token 1594: {symbol}")
