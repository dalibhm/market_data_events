import time

from gateway.ib_gateway.ib_gateway import IbGateway
from gateway.services.ib_gateway_connection import IbGatewayConnection


def test_ib_gateway():
    ib = IbGateway()
    ib.connect(host='127.0.0.1', port=4001, clientId=1)
    ib.start()
    ib.reqCurrentTime()
    time.sleep(0.5)
    ib.disconnect()


def test_ib_gateway_connection():
    ib_gateway_connection = IbGatewayConnection()
    ib_gateway_connection.ib_client.reqCurrentTime()
    time.sleep(0.5)
    ib_gateway_connection.ib_client.disconnect()


def test_ib_gateway_connection_reqMatchingSymbols():
    ib_gateway_connection = IbGatewayConnection()
    ib_gateway_connection.reqMatchingSymbols(reqId=11, symbol='PAYC')
    time.sleep(0.5)
    ib_gateway_connection.ib_client.disconnect()
