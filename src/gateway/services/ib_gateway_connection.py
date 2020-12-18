import logging
import os
from datetime import time
from queue import Queue

from gateway.ib_gateway.ib_gateway import IbGateway
from ibapi.common import TickerId, TagValueList
from ibapi.contract import Contract


class OneOnly:
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(OneOnly, cls).__new__(cls, *args, **kwargs)
        return cls._singleton


def init_logging():
    if not os.path.exists("../log"):
        os.makedirs("../log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=os.path.join("../log", "ibapi.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)


class AbstractConnection:
    pass


class IbGatewayConnection(OneOnly, AbstractConnection):
    def __init__(self, endpoint=('127.0.0.1', 4001, 1)):
        if not hasattr(self, 'ib_client'):
            self.host, self.port, self.clientId = endpoint
            init_logging()
            self.ib_client = IbGateway()
            self.ib_client.connect(host=self.host, port=self.port, clientId=self.clientId)
            self.ib_client.start()

    # def stop(self):
    #     self.client_loop.join()
    #     self.ib_client.disconnect()

    def collect_new_events(self):
        while self.ib_client.events:
            yield self.ib_client.events.pop(0)

    def reqMatchingSymbols(self, reqId, symbol):
        self.ib_client.reqMatchingSymbols(reqId, symbol)

    def reqHistoricalData(self, reqId: TickerId, contract: Contract, endDateTime: str,
                          durationStr: str, barSizeSetting: str, whatToShow: str,
                          useRTH: int, formatDate: int, keepUpToDate: bool, chartOptions: TagValueList):
        self.ib_client.reqHistoricalData(reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow,
                                         useRTH, formatDate, keepUpToDate, chartOptions)
