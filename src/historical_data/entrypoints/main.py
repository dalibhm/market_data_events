from gateway.ib_gateway.ib_commands import RequestHistoricalData
from historical_data.domain import commands


def add_request(historical_data_request: RequestHistoricalData, data_range):
    cmd = commands.CreateRequest(historical_data_request, data)