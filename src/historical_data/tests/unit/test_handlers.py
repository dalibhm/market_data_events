from datetime import datetime

from historical_data.adapters import repository
from historical_data.domain import commands  # , events
from historical_data.domain.instrument import Request, DataSummary

from historical_data.services import unit_of_work
from historical_data import bootstrap


class FakeRepository(repository.AbstractRepository):

    def __init__(self, instruments=[]):
        super().__init__()
        self._instruments = set(instruments)

    def _add(self, instrument):
        self._instruments.add(instrument)

    def _get(self, conId):
        # for key, value in kwargs:
        #     out = [entity for entity in self._entities if entity[key] == value]
        # return out
        return next((p for p in self._instruments if p.conId == conId), None)

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


def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_ORM=False,
        uow=FakeUnitOfWork(),
    )


class TestAddRequest:

    def test_for_new_request(self):
        bus = bootstrap_test_app()
        data_summary = DataSummary(
            start_date=datetime(2020, 6, 1),
            end_date=datetime(2020, 12, 1),
            data_start_date=datetime(2020, 6, 1),
            data_end_date=datetime(2020, 12, 1),
            data_points_number=123
        )

        request = Request(conId=1, endDateTime='20191220 00:00:00 GMT', durationStr='6 M', barSizeSetting='1 day',
                          whatToShow='TRADES', useRTH=1, formatDate=1, keepUpToDate=False,
                          data_summary=data_summary)

        bus.handle(
            commands.AddRequest(
                symbol='test_symbol',
                request=request,
            )
        )
        assert bus.uow.instruments.get(conId=1) is not None
        assert bus.uow.instruments.get(conId=1).requests[0] == request
        assert bus.uow.committed



    def test_for_existing_request(self):
        bus = bootstrap_test_app()
        bus.handle(commands.CreateContract(contract.Contract(conId=1, symbol='test-symbol')))
        bus.handle(commands.CreateContract(contract.Contract(conId=2, symbol='test-symbol')))
        assert 2 == bus.uow.instruments.get(symbol='test-symbol').contract.conId
        # TODO: see if grouping contracts by symbol is useful.

    def test_for_existing_contract_same_conId(self):
        """
        the key for a contract is the id. if we try to write a new contract with the same id, it fails
        :return:
        """
        bus = bootstrap_test_app()
        bus.handle(commands.CreateContract(contract.Contract(conId=1, symbol='test-symbol-1')))
        bus.handle(commands.CreateContract(contract.Contract(conId=1, symbol='test-symbol-2')))
        assert 1 == bus.uow.instruments.get(symbol='test-symbol-1').contract.conId
