import json

from bs4 import BeautifulSoup

mUrl = ""
mData = {}


def __init__(self, url, data):
    # self.mUrl = url
    # self.mData = data
    self.mUrl = "www.knougths.com"
    self.mData = {
        "parent": '<div id = "parent-div" class="li-has-thumb__content"></div>',
        "heading": '<a href="https://www.kdnuggets.com/2023/08/whose-responsibility-get-generative-ai-right.html");"> <b>Whose Responsibility Is It To Get Generative AI Right? </b> </a>',
        "content": '<p>The limitless possibilities of the technology that transcends boundaries.</p>'
    }


mUrl = "www.axunijfnk.com"
mData = {
    "parent": '<div id = "parent-div" class="li-has-thumb__content"></div>',
    "heading": '<a href="https://www.kdnuggets.com/2023/08/whose-responsibility-get-generative-ai-right.html");"> <b>Whose Responsibility Is It To Get Generative AI Right? </b> </a>',
    "content": '<p>The limitless possibilities of the technology that transcends boundaries.</p>',
    "img": '<img id = "scrap-img" src="abcd.jpg" class="kk">'
}

mSchemaDict = {}
mSchemaDict[mUrl] = {}
for key in mData.keys():
    soup = BeautifulSoup(mData[key], 'html.parser')
    outerTag = soup.find()
    if outerTag.has_attr('class'):
        mSchemaDict[mUrl][key] = {
            "type": outerTag.name,
            "atr": {
                "id" : outerTag.get('id'),
                "class": outerTag.get('class')[0]
            }
        }
    else:
        mSchemaDict[mUrl][key] = {
            "type": outerTag.name,
            "atr": {
                "class": ""
            }
        }

f = open('schema.json')
data = json.load(f)
data[mUrl] = mSchemaDict[mUrl]
print(data)
with open("schema.json", "w") as file:
    json.dump(data, file)
# mSchemaDict[mUrl] = {
#     "parent" : {
#         "type" : outerTag.name,
#         "atr" : {
#             "class" : outerTag.get('class')[0]
#         }
#     },
# };
