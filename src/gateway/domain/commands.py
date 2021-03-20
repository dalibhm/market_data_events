from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

from gateway.domain.contract_v0 import Contract, DerivativeSecTypes, ContractDetails


class Command:
    created_on: datetime


@dataclass
class CreateContract(Command):
    contract: Contract


@dataclass
class WriteContract(Command):
    contract: Contract


@dataclass
class WriteDerivativeSecTypes(Command):
    conId: int
    symbol: str
    derivative_sec_type: List[str]


@dataclass
class WriteContractDetails(Command):
    conId: int
    symbol: str
    contract: ContractDetails
