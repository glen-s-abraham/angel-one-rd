import os
import pyotp
from logzero import logger
from dotenv import load_dotenv, find_dotenv
from SmartApi import SmartConnect
from historic_utility import HistoricUtility
from connection_utils import ConnectionUtility

load_dotenv(find_dotenv())

connection_utility = ConnectionUtility()


# api_key = os.environ.get("SMART_API_KEY", "")
# username = os.environ.get("ANGEL_ONE_CLIENT_ID", "")
# pwd = os.environ.get("ANGEL_ONE_PIN", "")

# smartApi = SmartConnect(api_key=api_key)

# try:
#     token = os.environ.get("ANGEL_ONE_TOTP_QR", "")
#     totp = pyotp.TOTP(token).now()
# except Exception as e:
#     logger.error("Invalid Token: The provided token is not valid.")
#     raise e

# correlation_id = "abcde"
# data = smartApi.generateSession(username, pwd, totp)


# if data["status"] == False:
#     logger.error(data)

smart_api = connection_utility.get_client_session()

historic_utils = HistoricUtility(smart_api_client=smart_api)


df = historic_utils.fetch_candle_data("INFY", days=2000)

# Check if the DataFrame is not empty
if not df.empty:
    print(f"Number of records fetched: {len(df)}")
    
    # Print the first and last index in a robust way
    print(f"First index: {df.index[0]}")
    print(f"Last index: {df.index[-1]}")
else:
    print("No data fetched. Please check the symbol or the date range.")

