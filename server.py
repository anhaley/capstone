'''
This is a http server, as the program API endpoint

'''
from flask import Flask, render_template, request, Response, jsonify
import driver           # the dirver.py file
import os

app = Flask(__name__)

# /list?table=???
@app.route("/list", methods=["GET"])
def list_tables():
    response = ''

    table_name = request.args.get('table', '')
    table_info_obj = driver.get_table(table_name)

    response = jsonify(table_info_obj)

    return response


@app.route("/load", methods=["GET"])
def load_data():
    response = ''

    filename = 'files/Lists.xlsx'
    driver.populate_file(filename)
    
    response_obj = {'status': 'OK'}
    
    response = jsonify(response_obj)
    return response

@app.route("/file", methods=["GET", "POST"])
def upload_file():
    response = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            return response
        file = request.files['file']
        if file.filename == '':
            return response
        if file:
            driver.populate_file(file)
            response_obj = {'status': 'OK'}
            response = jsonify(response_obj)
            return response
        else:
            return response


@app.route('/')
def index():

    return 'Hello World'


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=80, debug=True)

