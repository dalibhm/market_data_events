from typing import List

from contracts.domain.events import NoContractsForInstrument
from ibapi.contract import Contract as IbContract


class Instrument:
    def __init__(self, symbol: str, contracts: List[IbContract] = []):
        self.symbol = symbol
        self.contracts = contracts
        self.events = []

    def __repr__(self):
        return f'Instrument({self.symbol}, {self.contracts})'

    def get_contract(self):
        if len(self.contracts) > 0:
            return self.contracts[0]
        else:
            self.events.append(NoContractsForInstrument(symbol=self.symbol))


class Contract:
    fields = [
        'conId',
        'symbol',
        'secType',
        'lastTradeDateOrContractMonth',
        'strike',
        'right',
        'multiplier'
        'exchange',
        'primaryExchange',
        'currency',
        'derivativeSecTypes',
        'localSymbol',
        'tradingClass',
        'includeExpired',
        'secIdType',
        'secId',

        'comboLegsDescrip',
        'comboLegs',
        'deltaNeutralContract'
    ]

    def __init__(self, ib_contract: IbContract):
        self._ib_contract = ib_contract

    @property
    def ib_contract(self):
        return self._ib_contract

    @classmethod
    def from_dict(cls, dictionary: dict):
        contract = Contract()
        for key, value in dictionary.items():
            if key in cls.fields:
                setattr(contract, key, value)
        return contract


def ib_contract_from_dict(dictionary: dict):
    contract = IbContract()
    for key, value in dictionary.items():
        if key in Contract.fields:
            setattr(contract, key, value)
    return contract
