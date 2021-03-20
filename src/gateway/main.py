import logging
import logging.config

logging.config.fileConfig('logconfig.ini')
logger = logging.getLogger(__name__)
logger.info('started logging')

import time

import sys
# sys.path.insert(0, '/Users/dali/workspace/code_2020/src/ib_gateway/adapters')
# sys.path.insert(0, '/Users/dali/workspace/code_2020/src/ib_gateway/domain')
# sys.path.insert(0, '/Users/dali/workspace/code_2020/src/ib_gateway/ib_gateway')
# sys.path.insert(0, '/Users/dali/workspace/code_2020/src/ib_gateway/services')
# sys.path.insert(0, '/Users/dali/workspace/code_2020/src/ibapi')

from gateway.domain import commands
from gateway.ib_gateway import ib_commands
from gateway.services.bootstrap import bootstrap




# def init_log():
#     logging.config.fileConfig('logconfig.ini')
#     logger.info('started logging')


def init():
    # init_log()
    logger.info('Intializing objects')
    bus, ib_command_handler, ib_gateway_connection = bootstrap()
    logger.info('Objects initialized.')
    time.sleep(1.0)
    return bus, ib_command_handler, ib_gateway_connection


def main():
    bus, ib_command_handler, ib_gateway_connection = init()
    logger.info('Sending command.')
    cmd = ib_commands.RequestMatchingSymbols(
        reqId=20,
        symbol='BB'
    )
    bus.handle(cmd)
    time.sleep(2.0)

    ib_gateway_connection.ib_client.disconnect()


if __name__ == '__main__':
    main()

