'''
This is a http server, as the program API endpoint

'''
from flask import Flask, render_template, request, Response, jsonify
import driver           # the dirver.py file


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



@app.route('/')
def index():

    return 'Hello World'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

