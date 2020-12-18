import pytest

from contracts.tests.e2e import api_client


# @pytest.mark.usefixtures('postgres_db')
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_202_and_batch_is_allocated():
    r = api_client.post_to_add_contract()
    assert r.status_code == 202