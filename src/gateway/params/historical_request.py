from dataclasses import dataclass


class Params:
    pass


@dataclass
class HistoricalParams(Params):
    endDateTime: str
    durationStr: str
    barSizeSetting: str
    whatToShow: str
    useRTH: int
    formatDate: int
    keepUpToDate: bool
