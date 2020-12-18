from abc import ABC
from datetime import datetime


class DomainEvent(ABC):
    created_on: datetime


class Command(ABC):
    created_on: datetime
