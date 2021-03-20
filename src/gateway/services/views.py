from gateway.domain.contract_v0 import Contract


def contract(conId, uow) -> Contract:
    with uow:
        results = list(uow.session.execute(
            'SELECT * FROM contracts WHERE "conId" = :conId',
            dict(conId=conId)
        ))
        return [Contract(**dict(r)) for r in results]