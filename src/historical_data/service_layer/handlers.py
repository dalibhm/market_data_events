from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import date

from common import utils
from historical_data.domain.download import Download
from historical_data.domain import commands
from historical_data.domain.instrument import Instrument
from ..domain.download import Download

if TYPE_CHECKING:
    from . import unit_of_work


class InstrumenMissing(Exception):
    pass


def add_download(
        cmd: commands.CreateDownload,
        uow: unit_of_work.AbstractUnitOfWork
) -> Download:
    with uow:
        instrument = uow.instruments.get(symbol=cmd.symbol)
        if instrument is None:
            instrument = Instrument(symbol=cmd.symbol,
                                    contract_id=cmd.contract_id,
                                    downloads=[])
            uow.instruments.add(instrument)
            download_id = utils.generate_event_id()
            download = Download(id=download_id,
                                contract_id=cmd.contract_id,
                                bar_size=cmd.bar_size,
                                what_to_show=cmd.what_to_show,
                                use_rth=cmd.use_rth,
                                start_date=cmd.start_date,
                                end_date=cmd.end_date)
            instrument.downloads.append(download)
            uow.commit()
            return download

        get_downloads()
        download_id = utils.generate_event_id()
        download = Download(id=download_id,
                            contract_id=cmd.contract_id,
                            bar_size=cmd.bar_size,
                            what_to_show=cmd.what_to_show,
                            use_rth=cmd.use_rth,
                            start_date=cmd.start_date,
                            end_date=cmd.end_date)
        instrument.downloads.append(download)
        uow.commit()
        return download


# def add_download(
#         id: str, symbol: str, contract_id: str, bar_size: str, what_to_show: str,
#         use_rth: int, start_date: str, end_date: str,
#         uow: unit_of_work.AbstractUnitOfWork
# ) -> Download:
#     with uow:
#         instrument = uow.instruments.get(symbol=symbol)
#         if instrument is None:
#             instrument = instrument.Instrument(symbol=symbol, contract_id=contract_id, downloads=[])
#             uow.instruments.add(instrument)
#         download = historical_data.domain.download.Download(id, bar_size, what_to_show, use_rth, start_date, end_date)
#         instrument.downloads.append(download)
#         uow.commit()
#         return download

def get_downloads(cmd: commands.CreateDownload,
                  uow: unit_of_work.AbstractUnitOfWork
                  ) -> Download:
    download = Download(id, bar_size, what_to_show, use_rth, start_date, end_date)
    with uow:
        instrument = uow.instruments.get(contract_id=contract_id)
        if instrument is None:
            add_download(download)
            return download
        downloads_checked = instrument.check_download_dates_against_previous(download)
        uow.commit()
        return downloads_checked


# def get_downloads(
#         id: str, symbol: str, contract_id: str, bar_size: str, what_to_show: str,
#         use_rth: int, start_date: str, end_date: str,
#         uow: unit_of_work.AbstractUnitOfWork
# ) -> Download:
#     download = Download(id, bar_size, what_to_show, use_rth, start_date, end_date)
#     with uow:
#         instrument = uow.instruments.get(contract_id=contract_id)
#         if instrument is None:
#             add_download(download)
#             return download
#         downloads_checked = instrument.check_download_dates_against_previous(download)
#         uow.commit()
#         return downloads_checked


def download_historical_data(
        id: str, symbol: str, contract_id: str, bar_size: str, what_to_show: str,
        use_rth: int, start_date: str, end_date: str,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    download = Download(id, bar_size, what_to_show, use_rth, start_date, end_date)
    with uow:
        instrument = uow.instruments.get_by_id(contract_id=contract_id)
        if instrument is None:
            raise InstrumenMissing(f'Instrument missing from database {contract_id} {symbol}')
        instrument.check_download_dates_against_previous(download)
        # send download somehow
        uow.commit()
