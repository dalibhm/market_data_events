from contracts.service_layer import unit_of_work


def get_contract_by_contract_id(contract_id: int, uow: unit_of_work):
    with uow:
        results = list(uow.session.execute(
            'SELECT conId, contract_id, ... FROM contracts WHERE conId = :conId',
            dict(conId=contract_id)
        ))
    return [dict(r) for r in results]