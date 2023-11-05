import json
from types import NoneType

import mysql
import mysql.connector
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, session

import siteSubmission
import testingtool
import queueHandler
from flask_session import Session

app = Flask(__name__)

onceStart = True

@app.route('/testTool')
def testTool():
    return render_template('testTool.html')


# Edit Below
@app.route('/testing', methods=['POST'])
def testing():
    if request.method == 'POST':
        paramKey = request.form.keys()
        sData = {}
        for key in paramKey:
            if key == 'url':
                sData["url"] = request.form[key]
            elif request.form[key] != "":
                soup = BeautifulSoup(request.form[key], 'html.parser')
                outerTag = soup.find()
                sData[key] = {
                    "type": outerTag.name,
                    "atr": {
                        "id": outerTag.get('id'),
                        "class": outerTag.get('class')[0] if outerTag.get('class') is not None else ""
                    }
                }
                # if not attrValidator(request.form[key]):
                #     return f'{request.form[key]} do not contains id or class attribute.'
                # else:
        testScrap = testingtool.TestMyScraping(sData)
        return f'{testScrap.getReturnValue()}'
    return ""


# {
#     url : {
#         "parent" : {
#             "type" : outerTag,
#             "atr" : {
#                 "id" : outerTag.get('id'),
#                 "class" : outerTag.get('class')
#             }
#         },
#         "heading" : {
#             ....
#         }
#     }
# }
#
# {
#     "url" : url,
#     "parent" : {
#         "type" : outerTag,
#         "atr" : {
#             "id" : outerTag.get('id'),
#             "class" : outerTag.get('class')
#         }
#     },
#     "heading" : {
#         ....
#     }
# }


# Edit above


@app.route('/blog/<parameter_name>')
def blog(parameter_name):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="scrapiusdb"
    )
    param = parameter_name
    db_cursor = db_connection.cursor(buffered=True)
    query = "select Site,data from scrapeddata where user=(%s)"
    db_cursor.execute(query, (param,))
    myresult = db_cursor.fetchall()
    if len(myresult) == 0:
        return f'No Data Found';
    else:
        return f'My Result => {myresult}'


@app.route('/userRegister', methods=['GET', 'POST'])
def userRegister():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        username = request.form['username']
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scrapiusdb"
        )
        db_cursor = db_connection.cursor(buffered=True)
        # if db_connection.is_connected():
        #     print('Connected to MySQL database')
        query = "Select * from userbase where email=(%s) OR username=(%s) Limit 1"
        db_cursor.execute(query, (email, username))
        myresult = db_cursor.fetchall()

        if len(myresult) == 0:
            query = "Insert into userbase (name, email, password, username) values (%s, %s, %s, %s)"
            db_cursor.execute(query, ('aa', email, password, username))
            db_connection.commit()
            session['loggedInEmail'] = email;
            return redirect('/dashboard')
        else:
            param = {"isUniqueUser": "True"}
            for item in myresult:
                if item[1] == email:
                    param["isUniqueUser"] = 'False'
            return redirect(url_for('/', messages=json.dumps(param)))


@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        # print("Login => " + email + "    " + password)

        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scrapiusdb"
        )
        db_cursor = db_connection.cursor(buffered=True)
        query = "select email,password from userbase"
        db_cursor.execute(query)
        myresult = db_cursor.fetchall()
        isVerified = 0
        for item in myresult:
            if item[0] == email:
                if item[1] == password:
                    isVerified = 2
                else:
                    isVerified = 1
        if isVerified == 2:
            session['loggedInEmail'] = email
            return redirect('/dashboard')
        elif isVerified == 1:
            # param = [str(isVerified),str(isVerified),str(isVerified)]
            return render_template('index.html', regData='Incorrect password')
        else:
            return render_template('index.html', regData='Email not found')


@app.route('/manageSite', methods=['GET', 'POST'])
def manageSite():
    # print(session['loggedInEmail'])
    # json_file = "sitedata.json"
    # existing_data = []
    # try:
    #     with open(json_file) as file:
    #         existing_data = json.load(file)
    # except FileNotFoundError:
    #     pass
    return render_template('manage.html')


def attrValidator(element1):
    soup = BeautifulSoup(element1, 'html.parser')
    outerTag = soup.find()
    if outerTag.has_attr('class'):
        if len(outerTag.get('class')) > 0:
            return True
    elif outerTag.has_attr('id'):
        if len(outerTag.get('id')) > 0:
            return True
    else:
        return False


@app.route('/addSite', methods=['GET', 'POST'])
def addSite():
    userEmail = session['loggedInEmail']
    mUrl = request.form['url']
    msg = ""
    paramKey = request.form.keys()
    if 'parent' in paramKey and not attrValidator(request.form['parent']):
        msg = "Parent do not contains id or class attribute."
    elif 'heading' in paramKey and not attrValidator(request.form['heading']):
        msg = "Heading do not contains id or class attribute."
    elif 'link' in paramKey and not attrValidator(request.form['link']):
        msg = "Link do not contains id or class attribute."
    elif 'img' in paramKey and not attrValidator(request.form['img']):
        msg = "Image do not contains id or class attribute."
    if msg == "":
        sData = {
            "parent": request.form['parent'],
            "heading": request.form['heading'],
            "link": request.form['link']
        }
        addSiteObj = siteSubmission.addSiteSubmission(userEmail, mUrl, sData)
        return redirect('/dashboard')
    else:
        return render_template('manage.html', regData=msg)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('Dashboard.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        json_file = "sitedata.json"
        new_data = {
            "url": request.form['siteBox'],
            "schema": request.form['schemaBox']
        }
        existing_data = []
        try:
            with open(json_file) as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass
        # Append the new dictionary to the existing data
        existing_data.append(new_data)
        # Write the updated data back to the JSON file
        with open(json_file, "w") as file:
            json.dump(existing_data, file)
    return redirect('/manageSite')


@app.route('/', methods=['GET', 'POST'])
def index():
    # existing_data = []
    # json_file = "sitedata.json"
    # try:
    #     with open(json_file) as file:
    #         existing_data = json.load(file)
    # except FileNotFoundError:
    #     pass
    # return render_template('index.html', regData=existing_data)
    if session.get('loggedInEmail') is not None:
        print(session['loggedInEmail'])
    return render_template('index.html')


if __name__ == "__main__":
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run()
