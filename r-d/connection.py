import os
import pyotp
from logzero import logger
from dotenv import load_dotenv, find_dotenv
from SmartApi import SmartConnect
from historic_utility import HistoricUtility

load_dotenv(find_dotenv())

api_key = os.environ.get("SMART_API_KEY", "")
username = os.environ.get("ANGEL_ONE_CLIENT_ID", "")
pwd = os.environ.get("ANGEL_ONE_PIN", "")

smartApi = SmartConnect(api_key=api_key)

try:
    token = os.environ.get("ANGEL_ONE_TOTP_QR", "")
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)


print(data)

if data["status"] == False:
    logger.error(data)


historic_utils = HistoricUtility(smart_api_client=smartApi)

print(
    historic_utils.fetch_candle_data(
        "INFY",
        fromdate="2024-12-19 09:15",
        todate="2024-12-19 15:15",
    )
)

print(historic_utils.fetch_candle_data("INFY", days=30))
