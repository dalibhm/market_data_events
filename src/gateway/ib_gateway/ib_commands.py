from dataclasses import dataclass
from datetime import datetime

from historical_data.domain.data import Contract


@dataclass
class IbCommand:
    created_on: datetime

    def __init__(self, **kwargs):
        self.created_on = datetime.now()
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)


@dataclass
class RequestMatchingSymbols(IbCommand):
    reqId: int
    symbol: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class RequestHistoricalData(IbCommand):
    reqId: int
    conId: int
    endDateTime: str
    durationStr: str
    barSizeSetting: str
    whatToShow: str
    useRTH: int
    formatDate: int
    keepUpToDate: bool
    chartOptions: list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
