from datetime import datetime

from historical_data.domain.download import Download


class Request:
    reqId: int
    contract_id: str
    endDateTime: str
    durationStr: str
    barSizeSetting: str
    whatToShow: str
    useRTH: str
    formatDate: int
    keepUpToDate: bool

    def __init__(self, download: Download):
        self.reqId = None
        # self.contract_id = None
        self.endDateTime = download.end_date
        self.startDateTime = download.start_date
        self.durationStr = self.compute_duration()
        self.barSizeSetting = download.bar_size
        self.whatToShow = download.what_to_show
        self.useRTH = download.use_rth
        self.keepUpToDate = False

    def compute_duration(self) -> str:
        start_date = datetime.strptime(self.startDateTime, '%Y%m%d')
        end_date = datetime.strptime(self.endDateTime, '%Y%m%d')
        delta = end_date - start_date
        return f"{delta.days} D"

    def get_request(self) -> dict:
        return dict(runId=self.reqId,
                    endDateTime=self.endDateTime,
                    durationStr=self.durationStr,
                    barSizeSetting=self.barSizeSetting,
                    whatToShow=self.whatToShow,
                    useRTH=self.useRTH,
                    formatDate=1,
                    keepUpToDate=False)

