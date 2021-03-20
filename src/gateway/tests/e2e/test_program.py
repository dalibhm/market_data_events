import logging
import time

import pytest
from testfixtures import LogCapture

from gateway.domain import commands
from gateway.domain.contract_v0 import Contract
from gateway.ib_gateway import ib_commands
from gateway.params.historical_request import HistoricalParams
from gateway.services import views
from gateway.services.bootstrap import bootstrap
from gateway.services.unit_of_work import SqlAlchemyUnitOfWork


@pytest.fixture
def bus():
    # init_log()
    bus, ib_command_handler = bootstrap()
    time.sleep(1.0)
    yield bus
    ib_command_handler.ib_gateway_connection.ib_client.disconnect()


def test_program_up(bus):
    cmd = ib_commands.RequestMatchingSymbols(
        reqId=20,
        symbol='IBM'
    )
    with LogCapture() as l:
        bus.handle(cmd)
        time.sleep(2.0)
    print(l)


def test_historical_data_download(bus):
    conId = 148163036
    contract = views.contract(conId=conId, uow=SqlAlchemyUnitOfWork())[0]
    contract.exchange = contract.primaryExchange
    cmd = ib_commands.RequestHistoricalData(
        reqId=20,
        contract=contract,
        params=HistoricalParams(
            endDateTime='20200622 00:00:00 GMT',
            durationStr='6 M',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=1,
            formatDate=1,
            keepUpToDate=False
        )
    )
    with LogCapture(level=logging.INFO) as l:
        bus.handle(cmd)
        time.sleep(2.0)
    print(l)
