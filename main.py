from flask import Flask, render_template, request, Response, jsonify
import sqlalchemy
import os
import logging



app = Flask(__name__)

#password for the database instance is cap-password
#the instance name is myinstance
engine = sqlalchemy.create_engine('postgresql://postgres:cap-password@104.197.116.127/postgres')
 

@app.route("/list", methods=["GET"])
def index():
    results = []
    db = engine.connect()
    people = db.execute("SELECT * FROM capstone")
    for row in people:
        results.append({"First Name": row[1], "Last Name":row[2], "Company Name":row[3], "Address":row[4], "City":row[5], "County":row[6], "State":row[7], "Zip":row[8], "Phone1":row[9], "Phone2":row[10], "Email":row[11], "Web":row[12]})

    
    return jsonify(results)
        
@app.route("/addFile", methods=["POST"])
def add():
    f = request.files["file"]
    connection = engine.raw_connection()
    cur = connection.cursor()


    cur.execute("Truncate {} Cascade;".format('capstone'))
    cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format('capstone'), f)
    cur.execute("commit;")
    return "ok"




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
