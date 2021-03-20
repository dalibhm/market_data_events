from datetime import datetime

from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, Boolean, ForeignKey,
    event,
)
from sqlalchemy.orm import mapper, relationship

import historical_data.domain.download
from historical_data.domain import instrument

metadata = MetaData()

instruments = Table(
    'instruments', metadata,
    # Column('symbol', String(255)),
    Column('conId', String(255), primary_key=True)
)

downloads = Table(
    'downloads', metadata,
    Column('id', String(255), primary_key=True),
    Column('contract_id', ForeignKey('instruments.conId')),
    Column('bar_size', String(255)),
    Column('what_to_show', String(255)),
    Column('use_rth', Integer),
    Column('start_date', String(255)),
    Column('end_date', String(255))  # ,
    # Column('eta', Date, nullable=True),
)

requests = Table(
    'requests', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('conId', ForeignKey('instruments.conId')),
    Column('endDateTime', String(255)),
    Column('durationStr', String(255)),
    Column('barSizeSetting', String),
    Column('whatToShow', String(255)),
    Column('useRTH', Integer),
    Column('formatDate', Integer),
    Column('keepUpToDate', Boolean),
    Column('insert_date', Date, default=datetime.now),
)

request_data_summary_map = Table(
    'request_data_summary_map', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('request_id', Integer, ForeignKey('requests.id')),
    Column('data_summary_id', Integer, ForeignKey('data_summary.id')),
)

data_summary = Table(
    'data_summary', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('start_date', Date),
    Column('end_date', Date),
    Column('data_start_date', Date),
    Column('data_end_date', Date),
    Column('data_points_number', Integer),
    # Column('eta', Date, nullable=True),
)


def start_mappers():
    # downloads_mapper = mapper(historical_data.domain.download.Download, downloads)
    data_summary_mapper = mapper(instrument.DataSummary, data_summary)

    requests_mapper = mapper(instrument.Request, requests,
                             properties={
                                 'data_summary': relationship(data_summary_mapper,
                                                              secondary=request_data_summary_map,
                                                              uselist=False
                                                              )
                             })
    instruments_mapper = mapper(instrument.Instrument, instruments, properties={
        # 'downloads': relationship(
        #     downloads_mapper
        # ),
        'requests': relationship(
            requests_mapper
        )
    })


@event.listens_for(instrument.Instrument, 'load')
def receive_load(instrument, _):
    instrument.events = []
