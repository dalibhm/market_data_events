from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, Float, Boolean, ForeignKey,
    event, create_engine
)
from sqlalchemy.orm import mapper, relationship

from gateway import config
from gateway.domain import contract_v0

metadata = MetaData()

instruments = Table(
    'instruments', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('symbol', String, index=True),
    Column('conId', Integer, index=True)
)

contracts = Table(
    'contracts', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('conId', Integer, index=True),
    # Column('instrument_id', Integer, ForeignKey('instruments.id')),
    Column('symbol', String(10), index=True),
    # Column('symbol', String(10)),
    Column('secType', String(10)),
    Column('lastTradeDateOrContractMonth', String),
    Column('strike', Float),  # float !!
    Column('right', String),
    Column('multiplier', String),
    Column('exchange', String),
    Column('primaryExchange', String),
    Column('currency', String),
    Column('localSymbol', String),
    Column('tradingClass', String),
    Column('includeExpired', Boolean),
    Column('secIdType', String),  # CUSIP;SEDOL;ISIN;RIC
    Column('secId', String),
    Column('comboLegsDescrip', String),  # type: str
    Column('comboLegs', String),  # None  # type: list<ComboLeg>
    Column('deltaNeutralContract', String),  # None
)

derivatives_sec_types = Table(
    'derivatives_sec_types', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('CFD', Boolean),
    Column('OPT', Boolean),
    Column('IOPT', Boolean),
    Column('WAR', Boolean),
    Column('BAG', Boolean),
    # Column('contract', String, index=True, nullable=False)
)

historical_data_map = Table(
    'historical_data_map', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('instrument_id', Integer, ForeignKey('instruments.id')),
    Column('contract_id', Integer, ForeignKey('contracts.id')),
    Column('derivatives_sec_types_id', Integer, ForeignKey('derivatives_sec_types.id')),
)


def start_mappers():
    contracts_mapper = mapper(contract_v0.Contract, contracts)
    derivatives_sec_types_mapper = mapper(contract_v0.DerivativeSecTypes, derivatives_sec_types)
    mapper(contract_v0.Instrument,
           instruments,
           properties={
               '_contract': relationship(
                   contracts_mapper,
                   secondary=historical_data_map,
                   uselist=False
               ),
               '_derivative_sec_types': relationship(
                   derivatives_sec_types_mapper,
                   secondary=historical_data_map,
                   uselist=False
               )
           }
           )
    engine = create_engine(config.get_postgres_uri(), echo=True)
    metadata.create_all(engine)
    # instruments.create(engine)
    # contracts.create(engine)
    # derivatives_sec_types.create(engine)


@event.listens_for(contract_v0.Instrument, 'load')
def receive_load(instrument, _):
    instrument.events = []
