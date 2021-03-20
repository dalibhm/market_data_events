import inspect
import logging

from gateway.adapters import sql_alchemy
from gateway.services import unit_of_work, messagebus, handlers, exchange
from gateway.services.data_handlers.contract_handlers import ContractHandler
from gateway.services.data_handlers.error_handlers import ErrorHandler
from gateway.services.data_handlers.historical_data_manager import HistoricalDataManager
from gateway.services.ib_gateway_connection import IbGatewayConnection, AbstractConnection
from gateway.services.ib_handlers import IbCommandHandler

logger = logging.getLogger(__name__)


def bootstrap(start_ORM: bool = None,
              uow: unit_of_work.AbstractUnitOfWork = None,
              ib_command_handler: IbCommandHandler = None,
              ) -> messagebus.MessageBus:
    logger.info('Creating objects.')
    if start_ORM is None:
        sql_alchemy.start_mappers()
        logger.info('Started ORM mapper')

    if uow is None:
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        logger.info('Created UOW')

    if ib_command_handler is None:
        historical_data_manager = HistoricalDataManager()
        ib_gateway_connection = IbGatewayConnection()
        ib_command_handler = IbCommandHandler(
            ib_gateway_connection=ib_gateway_connection,
            historical_data_manager=historical_data_manager,
            uow=uow
        )
        logger.info('Created IB Command Handler')

    dependencies = {'uow': uow,
                    'IbCommandHandler': IbCommandHandler}

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

    ib_commands_exchange = exchange.get_exchange('ib.commands')
    ib_commands_exchange.attach(ib_command_handler)

    error_handler = ErrorHandler()
    exchange.get_exchange('wrapper.errors').attach(error_handler)

    contracts_handler = ContractHandler()
    exchange.get_exchange('wrapper.symbol_samples').attach(contracts_handler)
    exchange.get_exchange('wrapper.contract_details').attach(contracts_handler)

    exchange.get_exchange('wrapper.historical_data').attach(historical_data_manager)
    exchange.get_exchange('wrapper.historical_data_end').attach(historical_data_manager)

    ib_events_exchange = exchange.get_exchange('ib.events')
    ib_events_exchange.attach(historical_data_manager)


    bus = messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
        ib_commands_exchange=ib_commands_exchange,
        ib_events_exchange=ib_events_exchange
    )

    exchange.get_exchange('main.contracts').attach(bus)
    exchange.get_exchange('main.derivativeSecTypes').attach(bus)
    exchange.get_exchange('main.contractDetails').attach(bus)
    exchange.get_exchange('main.historicalData').attach(bus)
    ib_events_exchange.attach(bus)

    return bus, ib_command_handler, ib_gateway_connection


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
