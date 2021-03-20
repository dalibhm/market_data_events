import pytest

from historical_data.domain import instrument
from historical_data.adapters import repository

pytestmark = pytest.mark.usefixtures('mappers')


def test_get_by_conId(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = repository.SqlAlchemyRepository(session)
    c1 = instrument.Request(conId=1, symbol='symbol-1')
    c2 = instrument.Request(conId=2, symbol='symbol-2')
    c3 = instrument.Request(conId=3, symbol='symbol-3')

    instrument_1 = instrument.Instrument(symbol=c1.symbol, conId=c1.conId)
    instrument_2 = instrument.Instrument(symbol=c2.symbol, conId=c2.conId)
    instrument_3 = instrument.Instrument(symbol=c3.symbol, conId=c3.conId)

    repo.add(instrument_1)
    repo.add(instrument_2)
    repo.add(instrument_3)

    assert repo.get_by_conId(conId=c1.conId) == instrument_1
    assert repo.get_by_conId(conId=c2.conId) == instrument_2
    assert repo.get_by_conId(conId=c3.conId) == instrument_3
