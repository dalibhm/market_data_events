from datetime import datetime
from flask import Flask, jsonify, request as flask_request

from historical_data.adapters import sql_alchemy
from historical_data.domain import commands
from historical_data.domain.instrument import Request, DataSummary
from historical_data.services import handlers, unit_of_work
from historical_data import bootstrap

bus = bootstrap.bootstrap()

app = Flask(__name__)


# adding contracts should be easier from the program
# I need an extra entrypoint that loads the module from another module

@app.route("/request", methods=['POST'])
def add_request():
    bus.handle(
        message=commands.AddRequest(
            symbol=flask_request.json['symbol'],
            request=Request(
                conId=flask_request.json['conId'],
                endDateTime=flask_request.json['endDateTime'],
                durationStr=flask_request.json['durationStr'],
                barSizeSetting=flask_request.json['barSizeSetting'],
                whatToShow=flask_request.json['whatToShow'],
                useRTH=flask_request.json['useRTH'],
                formatDate=flask_request.json['formatDate'],
                keepUpToDate=flask_request.json['keepUpToDate'],
                data_summary=DataSummary(
                    start_date=flask_request.json['start_date'],
                    end_date=flask_request.json['end_date'],
                    data_start_date=flask_request.json['data_start_date'],
                    data_end_date=flask_request.json['data_end_date'],
                    data_points_number=flask_request.json['data_points_number']
                )
            )
        )
    )
    return 'OK', 201


@app.route("/contracts/<string:symbol>", methods=['GET'])
def get_contract_by_symbol(symbol: str):
    try:
        contract = views.get_contract_by_symbol(symbol=symbol, uow=unit_of_work.SqlAlchemyUnitOfWork())
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return jsonify(contract), 200


@app.route("/contracts/<int:contract_id>", methods=['GET'])
def get_contract_by_id(contract_id: int):
    try:
        contract = views.get_contract_by_contract_id(contract_id=contract_id, uow=unit_of_work.SqlAlchemyUnitOfWork())
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return jsonify(contract), 200
