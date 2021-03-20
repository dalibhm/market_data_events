from dataclasses import dataclass
from datetime import datetime

from ibapi.common import BarData as IbBarData


@dataclass
class BarData:
    date: str = ""
    open: float = 0.
    high: float = 0.
    low: float = 0.
    close: float = 0.
    volume: int = 0
    wap: float = 0
    barCount: int = 0
    average: float = 0.

    @classmethod
    def from_ib(cls, bar_data: IbBarData):
        return cls(**bar_data.__dict__)

    def __lt__(self, other):
        return datetime.strptime(self.date, '%Y%m%d') < datetime.strptime(other.date, '%Y%m%d')
