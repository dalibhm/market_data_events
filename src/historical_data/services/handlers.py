from __future__ import annotations

from dataclasses import asdict
from typing import Optional, TYPE_CHECKING
from datetime import date

from common import utils
from historical_data.domain.download import Download
from historical_data.domain import commands
from historical_data.domain.instrument import Instrument, Request
from ..domain.download import Download

if TYPE_CHECKING:
    from . import unit_of_work


class InstrumenMissing(Exception):
    pass


def add_request(
        cmd: commands.AddRequest,
        uow: unit_of_work.AbstractUnitOfWork
) -> None:
    conId = cmd.request.conId
    symbol = cmd.symbol
    with uow:
        instrument = uow.instruments.get(conId=conId)
        if instrument is None:
            instrument = Instrument(conId=conId, symbol=symbol)
            uow.instruments.add(instrument)
        instrument.add_request(cmd.request)
        uow.commit()

def update_recent(
        request: Request,
        uow: unit_of_work.AbstractUnitOfWork
) -> Request:
    conId = request.conId
    with uow:
        instrument = uow.instruments.get(conId=conId)
        processed_request = instrument.update_recent(request.endDateTime)


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


EVENT_HANDLERS = {
    # events.Write: [write_contract_descriptions, log_message],
    # events.Allocated: [
    #     handlers.publish_allocated_event,
    #     handlers.add_allocation_to_read_model
    # ],
    # events.Deallocated: [
    #     handlers.remove_allocation_from_read_model,
    #     handlers.reallocate,
    # ],
    # events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    # commands.WriteContract: write_contract_descriptions,
    commands.AddRequest: add_request,
}  # type: Dict[Type[commands.Command], Callable]
