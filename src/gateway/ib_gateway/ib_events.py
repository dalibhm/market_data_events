from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

from gateway.domain.contract import Contract


@dataclass
class IbEvent:
    created_on: datetime

    def __init__(self, *args, **kwargs):
        self.created_on = datetime.now()

        for name in args:
            if name in asdict(self).keys():
                setattr(self, name, args[name])

        for name, value in kwargs.items():
            if name in asdict(self).keys():
                setattr(self, name, value)


@dataclass
class IbError(IbEvent):
    reqId: int = -1
    errorCode: int = -1
    errorString: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class ConnectionAcknowledged(IbEvent):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class ConnectionClosed(IbEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class HistoricalDataReceived(IbEvent):
    reqId: int = -1
    date: str = ""
    open: float = -1
    high: float = -1
    low: float = -1
    close: float = -1
    volume: int = 0
    wap: float = 0
    count: int = 0

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class HistoricalDataEnded(IbEvent):
    reqId: int = -1
    start: str = ""
    end: str = ""

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class ContractDetailsReceived(IbEvent):
    reqId: int

    # contracts fields
    conId = 0
    symbol = ""
    secType = ""
    lastTradeDateOrContractMonth = ""
    strike = 0.  # float !!
    right = ""
    multiplier = ""
    exchange = ""
    primaryExchange = ""  # pick an actual (ie non-aggregate) exchange that the contract trades on.  DO NOT SET TO SMART.
    currency = ""
    localSymbol = ""
    tradingClass = ""
    includeExpired = False
    secIdType = ""  # CUSIP;SEDOL;ISIN;RIC
    secId = ""

    # contract details
    marketName = ""
    minTick = 0.
    orderTypes = ""
    validExchanges = ""
    priceMagnifier = 0
    underConId = 0
    longName = ""
    contractMonth = ""
    industry = ""
    category = ""
    subcategory = ""
    timeZoneId = ""
    tradingHours = ""
    liquidHours = ""
    evRule = ""
    evMultiplier = 0
    mdSizeMultiplier = 0
    aggGroup = 0
    underSymbol = ""
    underSecType = ""
    marketRuleIds = ""
    secIdList = None
    realExpirationDate = ""
    lastTradeTime = ""
    # BOND values
    cusip = ""
    ratings = ""
    descAppend = ""
    bondType = ""
    couponType = ""
    callable = False
    putable = False
    coupon = 0
    convertible = False
    maturity = ""
    issueDate = ""
    nextOptionDate = ""
    nextOptionType = ""
    nextOptionPartial = False
    notes = ""


@dataclass
class ContractDescriptionReceived(IbEvent):
    reqId: int
    contract: Contract
    derivativeSecTypes: List[str]

    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            setattr(self, name, value)


@dataclass
class ContractReceived(IbEvent):
    reqId: int
    contract: Contract
