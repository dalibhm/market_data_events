from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, Float, Boolean, ForeignKey,
    event, create_engine
)
from sqlalchemy.orm import mapper, relationship

from gateway import config
from gateway.domain import contract

metadata = MetaData()

instruments = Table(
    'instruments', metadata,
    Column('symbol', String),
    Column('conId', Integer, primary_key=True)
)

contracts = Table(
    'contracts', metadata,
    Column('conId', Integer(), ForeignKey('instruments.conId'), primary_key=True),
    Column('symbol', String(10)),
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
    Column('conId', Integer, ForeignKey('instruments.conId'), primary_key=True),
    Column('CFD', Boolean),
    Column('OPT', Boolean),
    Column('IOPT', Boolean),
    Column('WAR', Boolean),
    Column('BAG', Boolean),
    # Column('contract', String, index=True, nullable=False)
)


def start_mappers():
    contracts_mapper = mapper(contract.Contract, contracts)
    derivatives_sec_types_mapper = mapper(contract.DerivativeSecTypes, derivatives_sec_types)
    mapper(contract.Instrument,
           instruments,
           properties={
               '_contract': relationship(
                   contracts_mapper,
                   uselist=False
               ),
               '_derivative_sec_types': relationship(
                   derivatives_sec_types_mapper,
                   uselist=False
               )
           }
           )
    engine = create_engine(config.get_postgres_uri())
    metadata.create_all(engine)
    # instruments.create(engine)
    # contracts.create(engine)
    # derivatives_sec_types.create(engine)


@event.listens_for(contract.Instrument, 'load')
def receive_load(instrument, _):
    instrument.events = []
