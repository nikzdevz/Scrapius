import json
import os
from datetime import datetime

from bs4 import BeautifulSoup
def getAttrsDict(attributes):
    mAttrDict = {}
    for attribute, value in attributes.items():
        mAttrDict[attribute] = value
    return mAttrDict


class addSiteSubmission:

    def __init__(self, username, mUrl, mData):
        mSchemaDict = {mUrl: {}}
        # Generating Schema
        for key in mData.keys():
            soup = BeautifulSoup(mData[key], 'html.parser')
            # print("MDATA KEY => " + key)
            outerTag = soup.find()
            mSchemaDict[mUrl][key] = {
                "type": outerTag.name,
                "atr": {
                    "id": outerTag.get('id') if outerTag.get('id') else "",
                    "class": outerTag.get('class')[0] if outerTag.get('class') else ""
                }
            }
        # Appending Schema to schema.json of user
        file_name = 'userbase/' + username
        if not os.path.exists(file_name):
            os.makedirs(file_name)
        file_name = file_name + "/schema.json"
        if not os.path.exists(file_name):
            # Create the file if it doesn't exist
            with open(file_name, 'w') as file:
                file.write("{}")
        f = open(file_name)
        data = json.load(f)
        data[mUrl] = mSchemaDict[mUrl]
        with open(file_name, "w") as file:
            json.dump(data, file)

        cr_filename = 'userbase/' + username + "/created.json"
        if not os.path.exists(cr_filename):
            # Create the file if it doesn't exist
            with open(cr_filename, 'w') as file:
                file.write("{}")
        f1 = open(cr_filename)
        cr_data = json.load(f1)
        cr_data[mUrl] = str(datetime.now().strftime('%d %b'))
        with open(cr_filename, "w") as file:
            json.dump(cr_data, file)
        # Appending Schema to queue.json
        with open('queue.json', 'r') as file:
            dataqueue = json.load(file)
        mSchemaDict[mUrl]['url'] = mUrl
        mSchemaDict[mUrl]['username'] = username
        dataqueue.append(mSchemaDict[mUrl])
        with open('queue.json', 'w') as file:
            json.dump(dataqueue, file, indent=4)
