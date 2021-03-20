from gateway.domain import commands, events
from gateway.domain.contract import Instrument
from gateway.ib_gateway import ib_events, ib_commands
from gateway.services import unit_of_work
from gateway.services.ib_gateway_connection import IbGatewayConnection

import logging

logger = logging.getLogger(__name__)


def publish_matching_symbols(event):
    print(event)


def add_contract(cmd: commands.CreateContract, uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        instrument = uow.instruments.get_by_conId(conId=cmd.contract.conId)
        if instrument is None:
            instrument = Instrument(symbol=cmd.contract.symbol, conId=cmd.contract.conId)
        instrument.add_contract(cmd.contract)
        uow.instruments.add(instrument)
        uow.commit()


def add_derivative_sec_types(cmd: commands.WriteDerivativeSecTypes, uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        instrument = uow.instruments.get_by_conId(conId=cmd.conId)
        if instrument is None:
            instrument = Instrument(symbol=cmd.symbol, conId=cmd.conId)
        instrument.add_derivativeSecTypes(cmd.derivative_sec_type)
        uow.instruments.add(instrument)
        uow.commit()


def log_message(event) -> None:
    print(event)


EVENT_HANDLERS = {
    events.HistoricalRequestProcessed: [log_message]
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
    commands.WriteContract: add_contract,
    commands.WriteDerivativeSecTypes: add_derivative_sec_types,

    commands.CreateContract: add_contract,
    # commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]
