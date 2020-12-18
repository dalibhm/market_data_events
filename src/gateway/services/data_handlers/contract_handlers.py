from gateway.ib_gateway import ib_events
from gateway.services import exchange

from gateway.domain import commands


class ContractHandler:
    """
    The handler is designed to be attached to the exchanges :
        'wrapper.symbol_samples': for contract description
        'wrapper.contract_details': for contract details
    """

    def __init__(self):
        self.contracts_exc = exchange.get_exchange('main.contracts')
        self.contracts_derivativeSecTypes_exc = exchange.get_exchange('main.derivativeSecTypes')
        self.contracts_contractDetails_exc = exchange.get_exchange('main.contractDetails')

    def send(self, contract_event: ib_events.IbEvent):
        if isinstance(contract_event, ib_events.ContractDescriptionReceived):
            self.contracts_exc.send(
                commands.CreateContract(contract=contract_event.contract)
            )
            self.contracts_derivativeSecTypes_exc.send(
                commands.WriteDerivativeSecTypes(
                    conId=contract_event.contract.conId,
                    symbol=contract_event.contract.symbol,
                    derivative_sec_type=contract_event.derivativeSecTypes)
            )
            # these exchange are read by the message bus that processes them and saves them in the database
