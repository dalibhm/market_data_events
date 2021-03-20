from gateway.domain.events import HistoricalRequest, DataSummary
from gateway.ib_gateway import ib_commands, ib_events
from gateway.services.data_handlers.historical_data_manager import HistoricalData


def test_historical_request():
    cmd = ib_commands.RequestHistoricalData(
        reqId=20,
        conId=148163036,
        endDateTime='20200622 00:00:00 GMT',
        durationStr='6 M',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=1,
        formatDate=1,
        keepUpToDate=False,
        chartOptions=[]
    )

    request = HistoricalRequest.from_command(cmd)
    assert 148163036 == request.conId


def test_data_summary():
    d1 = ib_events.HistoricalDataReceived(date="20201215", open=1, high=1, low=1, close=1, volume=1, wap=1, count=1)
    d2 = ib_events.HistoricalDataReceived(date="20201216", open=1, high=1, low=1, close=1, volume=1, wap=1, count=1)
    d3 = ib_events.HistoricalDataReceived(date="20201217", open=1, high=1, low=1, close=1, volume=1, wap=1, count=1)
    historical_data = HistoricalData(data=[d1, d2, d3])
    ds = DataSummary.from_historical_data(historical_data,
                                          ib_events.HistoricalDataEnded(
                                              start='20191213',
                                              end='20191220'
                                          ))
    assert "20201215" == ds.data_start_date
    assert "20201217" == ds.data_end_date
    assert 3 == ds.data_points_number
