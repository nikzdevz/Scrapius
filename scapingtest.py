import requests
from bs4 import BeautifulSoup
import json
import threading
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="scrapiusdb"
)
db_cursor = db_connection.cursor(buffered=True)


# print(db_connection)

# ======================================================================================================================

def scrap_handler(url, m_attrs):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    print(type(soup.findAll(m_attrs["parent"]["type"], m_attrs["parent"]["atr"])))
    for eachItem in reversed(soup.findAll(m_attrs["parent"]["type"], m_attrs["parent"]["atr"])):
        m_values = {};
        for keys in m_attrs:
            if keys != 'parent':
                m_values[keys] = eachItem.find(m_attrs[keys]["type"]).text
        query = "Select * from scrapeddata where Site=(%s) AND user='aa' AND title=(%s) Limit 1"
        db_cursor.execute(query, (url,m_values['heading']))
        myresult = db_cursor.fetchall()
        print(m_values['heading'])
        if len(myresult) == 0:
            query = "Insert into scrapeddata (Site, user, data, title) values (%s, 'aa', %s, %s)"
            db_cursor.execute(query,(url,str(m_values),m_values['heading']))
            db_connection.commit()




#
# READING JSON FILE - SCHEMA
#
with open('userbase/test/schema.json', 'r') as file:
    json_data = file.read()

mSiteList = json.loads(json_data)

for site in mSiteList.keys():
    threading.Thread(target=scrap_handler, args=(site, mSiteList[site])).start()
