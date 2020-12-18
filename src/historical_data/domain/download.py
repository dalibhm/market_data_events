from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

# from historical_data.domain.request import Request


@dataclass(unsafe_hash=True)
class RequestData:
    creation_time: str = datetime.now()
    request_time: str = None
    response_start_time: str = None
    response_end_time: str = None
    actual_start_date: str = None  # to compare to the ones sent by the request
    actual_end_date: str = None  # to compare to the ones sent by the request
    submitted: bool = False
    complete: bool = False


class Download:
    def __init__(self, id, contract_id, bar_size, what_to_show, use_rth, start_date, end_date):
        self.id = id
        self.contract_id = contract_id
        self.bar_size = bar_size
        self.what_to_show = what_to_show
        self.use_rth = use_rth
        self.start_date = start_date
        self.end_date = end_date

        self.request = Request(self)
        self.request_data = RequestData()

        self.data = []  # List[BarData]
        # Think about putting the data in another class

    def __repr__(self):
        return f'<Download {self.id} {self.bar_size} {self.what_to_show} {self.use_rth} {self.start_date} -> {self.end_date}>'

    def __eq__(self, other):
        if not isinstance(other, Download):
            return False
        return other.start_date == self.start_date \
               and other.end_date == self.end_date \
               and other.bar_size == self.bar_size \
               and other.what_to_show == self.what_to_show \
               and other.use_rth == self.use_rth

    def __hash__(self):
        return hash(self.bar_size + self.what_to_show + self.use_rth + self.start_date + self.end_date)

    def same_parameters(self, other: Download):
        return other.bar_size == self.bar_size \
               and other.what_to_show == self.what_to_show \
               and other.use_rth == self.use_rth


@dataclass(unsafe_hash=True)
class BarData:
    run_id: str
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    wap: float
    count: int
