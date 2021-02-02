import os

import pytest
from loguru import logger
from mixer.main import mixer

from converter.models import Payer

mixer.faker.locale = 'ru'


def pytest_sessionstart(session):
    logger.disable('test')


def pytest_sessionfinish(session):
    os.remove('result.log')


class PayerObj:
    record_number = int
    file_name = str
    file_date = str
    accounting = str
    full_name = str
    address = str
    period = str
    amount = str


@pytest.fixture
def payer() -> 'Payer':
    """Is instance of Payer record from xml file with valid data."""
    mixer.register(
        PayerObj,
        record_number=lambda: mixer.faker.small_positive_integer(),
        file_name=lambda: 'input.xml',
        file_date=lambda: '01.02.2021',
        accounting=lambda: str(mixer.faker.small_positive_integer()),
        full_name=lambda: mixer.faker.name(),
        address=lambda: mixer.faker.address(),
        period=lambda: '012021',
        amount=lambda: '100.00',
    )
    payer_obj = mixer.blend(PayerObj)
    return Payer(**payer_obj.__dict__)
