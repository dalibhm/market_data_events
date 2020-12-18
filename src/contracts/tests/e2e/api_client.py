import requests, json

from contracts.entrypoints.flask_app import add_contract


def post_to_add_contract():
    url = 'http://127.0.0.1:5000'
    contract = dict(conId=1, symbol='test-symbol')
    r = requests.post(
        f'{url}/add_batch',
        json=json.dumps(contract)
    )
    assert r.status_code == 201

