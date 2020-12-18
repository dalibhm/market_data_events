from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, ForeignKey,
    event,
)
from sqlalchemy.orm import mapper, relationship

import historical_data.domain.download
from historical_data.domain import instrument


metadata = MetaData()

instruments = Table(
    'instruments', metadata,
    Column('symbol', String(255), primary_key=True),
    Column('contract_id', String(255))
)

downloads = Table(
    'downloads', metadata,
    Column('id', String(255), primary_key=True),
    Column('contract_id', ForeignKey('instruments.contract_id')),
    Column('bar_size', String(255)),
    Column('what_to_show', String(255)),
    Column('use_rth', Integer),
    Column('start_date', String(255)),
    Column('end_date', String(255))  # ,
    # Column('eta', Date, nullable=True),
)


def start_mappers():
    downloads_mapper = mapper(historical_data.domain.download.Download, downloads)
    instruments_mapper = mapper(instrument.Instrument, instruments, properties={
        'downloads': relationship(
            downloads_mapper
        )
    })

@event.listens_for(instrument.Instrument, 'load')
def receive_load(instrument, _):
    instrument.events = []

