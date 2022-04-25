import pytest


@pytest.mark.parametrize(
    'token, response_code', [('patient_token', 200), ('doctor_token', 403), ('technician_token', 403)]
)
def test_access_to_analyses_list(client, token, response_code, request):
    response = client.get('/analyses', headers={'x-access-tokens': f'{request.getfixturevalue(token)}'})
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'token, response_code', [('patient_token', 403), ('doctor_token', 200), ('technician_token', 403)]
)
def test_access_to_doctor_orders(client, token, response_code, request):
    response = client.get('/doctor_orders', headers={'x-access-tokens': f'{request.getfixturevalue(token)}'})
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'token, response_code', [('patient_token', 403), ('doctor_token', 403), ('technician_token', 200)]
)
def test_access_to_filling_results(client, token, response_code, order, request):
    response = client.patch(
        '/fill_result',
        data={'order_id': order.id, 'result': 'You are ok'},
        headers={'x-access-tokens': f'{request.getfixturevalue(token)}'},
    )
    assert response.status_code == response_code
