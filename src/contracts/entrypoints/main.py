from contracts.service_layer import events
from contracts.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from common import messagebus


def init():
    pass


if __name__ == "main":
    symbol = 'PAYC'
    init()
    uow = SqlAlchemyUnitOfWork()
    messagebus.handle(
        events.RequestContract(symbol=symbol), uow
    )
