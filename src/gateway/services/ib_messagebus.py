# pylint: disable=broad-except
from __future__ import annotations
import logging
import time
from queue import Queue
from threading import Thread
from typing import List, Dict, Callable, Type, Union, TYPE_CHECKING
from gateway.domain import commands, events
from gateway.ib_gateway import ib_events, ib_commands

from .ib_gateway_connection import IbGatewayConnection


logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event, ib_events.IbEvent]


class IBMessageBus(Thread):

    def __init__(
            self,
            ib_gateway_connection: IbGatewayConnection,
            event_handlers: Dict[Type[ib_events.IbEvent], List[Callable]],
            command_handlers: Dict[Type[ib_commands.IbCommand], List[Callable]],
            ib_queue: Queue,
            main_queue: Queue
    ):
        super().__init__()
        self.ib_gateway_connection = ib_gateway_connection
        self.event_handlers = event_handlers
        self.queue = ib_queue

    def run(self) -> None:
        while True:
            message = self.queue.get()
            for handler in self.event_handlers[type(message)]:
                try:
                    logger.debug('handling event %s with handler %s', message, handler)
                    handler(message)
                except Exception:
                    logger.exception('Exception handling event %s', message)
                    continue

