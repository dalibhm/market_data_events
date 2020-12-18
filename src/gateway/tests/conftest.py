# pylint: disable=redefined-outer-name
import time
from pathlib import Path

import pytest
import requests
from tenacity import retry, stop_after_delay

from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

# from ib_gateway.adapters.sql_alchemy import metadata, start_mappers
from gateway.adapters import sql_alchemy
from gateway import config


@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    sql_alchemy.metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    sql_alchemy.start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def session_factory(in_memory_db):
    contracts = sql_alchemy.contracts
    sql_alchemy.start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(config.get_api_url())


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail('Postgres never came up')


@pytest.fixture(scope='session')
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    sql_alchemy.metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session_factory(postgres_db):
    sql_alchemy.start_mappers()
    yield sessionmaker(bind=postgres_db)
    clear_mappers()


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / '../entrypoints/flask_app.py').touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
