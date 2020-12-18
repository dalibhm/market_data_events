from contracts.domain import commands
from contracts.service_layer import unit_of_work
from contracts.tests.conftest import *
from ibapi.contract import Contract

from contracts.service_layer.handlers import add_contract, get_contract_by_symbol


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


def test_uow_add_contract_to_existing_instrument(session_factory):
    session = session_factory()
    insert_contract(session, symbol='test-symbol', version=None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    new_contract = Contract()
    new_contract.symbol = 'test-symbol'

    with uow:
        instrument = uow.instruments.get('test-symbol')
        assert 1 == len(instrument.contracts)

    add_contract(cmd=commands.CreateContract(1, "test-symbol", 100, None), uow=uow)

    with uow:
        instrument = uow.instruments.get('test-symbol')
        assert 2 == len(instrument.contracts)


def test_uow_add_contract_to_new_instrument(session_factory):
    session = session_factory()
    insert_contract(session, symbol='test-symbol', version=None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)

    add_contract(cmd=commands.CreateContract(1, "test-symbol-NEW", 100, None), uow=uow)

    with uow:
        instrument = uow.instruments.get('test-symbol')
        instrument_new = uow.instruments.get('test-symbol')
        assert 1 == len(instrument.contracts)
        assert 1 == len(instrument_new.contracts)


def test_uow_get_existing_contract(session_factory):
    session = session_factory()
    insert_contract(session, symbol='test-symbol', version=None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        instrument = uow.instruments.get(symbol='test-symbol')
        print(instrument)
        assert instrument.symbol == "test-symbol"
        assert 1 == len(instrument.contracts)