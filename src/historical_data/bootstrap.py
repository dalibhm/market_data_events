import inspect
import logging

from historical_data.adapters import sql_alchemy
from historical_data.services import unit_of_work, messagebus, handlers

logger = logging.getLogger(__name__)


def bootstrap(start_ORM: bool = None,
              uow: unit_of_work.AbstractUnitOfWork = None,
              ) -> messagebus.MessageBus:
    logger.info('Creating objects.')
    if start_ORM is None:
        sql_alchemy.start_mappers()
        logger.info('Started ORM mapper')

    if uow is None:
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        logger.info('Created UOW')

    dependencies = {'uow': uow}

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

    bus = messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

    return bus


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
