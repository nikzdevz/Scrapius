import json
import os
import xml.etree.ElementTree as ET

import mysql
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/userRegister',methods=['GET','POST'] )
def userRegister():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        username = request.form['username']
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="ShanuYadav",
            database="scrapiusdb"
        )
        db_cursor = db_connection.cursor(buffered=True)
        # if db_connection.is_connected():
        #     print('Connected to MySQL database')
        query = "Select * from userbase where email=(%s) OR username=(%s) Limit 1"
        db_cursor.execute(query, (email, username))
        myresult = db_cursor.fetchall()

        if len(myresult) == 0 :
            query = "Insert into userbase (name, email, password, username) values (%s, %s, %s, %s)"
            db_cursor.execute(query, ('aa', email,password,username))
            db_connection.commit()
            return redirect('/dashshri')
        else :
            param = {"isUniqueUser": "True"}
            for item in myresult :
                if item[1] == email:
                    param["isUniqueUser"] = 'False'
            return redirect(url_for('/', messages=json.dumps(param)))

@app.route('/userLogin', methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        print("Login => " + email + "    " + password)

        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="ShanuYadav",
            database="scrapiusdb"
        )
        db_cursor = db_connection.cursor(buffered=True)
        query = "select email,password from userbase"
        db_cursor.execute(query)
        myresult = db_cursor.fetchall()
        isverified = False
        for item in myresult:
            if (item[0] == email) and (item[1] == password):
                isverified = True
        if isverified:
            return redirect('/dashshri')
        else:
            return redirect('/')



@app.route('/manageSite', methods=['GET', 'POST'])
def manageSite():
    json_file = "sitedata.json"
    existing_data = []
    try:
        with open(json_file) as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        pass
    return render_template('manage.html', regData=existing_data)





@app.route('/dashshri', methods=['GET', 'POST'])
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
    existing_data = []
    json_file = "sitedata.json"
    try:
        with open(json_file) as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        pass
    return render_template('index.html', regData=existing_data)


if __name__ == "__main__":
    app.run(debug=True)
