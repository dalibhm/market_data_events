import inspect
import logging
from queue import Queue

from gateway.adapters import sql_alchemy
from gateway.services import unit_of_work, messagebus, handlers, ib_handlers, ib_messagebus, exchange
from gateway.services.historical_data_manager import HistoricalDataManager
from gateway.services.ib_gateway_connection import IbGatewayConnection, AbstractConnection
from ibapi.contract import Contract

logger = logging.getLogger(__name__)


def bootstrap(start_ORM: bool = None,
              uow: unit_of_work.AbstractUnitOfWork = None,
              ib_gateway_connection: AbstractConnection = None,
              historical_data_manager: HistoricalDataManager = None
              ) -> messagebus.MessageBus:
    logger.info('Creating objects.')
    if start_ORM is None:
        sql_alchemy.start_mappers()
        logger.info('Started ORM mapper')

    if uow is None:
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        logger.info('Created UOW')

    if historical_data_manager is None:
        historical_data_manager = HistoricalDataManager()
        logger.info('Created historical data manager')

    contract_details_exc = exchange.get_exchange('contract_details')
    historical_data_exc = exchange.get_exchange('historical_data')
    historical_data_end_exc = exchange.get_exchange('historical_data_end')

    if ib_gateway_connection is None:
        ib_gateway_connection = IbGatewayConnection()
        logger.info('Created IB Gateway Connection')

    dependencies = {'uow': uow,
                    'ib_gateway_connection': ib_gateway_connection,
                    'historical_data_manager': historical_data_manager}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    injected_ib_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in ib_handlers.EVENT_HANDLERS.items()
    }

    injected_ib_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in ib_handlers.COMMAND_HANDLERS.items()
    }

    main_bus = messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

    ib_bus = ib_messagebus.IBMessageBus(ib_gateway_connection=ib_gateway_connection,
                                        event_handlers=injected_ib_event_handlers,
                                        command_handlers=injected_command_handlers)

    return main_bus, ib_bus


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
