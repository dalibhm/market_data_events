from dataclasses import dataclass
from datetime import datetime

from gateway.domain.contract_v0 import Contract
from gateway.params.historical_request import HistoricalParams


@dataclass
class IbCommand:
    created_on: datetime = datetime.now()

    # def __init__(self, **kwargs):
    #     self.created_on = datetime.now()
    #     if kwargs is not None:
    #         for key, value in kwargs.items():
    #             setattr(self, key, value)


@dataclass
class RequestMatchingSymbols(IbCommand):
    reqId: int = None
    symbol: str = None


@dataclass
class RequestHistoricalData(IbCommand):
    reqId: int = None
    contract: Contract = None
    params: HistoricalParams = None
