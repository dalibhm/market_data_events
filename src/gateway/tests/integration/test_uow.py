from ib_gateway.domain import commands, events
from ib_gateway.services import unit_of_work
from ib_gateway.tests.conftest import *
from ibapi.contract import Contract

from ib_gateway.services.handlers import add_contract  # , get_contract_by_symbol


def insert_contract(session, symbol, version):
    session.execute(
        'INSERT INTO instruments (symbol) VALUES (:symbol)',
        dict(symbol=symbol),
    )

    session.execute(
        """INSERT INTO contracts (conId, symbol, secType, lastTradeDateOrContractMonth, 
        strike, right, multiplier, exchange, primaryExchange, currency , derivativeSecTypes,
        localSymbol, tradingClass, includeExpired, secIdType, secId, comboLegsDescrip, comboLegs, deltaNeutralContract) 
        VALUES (:conId, :symbol, :secType, :lastTradeDateOrContractMonth, 
        :strike, :right, :multiplier, :exchange, :primaryExchange, :currency , :derivativeSecTypes,
        :localSymbol, :tradingClass, :includeExpired, :secIdType, :secId, :comboLegsDescrip, :comboLegs, :deltaNeutralContract)""",
        dict(conId=1, symbol=symbol, secType="secType", lastTradeDateOrContractMonth="",
             strike=None, right="", multiplier="", exchange="exchange", primaryExchange="exchange", currency="USD",
             derivativeSecTypes="",
             localSymbol="", tradingClass="", includeExpired=False, secIdType="", secId="", comboLegsDescrip="",
             comboLegs="", deltaNeutralContract=""),
    )


def test_uow_add_contract(session_factory):
    new_contract = Contract()
    new_contract.symbol = 'test-symbol'

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        add_contract(cmd=events.ContractReceived(reqId=1, contract=new_contract), uow=uow)

    with uow:
        contract = uow.instruments.get(symbol='test-symbol')
        assert 'test-symbol' == contract.symbol


def test_uow_get_existing_contract(session_factory):
    session = session_factory()
    insert_contract(session, symbol='test-symbol-2', version=None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        contract = uow.instruments.get(symbol='test-symbol-2')
        assert contract.symbol == "test-symbol-2"


def test_uow_get_inexisting_contract(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory, entity_type=Contract)
    with uow:
        contract = uow.entities.get(symbol='test-symbol')
        assert contract is None

# def test_uow_add_contract_to_existing_instrument(session_factory):
#     session = session_factory()
#     insert_contract(session, symbol='test-symbol', version=None)
#     session.commit()
#
#     uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory, entity_type=Contract)
#     new_contract = Contract()
#     new_contract.symbol = 'test-symbol'
#
#     with uow:
#         contract = uow.entities.get(symbol='test-symbol')
#         assert 'test-symbol' == contract.symbol
#
#     add_contract(cmd=commands.CreateContract(1, "test-symbol", 100, None), uow=uow)
#
#     with uow:
#         instrument = uow.instruments.get('test-symbol')
#         assert 2 == len(instrument.contracts)
