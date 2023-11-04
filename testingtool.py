import json

import requests
from bs4 import BeautifulSoup


class TestMyScraping:

    def __init__(self, data):
        output = {}
        r = requests.get(data['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        item = 1
        for eachItem in reversed(soup.findAll(data["parent"]["type"], data["parent"]["atr"])):
            m_values = {};
            for key in data.keys():
                if key != 'parent' and key != 'url':
                    m_values[key] = eachItem.find(data[key]["type"]).text
            output[f'item{item}'] = m_values
            item = item+1
        print(json.dumps(output,indent=4))


data = {
    "url" : "https://economictimes.indiatimes.com/news/india",
    "parent": {
        "type": "div",
        "atr": {
            "id": None,
            "class": "eachStory"
        }
    },
    "heading": {
        "type": "a",
        "atr": {
            "class": ""
        }
    },
    "link": {
        "type": "a",
        "atr": {
            "class": ""
        }
    }
}
testMy = TestMyScraping(data)
