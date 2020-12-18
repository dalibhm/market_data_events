from historical_data.domain.instrument import Instrument
from historical_data.domain.download import Download


def first_download():
    return Download(id='ID-1', bar_size='5 min', what_to_show='TRADES', use_rth=1, start_date='2020-06-01', end_date='2020-08-01')


def second_download():
    return Download(id='ID-2', bar_size='5 min', what_to_show='TRADES', use_rth=1, start_date='2020-10-01', end_date='2020-11-01')


def test_first_download():
    instrument = Instrument(symbol="AA", code='01', downloads=[])
    download = first_download()
    download_out = instrument.check_download_dates_against_previous(download)
    assert download_out == download


def test_different_download():
    instrument = Instrument(symbol="AA", code='01', downloads=[first_download()])
    download_2 = second_download()
    download_out = instrument.check_download_dates_against_previous(download_2)
    assert download_out.start_date == '2020-08-01'
    assert download_out.end_date == '2020-11-01'
    assert download_out == Download(id='whatever id',
                                    bar_size='5 min',
                                    what_to_show='TRADES',
                                    use_rth=1,
                                    start_date='2020-08-01', end_date='2020-11-01')
