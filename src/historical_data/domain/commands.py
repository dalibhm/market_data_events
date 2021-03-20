from dataclasses import dataclass, field
from datetime import datetime

from historical_data.domain.instrument import Request, DataSummary


@dataclass
class Command:
    created_on: datetime = field(default_factory=datetime.now)


@dataclass
class AddRequest(Command):
    symbol: str = field(default="")
    request: Request = field(default=None)
