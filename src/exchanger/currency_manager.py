import csv
from _decimal import Decimal
from models.currency_balance import CurrencyBalance


class CurrencyManager:

    def __init__(self):
        self.filename = '/Users/macbookair/hillel_06_12/src/exchanger/models/data/currency.csv'

    def write_currency(self, currency_balance_list):
        with open(self.filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for currency_balance in currency_balance_list:
                writer.writerow((currency_balance.name, currency_balance.balance))

    def read_currency(self):
        with open(self.filename, newline='') as csvfile:
            currency_balance_list = []
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                currency_balance_list.append(CurrencyBalance(row[0], Decimal(row[1])))
        return currency_balance_list


if __name__ == "__main__":
    pass
