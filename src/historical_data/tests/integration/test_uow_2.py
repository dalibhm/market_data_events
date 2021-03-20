# pylint: disable=broad-except
import threading
import time
import traceback
from typing import List
import pytest

import historical_data.domain.download
from historical_data.domain import instrument
from historical_data.service_layer import unit_of_work
from .random_refs import random_sku, random_batchref, random_orderid


def insert_download(session, id, symbol, code, bar_size, what_to_show, use_rth, start_date, end_date):
    session.execute(
        'INSERT INTO instruments (symbol, code) VALUES (:symbol, :code)',
        dict(symbol=symbol, code=code),
    )
    session.execute(
        'INSERT INTO downloads (id, symbol, bar_size, what_to_show, use_rth, start_date, end_date)'
        ' VALUES (:id, :symbol, :bar_size, :what_to_show, :use_rth, :start_date, :end_date)',
        dict(id=id, symbol=symbol, bar_size=bar_size, what_to_show=what_to_show, use_rth=use_rth, start_date=start_date,
             end_date=end_date)
    )


def get_allocated_batch_ref(session, orderid, symbol):
    [[orderlineid]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid=orderid, sku=sku)
    )
    [[batchref]] = session.execute(
        'SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id'
        ' WHERE orderline_id=:orderlineid',
        dict(orderlineid=orderlineid)
    )
    return batchref


def test_uow_check_new_download(session_factory):
    session = session_factory()
    insert_download(session, 'download1', 'symbol1', 'code1',
                    bar_size='5 min', what_to_show='TRADES', use_rth=1,
                    start_date='2020-06-01', end_date='2020-08-01')
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        instrument = uow.instruments.get(symbol='symbol1')
        download = historical_data.domain.download.Download(id='ID-2',
                                                            bar_size='5 min', what_to_show='TRADES', use_rth=1,
                                                            start_date='2020-10-01', end_date='2020-11-01')
        download_checked = instrument.check_download_dates_against_previous(download)
        uow.commit()

    # batchref = get_allocated_batch_ref(session, 'o1', 'HIPSTER-WORKBENCH')
    assert download_checked == historical_data.domain.download.Download(id='ID-CHECK',
                                                                        bar_size='5 min', what_to_show='TRADES', use_rth=1,
                                                                        start_date='2020-08-01', end_date='2020-11-01')


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []


def try_to_allocate(orderid, sku, exceptions):
    line = instrument.OrderLine(orderid, sku, 10)
    try:
        with unit_of_work.SqlAlchemyUnitOfWork() as uow:
            product = uow.products.get(sku=sku)
            product.allocate(line)
            time.sleep(0.2)
            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)


@pytest.mark.skip
def test_concurrent_updates_to_version_are_not_allowed(postgres_session_factory):
    sku, batch = random_sku(), random_batchref()
    session = postgres_session_factory()
    insert_batch(session, batch, sku, 100, eta=None, product_version=1)
    session.commit()

    order1, order2 = random_orderid(1), random_orderid(2)
    exceptions = []  # type: List[Exception]
    try_to_allocate_order1 = lambda: try_to_allocate(order1, sku, exceptions)
    try_to_allocate_order2 = lambda: try_to_allocate(order2, sku, exceptions)
    thread1 = threading.Thread(target=try_to_allocate_order1)
    thread2 = threading.Thread(target=try_to_allocate_order2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    [[version]] = session.execute(
        "SELECT version_number FROM products WHERE sku=:sku",
        dict(sku=sku),
    )
    assert version == 2
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in str(exception)

    orders = list(session.execute(
        "SELECT orderid FROM allocations"
        " JOIN batches ON allocations.batch_id = batches.id"
        " JOIN order_lines ON allocations.orderline_id = order_lines.id"
        " WHERE order_lines.sku=:sku",
        dict(sku=sku),
    ))
    assert len(orders) == 1
    with unit_of_work.SqlAlchemyUnitOfWork() as uow:
        uow.session.execute('select 1')
