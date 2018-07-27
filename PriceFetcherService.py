from flask import Flask
from PriceFetcher import on_query


app = Flask(__name__)
un = "dgnajera"
key = "cs.utep.edu"


@app.route("/query/<username>/<password>/<path:url>")
def handle_query(username, password, url):
    if username == un and password == key:
        return on_query(url)[1:]
    else:
        return "Incorrect credentials"


@app.route("/")
def index():
    return "Welcome"


if __name__ == "__main__":
    app.run()
