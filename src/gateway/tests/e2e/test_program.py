import time

import pytest
from testfixtures import LogCapture

from ib_gateway.domain import commands
from ib_gateway.log_init import init_log
from ib_gateway.services.bootstrap import bootstrap


@pytest.fixture
def bus():
    # init_log()
    bus = bootstrap()
    time.sleep(1.0)
    yield bus
    bus.ib_gateway_connection.ib_client.disconnect()


def test_program_up(bus):
    cmd = commands.RequestMatchingSymbols(
        reqId=20,
        symbol='AMZN'
    )
    with LogCapture() as l:
        bus.handle(cmd)
        time.sleep(2.0)
    print(l)
