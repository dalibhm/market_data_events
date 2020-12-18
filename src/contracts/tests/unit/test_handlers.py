from contracts.adapters import repository
from contracts.domain import commands
from contracts.service_layer import unit_of_work, messagebus


class FakeRepository(repository.AbstractRepository):

    def __init__(self, instruments):
        super().__init__()
        self._instruments = set(instruments)

    def _add(self, instrument):
        self._instruments.add(instrument)

    def _get(self, symbol):
        return next((p for p in self._instruments if p.symbol == symbol), None)

    def _get_by_contract_id(self, contract_id):
        return next((
            p for p in self._instruments for b in p.contracts
            if b.conId == contract_id
        ), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.instruments = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class TestAddContract:

    def test_for_new_product(self):
        uow = FakeUnitOfWork()
        messagebus.handle(
            commands.CreateContract(1, "test-symbol", 100, None), uow
        )
        assert uow.instruments.get("test-symbol") is not None
        assert uow.committed

    def test_for_existing_product(self):
        uow = FakeUnitOfWork()
        messagebus.handle(commands.CreateContract(2, "test-symbol-2", 100, None), uow)
        messagebus.handle(commands.CreateContract(3, "test-symbol-2", 99, None), uow)
        assert 2 in [b.conId for b in uow.instruments.get("test-symbol-2").contracts]
