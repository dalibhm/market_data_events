from dataclasses import dataclass, fields
from typing import List

from gateway.domain.contract_v0 import Contract
from gateway.ib_gateway import ib_commands
from gateway.ib_gateway.ib_events import HistoricalDataEnded
from gateway.data_structures.historical_data import HistoricalData
from gateway.params.historical_request import HistoricalParams


@dataclass
class Event:
    pass


@dataclass
class HistoricalRequest:
    conId: int = -1
    endDateTime: str = ''
    durationStr: str = ''
    barSizeSetting: str = ''
    whatToShow: str = ''
    useRTH: int = -1
    formatDate: int = -1
    keepUpToDate: bool = False

    @classmethod
    def from_command(cls, cmd: ib_commands.RequestHistoricalData):
        out = cls()
        for field in fields(cls):
            name = field.name
            setattr(out, name, getattr(cmd, name))
        return out


@dataclass
class DataSummary:
    start_date: str
    end_date: str
    data_start_date: str
    data_end_date: str
    data_points_number: int

    @classmethod
    def from_historical_data(cls, historical_data: HistoricalData, historical_data_ended: HistoricalDataEnded):
        return cls(
            start_date=historical_data_ended.start,
            end_date=historical_data_ended.end,
            data_start_date=historical_data.start_date(),
            data_end_date=historical_data.end_date(),
            data_points_number=historical_data.data_points_number()
        )


@dataclass
class HistoricalRequestProcessed(Event):
    contract: Contract
    params: HistoricalParams
    data_summary: DataSummary
