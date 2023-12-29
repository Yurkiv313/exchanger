from _decimal import Decimal
from models.rate_api_client import RateApiClient
from models.invalid_balance_error import InvalidBalanceError
from models.currency_type_error import CurrencyTypeError
from currency_manager import CurrencyManager


class Controller:

    def __init__(self):
        self.currency_manager = CurrencyManager()
        self.rate_api_client = RateApiClient()
        self.currencies = self.currency_manager.read_currency()
        self.national_currency = 'UAH'
        self.allowed_foreign_currencies = [item for item in self.currencies if item.name != self.national_currency][0]

    @staticmethod
    def show_commands():
        print('1 - COURSE')
        print('2 - EXCHANGE')
        print('3 - STOP')

    def get_available_currencies(self):
        return [x.name for x in self.currencies]

    def get_courses_by_currency(self, from_curr, to_curr):
        currency_names = self.get_available_currencies()
        if from_curr not in currency_names or to_curr not in currency_names:
            raise CurrencyTypeError('INVALID CURRENCY')
        if from_curr == to_curr:
            return 1

        currencies = self.rate_api_client.get_courses()
        national_currency_case = from_curr == self.national_currency
        item_to_find = to_curr if national_currency_case else from_curr
        currency = [item for item in currencies if item['ccy'] == item_to_find][0]
        return Decimal(currency['sale']) if national_currency_case else Decimal(currency['buy'])

    def read_balance(self):
        return self.currency_manager.read_currency()

    def exchange(self, from_curr, to_curr, amount):
        rate = self.get_courses_by_currency(from_curr, to_curr)
        converted_amount = rate * amount if to_curr == self.national_currency else amount / rate
        list_currency = self.read_balance()
        updated_list = self.recalculate_balance(amount, converted_amount, list_currency, from_curr, to_curr)
        self.currency_manager.write_currency(updated_list)
        return str(converted_amount), str(rate)

    @staticmethod
    def recalculate_balance(amount, converted_amount, list_currency, from_curr, to_curr):
        currency_balance = [item for item in list_currency if item.name == to_curr][0]
        if currency_balance.balance < converted_amount:
            raise InvalidBalanceError(
                f'UNAVAILABLE, REQUIRED BALANCE, {converted_amount}, AVAILABLE, {currency_balance.balance}')
        for curr_balance in list_currency:
            if curr_balance.name == from_curr:
                curr_balance.balance = curr_balance.balance + amount
            if curr_balance.name == to_curr:
                curr_balance.balance = curr_balance.balance - converted_amount
        return list_currency

    def balance_to_curr(self, to_curr):
        list_currency = self.read_balance()
        currency_balance = [item for item in list_currency if item.name == to_curr][0]
        return currency_balance.balance
