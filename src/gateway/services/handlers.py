from gateway.domain import commands, events
from gateway.domain.contract import Instrument
from gateway.ib_gateway import ib_events, ib_commands
from gateway.services import unit_of_work
from gateway.services.ib_gateway_connection import IbGatewayConnection

import logging

logger = logging.getLogger(__name__)


# class ReqMatchingSymbolsHandler:
#     def __init__(self, uow, ib_gateway_connection):
#         self.uow = uow
#         self.ib_gateway_connection = ib_gateway_connection
#
#     def __call__(self, cmd: commands.RequestMatchingSymbols):
#         self.ib_gateway_connection.reqMatchingSymbols(reqId=cmd.reqId, symbol=cmd.symbol)

def reqMatchingSymbols(cmd: ib_commands.RequestMatchingSymbols,
                       ib_gateway_connection: IbGatewayConnection) -> None:
    ib_gateway_connection.reqMatchingSymbols(reqId=cmd.reqId, symbol=cmd.symbol)


def reqHistoricalData(cmd: ib_commands.RequestHistoricalData,
                      ib_gateway_connection: IbGatewayConnection) -> None:
    ib_gateway_connection.reqHistoricalData(reqId=cmd.reqId, contract=cmd.contract, endDateTime=cmd.endDateTime,
                                            durationStr=cmd.durationStr, barSizeSetting=cmd.barSizeSetting,
                                            whatToShow=cmd.whatToShow, useRTH=cmd.useRTH, formatDate=cmd.formatDate,
                                            keepUpToDate=cmd.keepUpToDate, chartOptions=cmd.chartOptions)
    # with uow:
    #     instrument = uow.instruments.get(symbol=cmd.symbol)
    #     if instrument is None:
    #         instrument = Instrument(symbol=cmd.symbol)
    #         uow.instruments.add(instrument)
    #     instrument.contracts.append(
    #         contract.ib_contract_from_dict(cmd.__dict__)
    #     )
    #     uow.commit()


def publish_matching_symbols(event):
    print(event)


# def publish_historical_data(event: events.HistoricalDataReceived, uow: unit_of_work.AbstractUnitOfWork) -> None:
#     pulsar_eventpublisher.publish(event)
#
#
# def publish_historical_ended(event: events.HistoricalDataEnded, uow: unit_of_work.AbstractUnitOfWork) -> None:
#     pulsar_eventpublisher.publish(event)
def write_contract_descriptions(event: events.ContractDescriptionReceived,
                                uow: unit_of_work.AbstractUnitOfWork) -> None:
    msg = f"Writing contract description for {event.contract}"
    logger.info(msg)
    with uow:
        instrument = uow.instruments.get_by_conId(conId=event.contract.conId)
        if instrument is None:
            instrument = Instrument(symbol=event.contract.symbol, conId=event.contract.conId)
            uow.instruments.add(instrument)
        instrument.add_contract(event.contract)
        instrument.add_derivativeSecTypes(event.derivativeSecTypes)
        uow.commit()
    # with uow:
    #     contract = event.contract
    #     add_contract(
    #         commands.CreateContract(contract=contract),
    #         uow=uow
    #     )
    #     instrument = uow.instruments.get_by_conId(conId=contract.conId)
    #     instrument.add_derivativeSecTypes(event.derivativeSecTypes)
    #     uow.commit()


def add_contract(cmd: commands.CreateContract, uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        instrument = uow.instruments.get_by_conId(conId=cmd.contract.conId)
        if instrument is None:
            instrument = Instrument(symbol=cmd.contract.symbol)
            uow.instruments.add(instrument)
        instrument.add_contract(cmd.contract)
        uow.commit()


def add_derivative_sec_types(cmd: commands.WriteDerivativeSecTypes, uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        instrument = uow.instruments.get_by_conId(conId=cmd.conId)
        if instrument is None:
            instrument = Instrument(symbol=cmd.symbol, conId=cmd.conId)
            uow.instruments.add(instrument)
        instrument.add_derivativeSecTypes(cmd.derivative_sec_type)
        uow.commit()



def log_message(event: ib_events.IbError) -> None:
    print(event)


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
    commands.WriteContract: add_contract,
    commands.WriteDerivativeSecTypes: add_derivative_sec_types,

    commands.CreateContract: add_contract,
    # commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]
