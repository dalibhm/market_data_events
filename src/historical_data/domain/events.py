from dataclasses import dataclass

from common.domain_events import DomainEvent, Command


@dataclass
class Event:
    pass


@dataclass
class CreateDownload(Command):
    tenant_id: str
    download_id: str
    bar_size: str
    what_to_show: str
    use_rth: int
    start_date: str
    end_date: str


@dataclass
class DownloadCreated(DomainEvent):
    tenant_id: str
    download_id: str
    bar_size: str
    what_to_show: str
    use_rth: int
    start_date: str
    end_date: str


@dataclass
class RequestSubmitted(DomainEvent):
    tenant_id: str
    download_id: str
    request_id: int
