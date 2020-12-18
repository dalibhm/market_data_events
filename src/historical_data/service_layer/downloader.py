from historical_data.domain.download import Download
from ib_gateway.ib_gateway import IbGateway
from ibapi.contract import Contract


class Downloader:
    def __init__(self, contract: Contract, download: Download, ib_gateway: IbGateway):
        self.contract = contract
        self.download = download
        self.ib_gateway = ib_gateway

        self.instrument = Instrument

    def run(self):
        request = self.download.get_request()
        self.ib_gateway.reqHistoricalData(**request)