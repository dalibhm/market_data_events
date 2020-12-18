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
from gateway.services.bootstrap import bootstrap




# def init_log():
#     logging.config.fileConfig('logconfig.ini')
#     logger.info('started logging')


def init():
    # init_log()
    logger.info('Intializing objects')
    bus = bootstrap()
    logger.info('Objects initialized.')
    time.sleep(1.0)
    return bus


def main():
    bus = init()
    logger.info('Sending command.')
    cmd = commands.RequestMatchingSymbols(
        reqId=20,
        symbol='AMZN'
    )
    bus.handle(cmd)
    time.sleep(5.0)
    bus.ib_gateway_connection.ib_client.disconnect()


if __name__ == '__main__':
    main()

