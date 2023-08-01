import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/manageSite', methods=['GET', 'POST'])
def manageSite():
    json_file = "sitedata.json"
    existing_data = []
    try:
        with open(json_file) as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        pass
    return render_template('manageSite.html', regData=existing_data)

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
