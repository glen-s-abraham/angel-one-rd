from dataclasses import dataclass
from typing import Optional
from enum import Enum


# Enum Definitions
class ORDER_VARIETY(Enum):
    NORMAL = "NORMAL"
    STOPLOSS = "STOPLOSS"
    AMO = "AMO"
    ROBO = "ROBO"
    NONE = None


class TRANSACTION_TYPE(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = None


class ORDER_TYPE(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOPLOSS_LIMIT = "STOPLOSS_LIMIT"
    STOPLOSS_MARKET = "STOPLOSS_MARKET"
    NONE = None


class PRODUCT_TYPE(Enum):
    CNC = "CNC"  # Cash and Carry
    MIS = "MIS"  # Margin Intraday Squareoff
    MARGIN = "MARGIN"
    INTRADAY = "INTRADAY"
    NONE = None


class ORDER_DURATION(Enum):
    DAY = "DAY"
    IOC = "IOC"
    NONE = None


class ORDER_EXCHANGE(Enum):
    BSE = "BSE"
    NSE = "NSE"
    NFO = "NFO"
    MCX = "MCX"
    BFO = "BFO"
    CDS = "CDS"
    NONE = None


@dataclass
class OrderCreateParams:
    """
    DTO for GTT Create Parameters with all fields optional.
    """

    variety: Optional[ORDER_VARIETY] = ORDER_VARIETY.NONE
    tradingsymbol: Optional[str] = None
    symboltoken: Optional[str] = None
    transactiontype: Optional[TRANSACTION_TYPE] = TRANSACTION_TYPE.NONE
    exchange: Optional[ORDER_EXCHANGE] = ORDER_EXCHANGE.NONE
    ordertype: Optional[ORDER_TYPE] = ORDER_TYPE.NONE
    producttype: Optional[PRODUCT_TYPE] = PRODUCT_TYPE.NONE
    duration: Optional[ORDER_DURATION] = ORDER_DURATION.NONE
    price: Optional[float] = None
    qty: Optional[int] = None  # Quantity
    disclosedqty: Optional[int] = None  # Disclosed quantity
    triggerprice: Optional[float] = None  # Trigger price
    timeperiod: Optional[int] = None  # Time period (in days)
    squareoff: Optional[float] = None  # Only for ROBO (Bracket Order)
    stoploss: Optional[float] = None  # Only for ROBO (Bracket Order)

    def __init__(
        self,
        variety: Optional[ORDER_VARIETY] = ORDER_VARIETY.NONE,
        tradingsymbol: Optional[str] = None,
        symboltoken: Optional[str] = None,
        transactiontype: Optional[TRANSACTION_TYPE] = TRANSACTION_TYPE.NONE,
        exchange: Optional[ORDER_EXCHANGE] = ORDER_EXCHANGE.NONE,
        ordertype: Optional[ORDER_TYPE] = ORDER_TYPE.NONE,
        producttype: Optional[PRODUCT_TYPE] = PRODUCT_TYPE.NONE,
        duration: Optional[ORDER_DURATION] = ORDER_DURATION.NONE,
        price: Optional[float] = None,
        qty: Optional[int] = None,
        quantity: Optional[int] = None,
        disclosedqty: Optional[int] = None,
        triggerprice: Optional[float] = None,
        timeperiod: Optional[int] = None,
        squareoff: Optional[float] = None,
        stoploss: Optional[float] = None,
    ):
        self.variety = variety
        self.tradingsymbol = tradingsymbol
        self.symboltoken = symboltoken
        self.transactiontype = transactiontype
        self.exchange = exchange
        self.ordertype = ordertype
        self.producttype = producttype
        self.duration = duration
        self.price = price
        self.qty = qty
        self.quantity = quantity
        self.disclosedqty = disclosedqty
        self.triggerprice = triggerprice
        self.timeperiod = timeperiod
        self.squareoff = squareoff
        self.stoploss = stoploss

    def to_dict(self) -> dict:
        """
        Converts the GTTCreateParams object into a dictionary.
        Excludes fields with None values and Enum.NONE.
        """
        return {
            key: (value.value if isinstance(value, Enum) else value)
            for key, value in self.__dict__.items()
            if value is not None
            and not (isinstance(value, Enum) and value == value.__class__.NONE)
        }


# Example Usage
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
    quantity=1
)
print(normal_order_params.to_dict())

gtt_params = OrderCreateParams(
    tradingsymbol="SBIN-EQ",
    symboltoken="3045",
    exchange=ORDER_EXCHANGE.NSE,
    producttype=PRODUCT_TYPE.MARGIN,
    transactiontype=TRANSACTION_TYPE.BUY,
    price=100000,
    qty=10,
    disclosedqty=10,
    triggerprice=200000,
    timeperiod=365,
)

# Print as dictionary
print(gtt_params.to_dict())
