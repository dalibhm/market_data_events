import os

from ib_gateway.entrypoints.app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# @app.route("/contracts/<string:symbol>", methods=['GET'])
# def get_contract_by_symbol(symbol: str):
#     try:
#         contract = views.get_contract_by_symbol(symbol=symbol, uow=unit_of_work.SqlAlchemyUnitOfWork())
#     except Exception as e:
#         return jsonify({'message': str(e)}), 400
#
#     return jsonify(contract), 200
