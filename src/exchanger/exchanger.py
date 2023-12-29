from _decimal import Decimal
from controller import Controller
from models.invalid_balance_error import InvalidBalanceError
from models.currency_type_error import CurrencyTypeError


def main(controller):
    while True:
        controller.show_commands()
        ch = input('Action: ')
        match ch:
            case '1':
                print('AVAILABLE CURRENCY:', end=" ")
                print(*(controller.get_available_currencies()), sep=", ")
                try:
                    from_curr = (input('Enter from currency: ').upper())
                    to_curr = (input('Enter to currency: ').upper())
                    rate = controller.get_courses_by_currency(from_curr, to_curr)
                    available = controller.balance_to_curr(to_curr)
                    print(f'From currency: {from_curr}, To currency: {to_curr}, RATE {rate}, AVAILABLE {available}')
                except CurrencyTypeError as m:
                    print(m.message)
            case '2':
                try:
                    from_curr = (input('Enter from currency: ').upper())
                    to_curr = (input('Enter to currency: ').upper())
                    amount = (Decimal(input('Enter amount: ')))
                    result = controller.exchange(from_curr, to_curr, amount)
                    print(to_curr, result[0], 'RATE', result[1])
                except CurrencyTypeError as m:
                    print(m.message)
                except InvalidBalanceError as m:
                    print(m.message)
            case '3':
                print('SERVICE STOPPED')
                break


if __name__ == '__main__':
    c = Controller()
    main(c)
