from __future__ import annotations

from typing import List

from historical_data.domain.download import Download
from historical_data.domain.events_old import SubmitRequest


class Instrument:
    def __init__(self, symbol: str, contract_id: str, downloads: List[Download] = None):
        """
        :param symbol: for information purpose only
        :param contract_id: unique identifier of a stock
        :param downloads: list of downloads already run for the contract
        """
        self.symbol = symbol
        self.contract_id = contract_id
        self.downloads = downloads or []
        self.events = []

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

# @dataclass(unsafe_hash=True)
