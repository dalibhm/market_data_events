from queue import Queue

from gateway.domain import commands, events
from gateway.ib_gateway import ib_events, ib_commands
from gateway.services.historical_data_manager import HistoricalDataManager
from gateway.services.ib_gateway_connection import IbGatewayConnection

import logging

logger = logging.getLogger(__name__)


def reqMatchingSymbols(cmd: ib_commands.RequestMatchingSymbols,
                       ib_gateway_connection: IbGatewayConnection) -> None:
    ib_gateway_connection.reqMatchingSymbols(reqId=cmd.reqId, symbol=cmd.symbol)


def reqHistoricalData(cmd: ib_commands.RequestHistoricalData,
                      ib_gateway_connection: IbGatewayConnection,
                      historical_data_manager: HistoricalDataManager) -> None:
    historical_data_manager.register_request(cmd)
    ib_gateway_connection.reqHistoricalData(reqId=cmd.reqId, contract=cmd.contract, endDateTime=cmd.endDateTime,
                                            durationStr=cmd.durationStr, barSizeSetting=cmd.barSizeSetting,
                                            whatToShow=cmd.whatToShow, useRTH=cmd.useRTH, formatDate=cmd.formatDate,
                                            keepUpToDate=cmd.keepUpToDate, chartOptions=cmd.chartOptions)


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


EVENT_HANDLERS = {
    ib_events.ContractDescriptionReceived: [write_contract_descriptions, log_message],
    ib_events.HistoricalDataReceived: [add_historical_data],
    ib_events.HistoricalDataEnded: [publish_historical_data],

    ib_events.IbError: [log_message],
    ib_events.ConnectionAcknowledged: [log_message],
    ib_events.ConnectionClosed: [log_message],

}  # type: Dict[Type[ib_events.Event], List[Callable]]

COMMAND_HANDLERS = {
    ib_commands.RequestMatchingSymbols: reqMatchingSymbols,

}  # type: Dict[Type[ib_commands.Command], Callable]
