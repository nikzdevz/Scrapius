import requests
from bs4 import BeautifulSoup


class TestMyScraping:

    def __init__(self, data):
        r = requests.get(data['url'])
        soup = BeautifulSoup(r.content, 'html.parser')