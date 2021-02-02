import re
from collections import UserList
from datetime import datetime
from typing import NamedTuple

from loguru import logger


class Payer(NamedTuple):
    record_number: int
    file_name: str
    file_date: str
    accounting: str
    full_name: str
    address: str
    period: str
    amount: float

    def __repr__(self) -> str:
        return f'<{self.accounting}, {self.full_name}, amount={self.amount}>'

    def validate_period(self) -> None or 'Payer':
        try:
            datetime.strptime(self.period, '%m%Y')
        except (ValueError, TypeError):
            logger.error(
                f'Error at payer number {self.record_number} - {self.full_name} invalid period format. '
                f'Invalid month or year in period "{self.period}".')
            return
        return self

    def validate_amount(self) -> None or 'Payer':
        error_message = f'Error at payer number {self.record_number} - {self.full_name} invalid money format. ' \
                        f'The amount "{self.amount}" does not match the format.'

        if self.amount.count('.') > 2:
            logger.error(error_message)
            return

        valid = re.compile(r'\d+[.]\d{2}?')
        if not valid.match(self.amount):
            logger.error(error_message)
            return
        return self

    def check_required_fields(self):
        if not self.accounting or not self.full_name or not self.period:
            logger.error(f'The payer number {self.record_number} is missing one of the required parameters.')
            return
        return self

    def validate_values(self) -> None or 'Payer':
        payer = self.check_required_fields()
        if not payer:
            return

        payer = self.validate_period()
        payer = self.validate_amount()

        if not payer:
            return
        return self


class PayerList(UserList):

    def append(self, item):
        for list_item in self:
            if f'{item.accounting}{item.period}' == f'{list_item.accounting}{list_item.period}':
                logger.error(
                    f'There are duplicate entries with the account '
                    f'"{item.accounting}" and period "{item.period}".',
                )
                self.remove(list_item)
                return
        self.data.append(item)
