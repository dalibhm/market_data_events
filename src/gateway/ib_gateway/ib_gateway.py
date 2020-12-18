import logging
from threading import Thread

from gateway.ib_gateway.ib_wrapper import Wrapper
from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.contract import ContractDetails
from ibapi.wrapper import iswrapper
from gateway.ib_gateway.ib_events import HistoricalDataReceived, HistoricalDataEnded, ContractDetailsReceived


class IbGateway(EClient, Wrapper):
    def __init__(self):
        # self.wrapper = EWrapper()
        # self.client = EClient(self.wrapper)
        EClient.__init__(self, self)
        self.nextValidOrderId = None
        self.permId2ord = {}

        self.events = []

    # def connect(self, ip, port, client_id):
    #     self.client.connect(ip, port, client_id)
    #
    # def disconnect(self):
    #     self.client.disconnect()
    #
    # def isConnected(self):
    #     return self.client.isConnected()

    def start(self):
        loop_thread = Thread(target=self.run)
        loop_thread.start()

    def stop(self):
        pass

    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId

    def nextOrderId(self):
        id = self.nextValidOrderId
        self.nextValidOrderId += 1
        return id





    # def reqCurrentTime(self):
    #     self.client.reqCurrentTime()
    #
    # def reqManagedAccts(self):
    #     self.client.reqManagedAccts()
    #
    # def reqAccountSummary(self):
    #     self.client.reqAccountSummary(reqId=2, groupName="All",
    #                                   tags="NetLiquidation")
    #
    # def reqAllOpenOrders(self):
    #     self.client.reqAllOpenOrders()
