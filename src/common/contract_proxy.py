from ibapi.contract import Contract as IbContract, ContractDetails as IbContractDetails


class Proxy:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name.starts_with('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)


class Contract(Proxy):
    def __init__(self, contract: IbContract):
        super().__init__(contract)


class ContractDetails(Proxy):
    def __init__(self, contract_details: IbContractDetails):
        super().__init__(contract_details)
