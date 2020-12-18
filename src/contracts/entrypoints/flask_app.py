from datetime import datetime
from flask import Flask, jsonify, request

from contracts import views
from contracts.adapters import sql_alchemy
from contracts.service_layer import handlers, unit_of_work

app = Flask(__name__)
sql_alchemy.start_mappers()


# adding contracts should be easier from the program
# I need an extra entrypoint that loads the module from another module

@app.route("/contracts", methods=['POST'])
def add_contract():
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    handlers.add_contract(
        contract=request.json['contract'],
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
