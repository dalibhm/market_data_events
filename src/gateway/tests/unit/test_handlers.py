from gateway.adapters import repository
from gateway.domain import commands, events

from gateway.services import unit_of_work, bootstrap
from gateway.services.ib_gateway_connection import AbstractConnection
from gateway.domain import contract


class FakeRepository(repository.AbstractRepository):

    def __init__(self, instruments=[]):
        super().__init__()
        self._instruments = set(instruments)

    def _add(self, instrument):
        self._instruments.add(instrument)

    def _get(self, symbol):
        # for key, value in kwargs:
        #     out = [entity for entity in self._entities if entity[key] == value]
        # return out
        return next((p for p in self._instruments if p.symbol == symbol), None)

    def _get_by_conId(self, conId):
        return next((
            p for p in self._instruments if p._contract.conId == conId
        ), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.instruments = FakeRepository(instruments=[])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeIbGatewayConnection(AbstractConnection):
    def __init__(self):
        self._events = []

    @property
    def events(self):
        return self._events

    def collect_new_events(self):
        while self._events:
            yield self._events.pop(0)

    def reqMatchingSymbols(self, reqId, symbol):
        test_contract = Contract()
        test_contract.symbol = symbol
        event = events.ContractDescriptionReceived(reqId=reqId, contract=Contract(), derivativeSecTypes=[])
        self._events.append(event)


def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_ORM=False,
        uow=FakeUnitOfWork(),
        ib_gateway_connection=FakeIbGatewayConnection()
    )


class TestAddContract:

    def test_for_new_contract(self):
        bus = bootstrap_test_app()

        bus.handle(
            commands.CreateContract(
                contract.Contract(conId=1, symbol='test-symbol')
            )
        )
        assert bus.uow.instruments.get(symbol='test-symbol') is not None
        assert bus.uow.committed

    def test_for_existing_contract(self):
        bus = bootstrap_test_app()
        bus.handle(commands.CreateContract(contract.Contract(conId=1, symbol='test-symbol')))
        bus.handle(commands.CreateContract(contract.Contract(conId=2, symbol='test-symbol')))
        assert 2 == bus.uow.instruments.get(symbol='test-symbol').contract.conId
        #TODO: see if grouping contracts by symbol is useful.

    def test_for_existing_contract_same_conId(self):
        """
        the key for a contract is the id. if we try to write a new contract with the same id, it fails
        :return:
        """
        bus = bootstrap_test_app()
        bus.handle(commands.CreateContract(contract.Contract(conId=1, symbol='test-symbol-1')))
        bus.handle(commands.CreateContract(contract.Contract(conId=1, symbol='test-symbol-2')))
        assert 1 == bus.uow.instruments.get(symbol='test-symbol-1').contract.conId