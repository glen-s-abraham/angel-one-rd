import os
import pyotp
from logzero import logger
from dotenv import load_dotenv, find_dotenv
from SmartApi import SmartConnect
from historic_utility import HistoricUtility
from connection_utils import ConnectionUtility
from instrument_utility import InstrumentUtility
from instrument_utility import MarketType
from instrument_utility import MarketMode
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

instrument_utility = InstrumentUtility()

connection_utility = ConnectionUtility()

smart_api = connection_utility.get_client_session()

feed_token = smart_api.getfeedToken()


smart_web_socket = connection_utility.get_ws_client_session()

correlation_id = "abc123"

watchlist = [
    instrument_utility.build_stream_token_param(
        exchange_type=MarketType.NSE_CM, stock_symbols=["INFY", "RELIANCE"]
    )
]

print(watchlist)


def on_data(wsapp, message):
    logger.info("Ticks: {}".format(message))
    # close_connection()


def on_open(wsapp):
    logger.info("on open")
    smart_web_socket.subscribe(correlation_id, MarketMode.DEPTH_20.value, watchlist)
    # sws.unsubscribe(correlation_id, mode, token_list1)


def on_error(wsapp, error):
    logger.error(error)


def on_close(wsapp):
    logger.info("Close")


def close_connection():
    smart_web_socket.close_connection()


smart_web_socket.on_open = on_open
smart_web_socket.on_data = on_data
smart_web_socket.on_error = on_error
smart_web_socket.on_close = on_close

smart_web_socket.connect()
