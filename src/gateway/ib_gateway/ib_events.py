from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

from gateway.data_structures.bar_data import BarData
from gateway.domain.contract_v0 import Contract


@dataclass
class IbEvent:
    created_on: datetime = datetime.now()


@dataclass
class IbError(IbEvent):
    reqId: int = -1
    errorCode: int = -1
    errorString: str = ""


@dataclass
class ConnectionAcknowledged(IbEvent):
    pass


@dataclass
class ConnectionClosed(IbEvent):
    pass


@dataclass
class HistoricalDataReceived(IbEvent):
    reqId: int = -1
    bar_data: BarData = None


@dataclass
class HistoricalDataEnded(IbEvent):
    reqId: int = -1
    start: str = ""
    end: str = ""


@dataclass
class ContractDetailsReceived(IbEvent):
    reqId: int = -1

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
    reqId: int = -1
    contract: Contract = None
    derivativeSecTypes: List[str] = None

    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            setattr(self, name, value)


@dataclass
class ContractReceived(IbEvent):
    reqId: int = -1
    contract: Contract = -1
