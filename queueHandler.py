# # import time
# #
# #
# import random
# import asyncio
# import time
#
#
# async def my_function():
#     print("Function called")
#     with open('hello.txt', 'w') as file:
#         # Write "Hello" to the file
#         num = random.random()
#         file.write("Hello" + str(num))
#
#
# async def print_active():
#     while True:
#         await my_function()  # Call the function
#         await asyncio.sleep(2)  # Wait for 2 seconds
#
# #
# # print_active()
import os
import time
from urllib.parse import urlparse

import mysql
import requests
from bs4 import BeautifulSoup
import json
import threading
import mysql.connector


class scrap_handler:
    def __init__(self, data):
        # print("Scrap Handler Data Item => " + str(data))
        mThread = threading.Thread(target=self.doScraping, args=([data]))
        mThread.daemon = True  # Set the thread as a daemon so it won't block the program from exiting
        mThread.start()

    def doScraping(self, data):
        # print(data)
        while True:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="scrapiusdb"
            )
            db_cursor = db_connection.cursor(buffered=True)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                # Add more headers if needed
            }
            r = requests.get(data['url'],headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            m_attrs = {**data};  # ** is used to duplicate complete variable
            url = data['url']
            username = data['username']
            m_attrs.pop("username")
            m_attrs.pop("url")
            print(url + "  =>   " + str(len(soup.findAll(m_attrs["parent"]["type"], m_attrs["parent"]["atr"]))))
            for eachItem in reversed(soup.findAll(m_attrs["parent"]["type"], m_attrs["parent"]["atr"])):
                m_values = {};
                for keys in m_attrs:
                    if keys == 'link':
                        mUrl = eachItem.find(m_attrs[keys]["type"], m_attrs[keys]["atr"]).get('href') if eachItem.find(
                            m_attrs[keys]["type"], m_attrs[keys]["atr"]) else ""
                        if mUrl != "" and not mUrl.startswith("http"):
                            parsed_url = urlparse(url)
                            mUrl = str(parsed_url.scheme + "://" + parsed_url.netloc) + mUrl
                        m_values[keys] = mUrl
                    elif keys == 'img':
                        m_values[keys] = eachItem.find(m_attrs[keys]["type"], m_attrs[keys]["atr"]).get('src')
                    elif keys != 'parent':
                        m_values[keys] = eachItem.find(m_attrs[keys]["type"], m_attrs[keys]["atr"]).text if (
                            eachItem.find(m_attrs[keys]["type"], m_attrs[keys]["atr"])) else ""
                if m_values['heading'] != "" :
                    query = "Select * from scrapeddata where Site=(%s) AND user=(%s) AND title=(%s) Limit 1"
                    db_cursor.execute(query, (url, data['username'], m_values['heading']))
                    myresult = db_cursor.fetchall()
                    if len(myresult) == 0:
                        try:
                            query = "Insert into scrapeddata (Site, user, data, title) values (%s, %s, %s, %s)"
                            db_cursor.execute(query,(url, data['username'], json.dumps(m_values, indent=4), m_values['heading']))
                            db_connection.commit()
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            print("username => " +data['username'])
                            print("heading => " + m_values['heading'])
            time.sleep(30)


def restart_scraping_services():
    userDir = os.listdir('userbase')
    with open('queue.json', 'r') as file:
        dataqueue = json.load(file)
    for user in userDir:
        with open('userbase/' + user + '/schema.json', 'r') as file:
            userSchema = json.load(file)
        for key in userSchema.keys():
            userSchema[key]['url'] = key
            userSchema[key]['username'] = user
            dataqueue.append(userSchema[key])
    with open('queue.json', 'w') as file:
        json.dump(dataqueue, file, indent=4)
    with open('configdata.json', 'r') as file:
        configdata = json.load(file)
    configdata["isRestarting"] = "false"
    with open('configdata.json', 'w') as file:
        json.dump(configdata, file, indent=4)
    print("Restarted All Services")


def queuehandlerStarted():
    print("Queue Handler Started")

# Create a thread that runs the function repeatedly
def queue_json_handler():
    while True:
        with open('configdata.json', 'r') as file:
            configdata = json.load(file)
        if configdata["isRestarting"] != "true":
            with open('queue.json', 'r') as file:
                dataqueue = json.load(file)
            for dataItem in dataqueue:
                scrap_handler(dataItem)
            # handleQueueRequest()
            dataqueue.clear()
            with open('queue.json', 'w') as file:
                json.dump(dataqueue, file, indent=4)
        time.sleep(2)


# Create and start the thread
thread = threading.Thread(target=queue_json_handler)
thread.daemon = True  # Set the thread as a daemon so it won't block the program from exiting
thread.start()

thread1 = threading.Thread(target=restart_scraping_services)
thread1.daemon = True
thread1.start()
