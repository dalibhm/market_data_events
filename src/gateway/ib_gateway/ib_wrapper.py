from datetime import datetime

from gateway.data_structures import bar_data
from gateway.ib_gateway.ib_events import ContractDetailsReceived, HistoricalDataReceived, HistoricalDataEnded, \
    ContractDescriptionReceived
from gateway.services import exchange
from ibapi.common import TickerId, ListOfContractDescription, BarData
from ibapi.contract import ContractDetails
from ibapi.wrapper import EWrapper
from gateway.ib_gateway import ib_events


class Wrapper(EWrapper):
    def __init__(self):
        super().__init__()
        self.error_exchange = exchange.get_exchange('wrapper.errors')
        self.connection_exchange = exchange.get_exchange('wrapper.connection')
        self.symbol_samples_exchange = exchange.get_exchange('wrapper.symbol_samples')
        self.contract_details_exchange = exchange.get_exchange('wrapper.contract_details')
        self.historical_data_exchange = exchange.get_exchange('wrapper.historical_data')
        self.historical_data_end_exchange = exchange.get_exchange('wrapper.historical_data_end')

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        self.error_exchange.send(
            ib_events.IbError(reqId=reqId, errorCode=errorCode, errorString=errorString)
        )

    def connectAck(self):
        self.connection_exchange.send(
            ib_events.ConnectionAcknowledged()
        )

    def connectionClosed(self):
        self.connection_exchange.send(
            ib_events.ConnectionClosed()
        )

    def symbolSamples(self, reqId: int,
                      contractDescriptions: ListOfContractDescription):
        for contractDescription in contractDescriptions:
            self.symbol_samples_exchange.send(
                ContractDescriptionReceived(reqId=reqId,
                                            contract=contractDescription.contract,
                                            derivativeSecTypes=contractDescription.derivativeSecTypes
                                            )
            )

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        contract = contractDetails.contract
        self.contract_details_exchange.send(
            ContractDetailsReceived(reqId, **contract.__dict__, **ContractDetails.__dict__))

    def historicalData(self, reqId: int, bar: BarData):
        self.historical_data_exchange.send(
            HistoricalDataReceived(reqId=reqId, bar_data=bar_data.BarData.from_ib(bar))
        )

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.historical_data_end_exchange.send(HistoricalDataEnded(reqId=reqId, start=start, end=end))
