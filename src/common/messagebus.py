import logging
from typing import Union, List

from common import domain_events
from contracts.service_layer.handlers import request_contract_from_gateway
from ib_gateway import events as ib_gateway_events

from contracts.service_layer import events as contracts_events



import historical_data.service_layer.messagebus as historical_data

logger = logging.getLogger(__name__)

Message = Union[domain_events.Command, domain_events.DomainEvent]


def handle(message: Message, uow):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, domain_events.DomainEvent):
            handle_event(message, queue, uow)
        elif isinstance(message, domain_events.Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')
    return results


def handle_event(
    event: domain_events.DomainEvent,
    queue: List[Message],
    uow
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug('handling event %s with handler %s', event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling event %s', event)
            continue


def handle_command(
    command: domain_events.Command,
    queue: List[Message],
    uow
):
    logger.debug('handling command %s', command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logger.exception('Exception handling command %s', command)
        raise


EVENT_HANDLERS = { }
#     events.Allocated: [handlers.publish_allocated_event],
#     events.OutOfStock: [handlers.send_out_of_stock_notification],
# }  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    contracts_events.RequestContract: request_contract_from_gateway  #,
    # commands.CreateBatch: handlers.add_batch,
    # commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]
