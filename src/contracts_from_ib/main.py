from ibapi.contract import Contract
from ibwrapper.ib_client import IbWrapper


def run():
    ibclient = IbWrapper()
    ibclient.start()
    # something is missing here about the connection

    stock = 'sample stock'
    contract = Contract()
    contract.symbol = stock
    ibclient.reqContractDetails(reqId=100, contract=contract)
    # this needs the IB client to be up and running


if __name__ == 'main':
    run()
