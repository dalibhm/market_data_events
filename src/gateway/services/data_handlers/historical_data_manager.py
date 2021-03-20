from collections import defaultdict

from gateway.data_structures.historical_data import HistoricalData
from gateway.domain.contract_v0 import Contract
from gateway.ib_gateway.ib_events import HistoricalDataReceived, HistoricalDataEnded
from gateway.domain.events import HistoricalRequestProcessed, HistoricalRequest, DataSummary
from gateway.params.historical_request import HistoricalParams
from gateway.services import exchange, views


class HistoricalDataManager:
    def __init__(self):
        self.requests = dict()  # dict[(reqId, contract, params)]
        self.data = defaultdict(lambda: HistoricalData())  # dict[reqId, HistoricalData]
        self.exc = exchange.get_exchange('main.historicalData')

    def send(self, msg):
        if isinstance(msg, HistoricalDataReceived):
            self.add(msg)
        if isinstance(msg, HistoricalDataEnded):
            request, data = self.get(msg.reqId)
            out_msg = HistoricalRequestProcessed(contract=request[1],
                                                 params=request[2],
                                                 data_summary=DataSummary.from_historical_data(
                                                     historical_data=data,
                                                     historical_data_ended=msg
                                                 )
                                                 )
            self.exc.send(out_msg)

    def register_request(self, reqId: int, contract: Contract, params: HistoricalParams):
        self.requests[reqId] = (reqId, contract, params)

    def add(self, msg: HistoricalDataReceived):
        self.data[msg.reqId].add(msg.bar_data)

    def get(self, reqId):
        request = self.requests.pop(reqId)
        data = self.data.pop(reqId)
        return request, data
