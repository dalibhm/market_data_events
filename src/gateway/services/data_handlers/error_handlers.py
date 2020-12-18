import logging

from gateway.services import exchange

logger = logging.getLogger(__name__)


class ErrorHandler:
    def __init__(self):
        # self.exchange = exchange.get_exchange('ib.')
        pass

    def send(self, msg):
        print(msg)
        logger.error(msg)