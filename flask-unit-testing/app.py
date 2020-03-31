from flask import Flask, render_template
from flask_restful import Api, Resource
from string import Template

list_of_numbers = list(range(5)) # 0 1 2 3 4
total = sum(list_of_numbers)

# Create a Flask instance and pass that instance to the API
app = Flask(__name__)
api = Api(app)

# add class inherits the Resource class to specify Route associated with it.
class Addition(Resource):
    def div(a,b):
        return a/b

    # HTTP GET method (REST)
    def get(self):
        return {"total": total}

class say_hello(Resource):
    # HTTP GET method (REST)
    def get(self):
        return 'Hello World!'.upper()

# Various URL Routing addresses go here
@app.route("/")
def home():
    return "This is the home page!"

# Main function starts here
def main():
    global app, api

    # populate api with URLs to resources
    api.add_resource(say_hello, "/hello")
    api.add_resource(Addition, "/total")

    # allows us to see changes reflected without restarting the program
    app.run(debug=True)

# Without executing the main within a conditional expression it will break the detection of unit tests
if __name__ == '__main__':
    main()
