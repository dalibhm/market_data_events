from dataclasses import dataclass
from datetime import datetime


class Command:
    created_on: datetime


@dataclass
class CreateContract(Command):
    conId: int = 0
    symbol: str = ""
    secType: str = ""
    lastTradeDateOrContractMonth: str = ""
    strike: float = 0.  # float !!
    right: str = ""
    multiplier: str = ""
    exchange: str = ""
    primaryExchange: str = ""  # pick an actual (ie non-aggregate) exchange that the contract trades on.  DO NOT SET TO SMART.
    currency: str = ""
    localSymbol: str = ""
    tradingClass: str = ""
    includeExpired: bool = False
    secIdType: str = ""  # CUSIP;SEDOL;ISIN;RIC
    secId: str = ""

    # combos
    comboLegsDescrip: str = ""  # type: str; received in open order 14 and up for all combos
    comboLegs: str = None  # type: list<ComboLeg>
    deltaNeutralContract: str = None
