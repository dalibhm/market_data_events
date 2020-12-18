from gateway.ib_gateway import ib_events
from gateway.services import exchange


class ContractHandler:
    def __init__(self):
        self.contracts_exc = exchange.get_exchange('contracts')
        self.contracts_derivativeSecTypes_exc = exchange.get_exchange('derivativeSecTypes')

    def send(self, contract_event: ib_events.IbEvent):
        if isinstance(contract_event, ib_events.ContractDescriptionReceived):
            self.contracts_exc.send(contract_event.contract)
            self.contracts_derivativeSecTypes_exc.send(contract_event.derivativeSecTypes)
            # these exchange are read by the message bus that processes them and saves them in the database
