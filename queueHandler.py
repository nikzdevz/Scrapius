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
import json
import threading
import time

import mysql
import requests
from bs4 import BeautifulSoup
import json
import threading
import mysql.connector


class scrap_handler:
    def __init__(self, data):
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
            r = requests.get(data['url'])
            soup = BeautifulSoup(r.content, 'html.parser')
            m_attrs =  {**data};
            url = data['url']
            username = data['username']
            m_attrs.pop("username")
            m_attrs.pop("url")
            for eachItem in reversed(soup.findAll(m_attrs["parent"]["type"], m_attrs["parent"]["atr"])):
                m_values = {};
                for keys in m_attrs:
                    if keys != 'parent':
                        m_values[keys] = eachItem.find(m_attrs[keys]["type"]).text
                query = "Select * from scrapeddata where Site=(%s) AND user='aa' AND title=(%s) Limit 1"
                db_cursor.execute(query, (url, m_values['heading']))
                myresult = db_cursor.fetchall()
                print(m_values['heading'])
                if len(myresult) == 0:
                    query = "Insert into scrapeddata (Site, user, data, title) values (%s, 'aa', %s, %s)"
                    db_cursor.execute(query, (url, str(m_values), m_values['heading']))
                    db_connection.commit()
            time.sleep(30)


# Create a thread that runs the function repeatedly
def call_my_function():
    while True:
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
thread = threading.Thread(target=call_my_function)
thread.daemon = True  # Set the thread as a daemon so it won't block the program from exiting
thread.start()