import json
import requests


class RateApiClient:

    def __init__(self):
        self.rate_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

    def get_courses(self):
        get_request = requests.get(self.rate_url)
        if get_request.status_code == 200:
            res = json.loads(get_request.content)
            return res
        return None
