import abc

from contracts.domain.contract import Instrument


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[Contract]

    def add(self, contract: Instrument):
        self._add(contract)
        self.seen.add(contract)

    def get(self, symbol) -> Instrument:
        instrument = self._get(symbol)
        if instrument:
            self.seen.add(instrument)
        return instrument

    @abc.abstractmethod
    def _add(self, instrument: Instrument):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, symbol) -> Instrument:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, instrument):
        self.session.add(instrument)

    def _get(self, symbol):
        return self.session.query(Instrument).filter_by(symbol=symbol).first()
