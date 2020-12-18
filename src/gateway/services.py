from ibwrapper.ib_client import IbWrapper


class RequestManager:

    def request_contract(request, uow):
        request_manager.register_request(request)
        ib_client.reqHistoricalData(**request)
        # --> mark request as submitted
