# pylint: disable=broad-except
from __future__ import annotations
import logging
import time
from queue import Queue
from typing import List, Dict, Callable, Type, Union, TYPE_CHECKING
from gateway.domain import commands, events
from gateway.ib_gateway import ib_events, ib_commands
from .exchange import Exchange

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event, ib_events.IbEvent, ib_commands.IbCommand]
Event = Union[events.Event, ib_events.IbEvent]
Command = Union[commands.Command, ib_commands.IbCommand]


class MessageBus:

    def __init__(
            self,
            uow: unit_of_work.AbstractUnitOfWork,
            event_handlers: Dict[Type[events.Event], List[Callable]],
            command_handlers: Dict[Type[commands.Command], Callable],
            ib_commands_exchange: Exchange,
            ib_events_exchange: Exchange,
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.ib_commands_exchange = ib_commands_exchange
        self.ib_events_exchange = ib_events_exchange

    def handle(self, message: Message) -> None:
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            elif isinstance(message, ib_commands.IbCommand):
                self.ib_commands_exchange.send(message)
            elif isinstance(message, ib_events.IbEvent):
                self.ib_events_exchange.send(message)
            else:
                raise Exception(f'{message} was not an Event or Command')

    def handle_event(self, event: events.Event) -> None:
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue

    def handle_command(self, command: commands.Command):
        logger.debug('handling command %s', command)
        try:
            handler = self.command_handlers[type(command)]

            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise

    def handle_ib_event(self, event: ib_events.IbEvent) -> None:
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug('handling ib event %s with handler %s', event, handler)
                handler(event)
            except Exception:
                logger.exception('Exception handling ib event %s', event)
                continue
