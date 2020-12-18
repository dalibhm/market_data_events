from queue import Queue
from typing import Union

from gateway.domain.contract import Contract
from gateway.domain import commands, events
from gateway.ib_gateway import ib_events, ib_commands
from gateway.services import views
from gateway.services.data_handlers.historical_data_manager import HistoricalDataManager
from gateway.services.ib_gateway_connection import IbGatewayConnection

import logging

logger = logging.getLogger(__name__)

IbMessage = Union[ib_commands.IbCommand, ib_events.IbEvent]


class IbCommandHandler:
    def __init__(self, ib_gateway_connection: IbGatewayConnection,
                 historical_data_manager: HistoricalDataManager,
                 uow):
        self.ib_gateway_connection = ib_gateway_connection
        self.historical_data_manager = historical_data_manager
        self.uow = uow

    def send(self, msg: IbMessage):
        if isinstance(msg, ib_commands.RequestMatchingSymbols):
            self.reqMatchingSymbols(msg)
        if isinstance(msg, ib_commands.RequestHistoricalData):
            self.reqHistoricalData(msg)

    def reqMatchingSymbols(self, cmd: ib_commands.RequestMatchingSymbols) -> None:
        self.ib_gateway_connection.reqMatchingSymbols(reqId=cmd.reqId, symbol=cmd.symbol)

    def reqHistoricalData(self, cmd: ib_commands.RequestHistoricalData,
                          ) -> None:
        self.historical_data_manager.register_request(cmd)
        # TODO: Check if this can be done directly on HistoricalDataManager send function
        contracts = views.contract(cmd.conId, self.uow)
        contract: Contract = contracts[0]
        contract.exchange = contract.primaryExchange
        self.ib_gateway_connection.reqHistoricalData(
            reqId=cmd.reqId, contract=contracts[0], endDateTime=cmd.endDateTime,
            durationStr=cmd.durationStr, barSizeSetting=cmd.barSizeSetting,
            whatToShow=cmd.whatToShow, useRTH=cmd.useRTH, formatDate=cmd.formatDate,
            keepUpToDate=cmd.keepUpToDate, chartOptions=cmd.chartOptions
        )


#TODO: ensure that the code below is not necessary and remove it
def write_contract_descriptions(event: ib_events.ContractDescriptionReceived,
                                command_queue: Queue) -> None:
    msg = f"Writing contract description for {event.contract}"
    logger.info(msg)
    write_contract_cmd = commands.WriteContract(event.contract)
    write_derivativeSecTypes_cmd = commands.WriteDerivativeSecTypes(event.derivativeSecTypes)
    command_queue.put(write_contract_cmd)
    command_queue.put(write_derivativeSecTypes_cmd)


def add_historical_data(event: ib_events.HistoricalDataReceived,
                        historical_data_manager: HistoricalDataManager):
    historical_data_manager.add(event)


def publish_historical_data(event: ib_events.HistoricalDataEnded,
                            historical_data_manager: HistoricalDataManager):
    _, data = historical_data_manager.get(event.reqId)
    # command_queue
    print(data)


def log_message(event: ib_events.IbError) -> None:
    print(event)


# EVENT_HANDLERS = {
#     ib_events.ContractDescriptionReceived: [write_contract_descriptions, log_message],
#     ib_events.HistoricalDataReceived: [add_historical_data],
#     ib_events.HistoricalDataEnded: [publish_historical_data],
#
#     ib_events.IbError: [log_message],
#     ib_events.ConnectionAcknowledged: [log_message],
#     ib_events.ConnectionClosed: [log_message],
#
# }  # type: Dict[Type[ib_events.Event], List[Callable]]
#
# COMMAND_HANDLERS = {
#     ib_commands.RequestMatchingSymbols: reqMatchingSymbols,
#
# }  # type: Dict[Type[ib_commands.Command], Callable]
