from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from historical_data.domain.download import Download


@dataclass
class Request:
    conId: int
    endDateTime: str
    durationStr: str
    barSizeSetting: str
    whatToShow: str
    useRTH: int
    formatDate: int
    keepUpToDate: bool
    data_summary: DataSummary


class Instrument:
    def __init__(self, symbol: str, conId: str,
                 downloads: List[Download] = None,
                 requests: List[Request] = None):
        """
        :param symbol: for information purpose only
        :param contract_id: unique identifier of a stock
        :param downloads: list of downloads already run for the contract
        """
        self.symbol = symbol
        self.conId = conId
        self.downloads = downloads or []
        self.requests = requests or []
        self.events = []

    # @property
    # def conId(self):
    #     return self._conId

    # think about renaming to add_download
    # check with add_download in services to see where best to put the function
    def check_download_dates_against_previous(self, download: Download) -> List[Download]:
        """
        takes as input the dates we are interested in and the parameters of the download,
        checks against the database to see if there are any previous download and covers the gaps
        between the dates

        :param download: download input
        :return: download suggested after checking the instrument's previous downloads
        """
        if len(self.downloads) == 0:
            out = download
        else:
            start_dates = [d.start_date for d in self.downloads if download.same_parameters(d)]
            end_dates = [d.end_date for d in self.downloads if download.same_parameters(d)]
            earliest_date = sorted(start_dates)[0]
            latest_date = sorted(end_dates)[-1]
            if download.end_date > latest_date:
                out = Download(id=download.id,
                               bar_size=download.bar_size,
                               what_to_show=download.what_to_show,
                               use_rth=download.use_rth,
                               start_date=latest_date,
                               end_date=download.end_date)
            else:
                out = download
            self.downloads.append(out)
            for d in out:
                self.events.append(
                    SubmitRequest(tenant_id=self.contract_id,
                                  download_id=d.id,
                                  request_id=request_id))
        return [out]

    def add_request(self, request: Request):
        self.requests.append(request)

    def update_recent(self, endDateTime: str):
        latest_date_in_db = self.latest_date()
        end_date_time = datetime.strptime(date_string=endDateTime, format='%Y%m%d %H:%M:%S %Z')
        if latest_date_in_db >= end_date_time:
            return None
        return endDateTime

    def latest_date(self):
        return max([
            datetime.strptime(date_string=request.endDateTime, format='%Y%m%d %H:%M:%S %Z')
            for request in self.requests
        ])

    def update_old(self, endDateTime: str):
        latest_date_in_db = self.earliest_date()
        end_date_time = datetime.strptime(date_string=endDateTime, format='%Y%m%d %H:%M:%S %Z')
        if latest_date_in_db >= end_date_time:
            return None
        return endDateTime

    def earliest_date(self):
        return max([
            datetime.strptime(date_string=request.endDateTime, format='%Y%m%d %H:%M:%S %Z')
            for request in self.requests
        ])


# @dataclass(unsafe_hash=True)


@dataclass
class DataSummary:
    start_date: datetime
    end_date: datetime
    data_start_date: datetime
    data_end_date: datetime
    data_points_number: int
