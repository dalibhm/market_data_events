import logging
from dataclasses import dataclass, asdict, fields

from ibapi.contract import Contract as IbContract, ContractDetails as IbContractDetails

logger = logging.getLogger(__name__)


class Instrument:
    def __init__(self, symbol: str, conId):
        self.symbol = str(symbol)
        self.conId = conId
        self._contract = None
        self._contract_details = None
        self._derivative_sec_types = None
        self.events = []

    def __repr__(self):
        return f'Instrument({self.symbol})'

    @property
    def contract(self):
        return self._contract

    # @property
    # def symbol(self):
    #     return self.symbol

    def add_contract(self, contract):
        if self._contract is None:
            self._contract = Contract.from_ib(contract)
        else:
            msg = f'Contract for {self} already in database'
            logger.warning(msg)

    def add_derivativeSecTypes(self, derivativeSecTypes):
        if self._derivative_sec_types is None:
            self._derivative_sec_types = DerivativeSecTypes(self._contract.conId, derivativeSecTypes)
        else:
            msg = f'DerivativeSecTypes for {self} already in database'
            logger.warning(msg)

    def __repr__(self):
        return f"Instrument({self.symbol}, {self.conId})"


# @dataclass
class Contract:
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
    comboLegs = None  # type: list<ComboLeg>
    deltaNeutralContract = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in fields(Contract):
                setattr(self, key, value)
    fields = [
        'conId', 'symbol', 'secType', 'lastTradeDateOrContractMonth', 'strike', 'right', 'multiplier',
        'exchange', 'primaryExchange', 'currency', 'localSymbol', 'tradingClass', 'includeExpired', 'secIdType',
        'secId', 'comboLegsDescrip', 'comboLegs', 'deltaNeutralContract'
    ]
    #
    # def __init__(self, **kwargs):
    #     self.conId = 0
    #     self.symbol = ""
    #     self.secType = ""
    #     self.lastTradeDateOrContractMonth = ""
    #     self.strike = 0.  # float !!
    #     self.right = ""
    #     self.multiplier = ""
    #     self.exchange = ""
    #     self.primaryExchange = ""  # pick an actual (ie non-aggregate) exchange that the contract trades on.  DO NOT SET TO SMART.
    #     self.currency = ""
    #     self.localSymbol = ""
    #     self.tradingClass = ""
    #     self.includeExpired = False
    #     self.secIdType = ""  # CUSIP;SEDOL;ISIN;RIC
    #     self.secId = ""
    #
    #     # combos
    #     self.comboLegsDescrip = ""  # type: str; received in open order 14 and up for all combos
    #     self.comboLegs = None  # type: list<ComboLeg>
    #     self.deltaNeutralContract = None
    #
    #     for name, value in kwargs.items():
    #         setattr(self, name, value)

    @classmethod
    def from_ib(cls, ib_contract: IbContract):
        out = cls()
        for field in fields(cls):
            name = field.name
            setattr(out, name, getattr(ib_contract, name))
        return out

    def __str__(self):
        s = ",".join((
            str(self.conId),
            str(self.symbol),
            str(self.secType),
            str(self.lastTradeDateOrContractMonth),
            str(self.strike),
            str(self.right),
            str(self.multiplier),
            str(self.exchange),
            str(self.primaryExchange),
            str(self.currency),
            str(self.localSymbol),
            str(self.tradingClass),
            str(self.includeExpired),
            str(self.secIdType),
            str(self.secId)))
        s += "combo:" + self.comboLegsDescrip

        if self.comboLegs:
            for leg in self.comboLegs:
                s += ";" + str(leg)

        if self.deltaNeutralContract:
            s += ";" + str(self.deltaNeutralContract)

        return s

    def __repr__(self):
        return f"Contract({str(self)})"

    # @property
    # def ib_contract(self):
    #     ib_contract = IbContract()
    #     for field in self.fields:
    #         setattr(ib_contract, field, getattr(self, field))
    #     return ib_contract

    # @classmethod
    # def from_dict(cls, dictionary: dict):
    #     contract = Contract()
    #     for key, value in dictionary.items():
    #         if key in cls.fields:
    #             setattr(contract, key, value)
    #     return contract


# def ib_contract_from_dict(dictionary: dict):
#     contract = IbContract()
#     for key, value in dictionary.items():
#         if key in Contract.fields:
#             setattr(contract, key, value)
#     return contract


class DerivativeSecTypes:
    def __init__(self, conId, derivativeSecTypes):
        self.conId = conId
        self.CFD = False
        self.OPT = False
        self.IOPT = False
        self.WAR = False
        self.BAG = False

        for name in derivativeSecTypes:
            setattr(self, name, True)


@dataclass
class ContractDetails:
    contract_id: int
    marketName: str
    minTick: float = 0.
    orderTypes: str = ""
    validExchanges: str = ""
    priceMagnifier: int = 0
    underConId: int = 0
    longName: str = ""
    contractMonth: str = ""
    industry: str = ""
    category: str = ""
    subcategory: str = ""
    timeZoneId: str = ""
    tradingHours: str = ""
    liquidHours: str = ""
    evRule: str = ""
    evMultiplier: int = 0
    mdSizeMultiplier: int = 0
    aggGroup: int = 0
    underSymbol: str = ""
    underSecType: str = ""
    marketRuleIds: str = ""
    secIdList = None
    realExpirationDate: str = ""
    lastTradeTime: str = ""
    # BOND values
    cusip: str = ""
    ratings: str = ""
    descAppend: str = ""
    bondType: str = ""
    couponType: str = ""
    callable: bool = False
    putable: bool = False
    coupon: int = 0
    convertible: bool = False
    maturity: str = ""
    issueDate: str = ""
    nextOptionDate: str = ""
    nextOptionType: str = ""
    nextOptionPartial: bool = False
    notes: str = ""

    @classmethod
    def from_ib(cls, ib_contract_details: IbContractDetails):
        out = cls()
        for name, value in asdict(out).items:
            setattr(out, name, getattr(ib_contract_details, name))
        return out
