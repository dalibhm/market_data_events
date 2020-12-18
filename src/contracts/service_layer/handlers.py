from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime

# from contracts.adapters import pulsar_eventpublisher
from contracts.domain import commands, contract
from contracts.domain.contract import Instrument
from contracts import views
from contracts.service_layer.events import RequestContract
from ibapi.contract import Contract

if TYPE_CHECKING:
    from contracts.service_layer import unit_of_work


class ContractAlreadyInDatabase(Exception):
    pass


class ContractNotInDatabase(Exception):
    pass


def add_contract(cmd: commands.CreateContract, uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        instrument = uow.instruments.get(symbol=cmd.symbol)
        if instrument is None:
            instrument = Instrument(symbol=cmd.symbol)
            uow.instruments.add(instrument)
        instrument.contracts.append(
            contract.ib_contract_from_dict(cmd.__dict__)
        )
        uow.commit()


def get_contract_by_symbol(symbol: str, uow: unit_of_work.AbstractUnitOfWork) -> Contract:
    with uow:
        instrument = uow.instruments.get(symbol=symbol)
        contract = instrument.get_contract()
    return contract


def request_contract_from_gateway(symbol: str, uow: unit_of_work.AbstractUnitOfWork):
    request = RequestContract(created_on=datetime.now(), symbol=symbol)
    pulsar_eventpublisher.publish('RequestContract', request)
