from datetime import datetime

import pytest

from historical_data.domain import commands, events
from historical_data.domain.instrument import Request, DataSummary
from historical_data.services import unit_of_work

from historical_data.services.handlers import add_request  # , get_contract_by_symbol


def insert_request(session, conId, symbol, version):
    session.execute(
        'INSERT INTO instruments (conId, symbol) VALUES (:conId, :symbol)',
        dict(conId=conId, symbol=symbol),
    )

    session.execute(
        """INSERT INTO requests (id, conId, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH,
        formatDate, keepUpToDate)
        VALUES (:id, :conId, :endDateTime, :durationStr, :barSizeSetting, :whatToShow, :useRTH,
        :formatDate, :keepUpToDate)""",
        dict(id=12, conId=conId, endDateTime='20191220 00:00:00 GMT', durationStr='6 M', barSizeSetting='1 day',
             whatToShow='TRADES', useRTH=0, formatDate=1, keepUpToDate=False)
    )

    session.execute(
        """INSERT INTO data_summary (id, start_date, end_date, data_start_date, data_end_date, 
        data_points_number)
        VALUES (:id, :start_date, :end_date, :data_start_date, :data_end_date, 
        :data_points_number)""",
        dict(id=2, start_date=datetime(2020, 6, 1), end_date=datetime(2020, 6, 1),
             data_start_date=datetime(2020, 6, 1), data_end_date=datetime(2020, 12, 1),
             data_points_number=124)
    )

    session.execute(
        """INSERT INTO request_data_summary_map (id, request_id, data_summary_id)
        VALUES (:id, :request_id, :data_summary_id)""",
        dict(id=1, request_id=12, data_summary_id=2)
    )


@pytest.fixture
def sample_request():
    data_summary = DataSummary(
        start_date=datetime(2020, 6, 1),
        end_date=datetime(2020, 12, 1),
        data_start_date=datetime(2020, 6, 1),
        data_end_date=datetime(2020, 12, 1),
        data_points_number=124
    )
    request = Request(conId=1, endDateTime='20191220 00:00:00 GMT', durationStr='6 M', barSizeSetting='1 day',
                      whatToShow='TRADES', useRTH=1, formatDate=1, keepUpToDate=False,
                      data_summary=data_summary)
    return request


def test_uow_add_request(session_factory, sample_request):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        add_request(
            cmd=commands.AddRequest(
                symbol='test-symbol',
                request=sample_request
            ),
            uow=uow)

    with uow:
        instrument = uow.instruments.get(conId=1)
        assert 'test-symbol' == instrument.symbol


def test_uow_get_existing_request(session_factory, sample_request):
    session = session_factory()
    insert_request(session, conId=1, symbol='test-symbol-2', version=None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        instrument = uow.instruments.get(conId=1)
        assert instrument.symbol == "test-symbol-2"
        assert instrument.requests[0] == sample_request


def test_uow_get_inexisting_request(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        instrument = uow.instruments.get(conId=1)
        assert instrument is None

#TODO: test add a request to an existing instrument

# def test_uow_add_contract_to_existing_instrument(session_factory):
#     session = session_factory()
#     insert_contract(session, symbol='test-symbol', version=None)
#     session.commit()
#
#     uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory, entity_type=Contract)
#     new_contract = Contract()
#     new_contract.symbol = 'test-symbol'
#
#     with uow:
#         contract = uow.entities.get(symbol='test-symbol')
#         assert 'test-symbol' == contract.symbol
#
#     add_contract(cmd=commands.CreateContract(1, "test-symbol", 100, None), uow=uow)
#
#     with uow:
#         instrument = uow.instruments.get('test-symbol')
#         assert 2 == len(instrument.contracts)
