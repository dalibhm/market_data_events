import abc

from gateway.domain.contract import Instrument, Contract, DerivativeSecTypes, ContractDetails


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[Instrument]

    def add(self, instrument: Instrument):
        self._add(instrument)
        self.seen.add(instrument)

    def get(self, symbol) -> Instrument:
        instrument = self._get(symbol)
        if instrument:
            self.seen.add(instrument)
        return instrument

    def get_by_conId(self, conId) -> Instrument:
        instrument = self._get_by_conId(conId)
        if instrument:
            self.seen.add(instrument)
        return instrument

    @abc.abstractmethod
    def _add(self, instrument: Instrument):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, symbol) -> Instrument:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_conId(self, conId) -> Instrument:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, instrument):
        self.session.add(instrument)

    def _get(self, symbol):
        return self.session.query(Instrument).filter_by(symbol=symbol).first()

    def _get_by_conId(self, conId):
        if self.session.query(Instrument).count() > 0:
            return self.session.query(Instrument).filter(Instrument.conId == conId).first()
        else:
            return None

# class ContractRepository(SqlAlchemyRepository):
#     Instrument = Contract
#
#     def __init__(self, session):
#         super().__init__()
#         self.session = session
#
#     def _get(self, conId):
#         return self.session.query(self.Instrument).filter(conId=conId)
#
#
# class ContractDescriptionRepository(SqlAlchemyRepository):
#     Instrument = ContractDescription
#
#     def __init__(self, session):
#         super().__init__()
#         self.session = session
#
#     def _get(self, conId):
#         return self.session.query(self.Instrument).filter(conId=conId)
#
#
# class ContractDetailsRepository(SqlAlchemyRepository):
#     Instrument = ContractDetails
#
#     def __init__(self, session):
#         super().__init__()
#         self.session = session
#
#     def _get(self, conId):
#         return self.session.query(self.Instrument).filter(conId=conId)
