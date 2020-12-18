from collections import defaultdict

from gateway.ib_gateway.ib_commands import RequestHistoricalData
from gateway.ib_gateway.ib_events import HistoricalDataReceived, HistoricalDataEnded
from gateway.services import exchange


class HistoricalData:
    def __init__(self):
        self.data = []

    def add(self, data_in):
        self.data.append(data_in)


class HistoricalDataManager:
    def __init__(self):
        self.requests = dict()  # dict[reqId, RequestHistoricalData]
        self.data = defaultdict(lambda: HistoricalData())  # dict[reqId, HistoricalData]
        self.exc = exchange.get_exchange('historical_data')

    def send(self, msg):
        if isinstance(msg, HistoricalDataReceived):
            self.add(msg)
        if isinstance(msg, HistoricalDataEnded):
            reqId = msg.reqId
            request, data = self.get(reqId)
            self.exc.send((request, data))

    def register_request(self, request: RequestHistoricalData):
        reqId = request.reqId
        self.requests[reqId] = request

    def add(self, data: HistoricalDataReceived):
        reqId = data.reqId
        self.data[reqId].add(data)

    def get(self, reqId):
        request = self.requests.pop(reqId)
        data = self.data.pop(reqId)
        return request, data
