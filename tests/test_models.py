import pytest
from converter.models import PayerList


@pytest.mark.parametrize('value', [
    '022021',
    '122021',
    '042022',
])
def test_validate_period_with_valid_data(value, payer):
    updated_payer = payer._replace(period=value)

    result = updated_payer.validate_period()
    assert result is not None


@pytest.mark.parametrize('value', [
    '222021',
    '1021',
    '',
    1,
    True,
    None,
])
def test_validate_period_with_invalid_data(value, payer):
    updated_payer = payer._replace(period=value)

    result = updated_payer.validate_period()
    assert result is None


@pytest.mark.parametrize('value', [
    '100.00',
    '101.11',
    '1000000.01',
    '11999923949494394.99'
    '0.01',
    '0.00',
])
def test_validate_amount_with_valid_data(value, payer):
    updated_payer = payer._replace(amount=value)

    result = updated_payer.validate_amount()
    assert result is not None


@pytest.mark.parametrize('value', [
    'money'
    '',
    '101',
    '1',
    '1199.9923949494394.99'
    '1199,394.99'
    'm.99'
    '0.0123',
    '0.0',
    '-100.00',
])
def test_validate_amount_with_invalid_data(value, payer):
    updated_payer = payer._replace(amount=value)

    result = updated_payer.validate_amount()
    assert result is None


def test_append_data_in_payer_list(payer):
    payer_list = PayerList()
    payer_list.append(payer)

    assert len(payer_list) == 1

    payer_list.append(payer)
    # records with same period and accounting are deleted
    assert len(payer_list) == 0

    new_payer = payer._replace(accounting='159233242')

    payer_list.append(payer)
    payer_list.append(new_payer)

    assert len(payer_list) == 2
