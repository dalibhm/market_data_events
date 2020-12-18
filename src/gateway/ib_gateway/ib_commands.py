from dataclasses import dataclass
from datetime import datetime

from historical_data.domain.data import Contract


@dataclass
class IbCommand:
    created_on: datetime

    def __init__(self):
        self.created_on = datetime.now()


@dataclass
class RequestMatchingSymbols(IbCommand):
    reqId: int
    symbol: str


@dataclass
class RequestHistoricalData(IbCommand):
    reqId: int
    contract: Contract
    endDateTime: str
    durationStr: str
    barSizeSetting: str
    whatToShow: str
    useRTH: int
    formatDate: int
    keepUpToDate: bool
    chartOptions: list
