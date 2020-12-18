from dataclasses import dataclass
from datetime import datetime


class Command:
    created_on: datetime


@dataclass
class CreateDownload(Command):
    def __init__(self):
        self.end_date = None
        self.start_date = None
        self.use_rth = None
        self.what_to_show = None
        self.bar_size = None

    symbol: str = ""
    contract_id: int = 0
    secType: str = ""
    lastTradeDateOrContractMonth: str = ""
    strike: float = 0.  # float !!
    right: str = ""
    # exchange: str = ""
    # primaryExchange: str = ""  # pick an actual (ie non-aggregate) exchange that the contract trades on.  DO NOT SET TO SMART.
    # currency: str = ""
    params 


@dataclass
class SubmitRequest(Command):
    tenant_id: str
    download_id: str
    request_id: int
    # bar_size: str
    # what_to_show: str
    # use_rth: int
    # start_date: str
    # end_date: str


@dataclass
class DownloadHistoricalData(Command):
    tenant_id: str
    download_id: str
    contact_id: str
    request_id: str
