from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, Float, Boolean, ForeignKey,
    event,
)
from sqlalchemy.orm import mapper, relationship
from ibapi.contract import Contract as IbContract
from contracts.domain import contract

metadata = MetaData()

contracts = Table(
    'contracts', metadata,
    Column('conId', Integer, primary_key=True),
    Column('symbol', ForeignKey('instruments.symbol')),
    Column('secType', String, index=True, nullable=False),
    Column('lastTradeDateOrContractMonth', String),
    Column('strike', Float),  # float !!
    Column('right', String),
    Column('multiplier', String),
    Column('exchange', String, primary_key=True, index=True),
    Column('primaryExchange', String, index=True),
    Column('currency', String, index=True),
    Column('derivativeSecTypes', String, index=True),
    Column('localSymbol', String),
    Column('tradingClass', String),
    Column('includeExpired', Boolean),
    Column('secIdType', String),  # CUSIP;SEDOL;ISIN;RIC
    Column('secId', String),

    Column('comboLegsDescrip', String),  # type: str
    Column('comboLegs', String),  # None  # type: list<ComboLeg>
    Column('deltaNeutralContract', String)  # None
)

instruments = Table(
    'instruments', metadata,
    Column('symbol', String, primary_key=True)  # ,
    # Column('contract', String, index=True, nullable=False)
)


def start_mappers():
    contracts_mapper = mapper(IbContract, contracts)
    instruments_mapper = mapper(contract.Instrument, instruments,
                                properties={
                                    'contracts': relationship(IbContract),
                                })


@event.listens_for(contract.Instrument, 'load')
def receive_load(instrument, _):
    instrument.events = []
