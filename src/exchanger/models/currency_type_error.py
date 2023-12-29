class CurrencyTypeError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


if __name__ == "__main__":
    pass