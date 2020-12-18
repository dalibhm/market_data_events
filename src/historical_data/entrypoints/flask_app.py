from datetime import datetime
from flask import Flask, jsonify, request


from historical_data.adapters import sql_alchemy
from historical_data.domain import commands
from historical_data.service_layer import handlers, unit_of_work

app = Flask(__name__)
sql_alchemy.start_mappers()


# adding contracts should be easier from the program
# I need an extra entrypoint that loads the module from another module

@app.route("/download", methods=['POST'])
def add_contract():
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    handlers.add_download(
        cmd=commands.CreateDownload(symbol=request.json['symbol'],
                                    secType=request.json['secType'],
                                    lastTradeDateOrContractMonth=request.json['lastTradeDateOrContractMonth'],
                                    strike=request.json['strike'],
                                    right=request.json['right'],
                                    params=request.json['params']),
        uow=unit_of_work.SqlAlchemyUnitOfWork()
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
