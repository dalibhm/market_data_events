from datetime import datetime
from flask import Flask, jsonify, request

from ib_gateway.domain import commands

from ib_gateway.services import handlers
# from ib_gateway.entrypoints.app.flask_app import bus

from . import main

from flask import current_app
# from ib_gateway.entrypoints.app.flask_app import app


@main.route('/')
def index():
    return 'ib gateway'


@main.route("/HistoricalData", methods=['POST'])
def reqHistoricalData():
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    handlers.reqHistoricalData(
        commands.RequestHistoricalData(
            reqId=request.json['reqId'],
            contract=request.json['contract'],
            endDateTime=request.json['endDateTime'],
            durationStr=request.json['durationStr'],
            barSizeSetting=request.json['barSizeSetting'],
            whatToShow=request.json['whatToShow'],
            useRTH=request.json['useRTH'],
            formatDate=request.json['formatDate'],
            keepUpToDate=request.json['keepUpToDate'],
            chartOptions=request.json['chartOptions']
        ),
        uow=unit_of_work.SqlAlchemyUnitOfWork()
    )
    return 'OK', 201


@main.route("/MatchingSymbols", methods=['POST'])
def reqMatchingSymbols():
    # eta = request.json['eta']
    # if eta is not None:
    #     eta = datetime.fromisoformat(eta).date()
    cmd = commands.RequestMatchingSymbols(
        reqId=request.json['reqId'],
        symbol=request.json['symbol']
    )
    bus.handle(cmd)
    # ib_gateway_connection=IbGatewayConnection(),
    # uow=None
    # )
    return 'OK', 201
