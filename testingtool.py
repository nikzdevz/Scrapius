import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class TestMyScraping:
    returnValue = ""

    def __init__(self, data):
        output = {}
        r = requests.get(data['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        item = 1
        for eachItem in reversed(soup.findAll(data["parent"]["type"], data["parent"]["atr"])):
            m_values = {};
            for key in data.keys():
                if key == 'link' :
                    mUrl = eachItem.find(data[key]["type"], data[key]["atr"]).get('href') if eachItem.find(
                        data[key]["type"], data[key]["atr"]) else ""
                    if mUrl != "" and not mUrl.startswith("http"):
                        parsed_url = urlparse(data['url'])
                        mUrl = str(parsed_url.scheme + "://" + parsed_url.netloc) + mUrl
                    m_values[key] = mUrl
                elif  key == 'img':
                    chkUrl = str(eachItem.find(data[key]["type"], data[key]["atr"]).get('src'))
                    # print(str(eachItem.find(data[key]["type"], data[key]["atr"])))
                    if not chkUrl.startswith('http'):
                        chkUrl = eachItem.find(data[key]["type"], data[key]["atr"]).get('data-src')
                    if not str(chkUrl).startswith('http') :
                        chkUrl = eachItem.find(data[key]["type"], data[key]["atr"]).get('data-lazy-src')
                    m_values[key] = chkUrl
                elif key != 'parent' and key != 'url':
                    m_values[key] = eachItem.find(data[key]["type"]).text.strip()
            output[f'item{item}'] = m_values
            item = item + 1
        # print(json.dumps(output,indent=4))
        self.returnValue = output

    def getReturnValue(self):
        return self.returnValue