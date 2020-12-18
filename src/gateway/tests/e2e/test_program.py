import logging
import time

import pytest
from testfixtures import LogCapture

from gateway.domain import commands
from gateway.domain.contract import Contract
from gateway.ib_gateway import ib_commands
from gateway.services.bootstrap import bootstrap


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
    cmd = ib_commands.RequestHistoricalData(
        reqId=20,
        conId=148163036,
        endDateTime='20200622 00:00:00 GMT',
        durationStr='6 M',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=1,
        formatDate=1,
        keepUpToDate=False,
        chartOptions=[]
    )
    with LogCapture(level=logging.INFO) as l:
        bus.handle(cmd)
        time.sleep(2.0)
    print(l)
