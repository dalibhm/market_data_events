# from typing import List, Dict, Callable, Type
# from historical_data.domain import events
# from historical_data.domain.download import Download
# from ib_gateway.events import HistoricalDataReceived, HistoricalDataEnded
#
#
# def handle(event: events.Event):
#     for handler in HANDLERS[type(event)]:
#         handler(event)
#
#
# def send_out_of_stock_notification(event: events.OutOfStock):
#     pass
#
#
# HANDLERS = {
#     events.OutOfStock: [send_out_of_stock_notification],
#
# }  # type: Dict[Type[events.Event], List[Callable]]
#
#
# def handle_data(event: HistoricalDataReceived, download: Download):
#     if event.reqId == download.request_id:
#         download.data.append(event)