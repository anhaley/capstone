"""
This is an HTTP server, as the program API endpoint
"""
from flask import Flask, render_template, request, Response, jsonify
import driver  # the driver.py file
import os

app = Flask(__name__)


# /list?table=???
@app.route("/list", methods=["GET"])
def list_tables():
    table_name = request.args.get('table', '')
    table_info_obj = driver.get_table(table_name)

    response = jsonify(table_info_obj)

    return response


@app.route("/load", methods=["GET"])
def load_data():
    response = ''

    filename = 'files/Lists.xlsx'
    driver.process_file(filename)

    response_obj = {'status': 'OK'}

    response = jsonify(response_obj)
    return response


@app.route("/file", methods=["POST"])
def upload_file():
    """
    POST <file> will trigger the Python code to ingest a spreadsheet into the database.
    Returns:
        The JSON representation of the server response.
    """
    response = ''
    if request.method == 'POST':
        # right now, this is a dummy method, just illustrating that the response is returned
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '' or file.filename is None:
                return response
            else:
                driver.process_file(file)
                response_obj = {'status': 'OK'}
                response = jsonify(response_obj)
    return response


@app.route('/')
def index():
    return 'Hello World\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)