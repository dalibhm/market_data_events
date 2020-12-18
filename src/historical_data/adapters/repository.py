import abc

from historical_data.domain import instrument


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[instrument.Instrument]

    def add(self, instrument: instrument.Instrument):
        self._add(instrument)
        self.seen.add(instrument)

    def get(self, symbol) -> instrument.Instrument:
        instrument = self._get(symbol)
        if instrument:
            self.seen.add(instrument)
        return instrument

    @abc.abstractmethod
    def _add(self, instrument: instrument.Instrument):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, symbol) -> instrument.Instrument:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, symbol):
        return self.session.query(instrument.Instrument).filter_by(symbol=symbol).first()
