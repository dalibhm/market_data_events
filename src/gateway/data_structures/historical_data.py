from gateway.ib_gateway.ib_events import HistoricalDataReceived


class HistoricalData:
    def __init__(self, data: HistoricalDataReceived = None):
        self.data = data or []

    def add(self, data_in):
        self.data.append(data_in)

    def start_date(self):
        return next(b.date for b in sorted(self.data))

    def end_date(self):
        return next(b.date for b in sorted(self.data, reverse=True))

    def data_points_number(self):
        return len(self.data)
