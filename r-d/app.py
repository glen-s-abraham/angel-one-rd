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
from order_utility import (
    OrderCreateParams,
    ORDER_DURATION,
    ORDER_EXCHANGE,
    ORDER_TYPE,
    ORDER_VARIETY,
    OrderUtility,
    PRODUCT_TYPE,
    TRANSACTION_TYPE,
)

instrument_utility = InstrumentUtility()

connection_utility = ConnectionUtility()

smart_api = connection_utility.get_client_session()

feed_token = smart_api.getfeedToken()


smart_web_socket = connection_utility.get_ws_client_session()

correlation_id = "abc123"

watchlist = [
    instrument_utility.build_stream_token_param(
        exchange_type=MarketType.NSE_CM, stock_symbols=["TATAPOWER", "COALINDIA"]
    )
]

print(watchlist)


def on_data(wsapp, message):
    logger.info("Ticks: {}".format(message))
    # close_connection()


def on_open(wsapp):
    logger.info("on open")
    smart_web_socket.subscribe(correlation_id, MarketMode.SNAP_QUOTE.value, watchlist)
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

# smart_web_socket.connect()

# Order placing example
order_utility = OrderUtility(smart_api)

normal_order_params = OrderCreateParams(
    variety=ORDER_VARIETY.NORMAL,
    tradingsymbol="SBIN-EQ",
    symboltoken="3045",
    transactiontype=TRANSACTION_TYPE.BUY,
    exchange=ORDER_EXCHANGE.NSE,
    ordertype=ORDER_TYPE.LIMIT,
    producttype=PRODUCT_TYPE.INTRADAY,
    duration=ORDER_DURATION.DAY,
    price=19500,
    squareoff=0,
    stoploss=0,
    quantity=1,
)

# res = order_utility.place_order(order_details=normal_order_params)
# res = order_utility.cancel_order(
#     order_id="250101000696373", variety=ORDER_VARIETY.NORMAL
# )


stoploss_order_params = OrderCreateParams(
    variety=ORDER_VARIETY.STOPLOSS,
    tradingsymbol="SBIN-EQ",
    symboltoken="3045",
    transactiontype=TRANSACTION_TYPE.BUY,
    exchange=ORDER_EXCHANGE.NSE,
    ordertype=ORDER_TYPE.STOPLOSS_LIMIT,
    producttype=PRODUCT_TYPE.INTRADAY,
    duration=ORDER_DURATION.DAY,
    price=19700,
    triggerprice=19700,
    squareoff=0,
    stoploss=0,
    quantity=1,
) 

robo_order_params=OrderCreateParams(
    variety=ORDER_VARIETY.ROBO,
    tradingsymbol="SBIN-EQ",
    symboltoken="3045",
    ordertype=ORDER_TYPE.LIMIT,
    transactiontype=TRANSACTION_TYPE.BUY,
    exchange=ORDER_EXCHANGE.NSE,
    producttype=PRODUCT_TYPE.BO,
    duration=ORDER_DURATION.DAY,
    price=19700,
    stoploss=10,
    squareoff=30,
    quantity=1
    
) 


res = order_utility.place_order(order_details=robo_order_params)
# res = order_utility.get_ltp(symbol="SBIN-EQ",token="3045")

print(res)
