from gateway.domain.contract import Contract, DerivativeSecTypes
from gateway.ib_gateway import ib_commands, ib_events


def test_contract_description():
    ib_events.ContractDescriptionReceived(reqId=1, contract=Contract(), derivativeSecTypes=DerivativeSecTypes)
