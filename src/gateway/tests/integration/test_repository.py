import pytest

from ib_gateway.domain import contract
from ib_gateway.adapters import repository


pytestmark = pytest.mark.usefixtures('mappers')


def test_get_by_conId(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyRepository(session)
    c1 = contract.Contract(conId=1, symbol='symbol-1')
    c2 = contract.Contract(conId=2, symbol='symbol-2')
    c3 = contract.Contract(conId=3, symbol='symbol-3')

    instrument_1 = contract.Instrument(symbol=c1.symbol)
    instrument_2 = contract.Instrument(symbol=c2.symbol)
    instrument_3 = contract.Instrument(symbol=c3.symbol)

    repo.add(instrument_1)
    repo.add(instrument_2)
    repo.add(instrument_3)

    assert repo.get_by_conId(conId=c1.conId) == instrument_1
    assert repo.get_by_conId(conId=c2.conId) == instrument_2
    assert repo.get_by_conId(conId=c3.conId) == instrument_3