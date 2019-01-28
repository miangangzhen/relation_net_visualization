from flask import Flask
from flask import request, send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    with open("../resource/visualization.html", "r", encoding="utf-8") as f:
        string = f.read()
    return string


@app.route("/relation.json", methods=["GET"])
def relation():
    with open("relation.json", "r", encoding="utf-8") as f:
        string = f.read()
    return string


@app.route("/point0.png", methods=["GET"])
def point():
    return send_from_directory("../resource", "point.png")


@app.route("/point1.png", methods=["GET"])
def point1():
    return send_from_directory("../resource", "point1.png")


@app.route("/d3.v3.min.js", methods=["GET"])
def d3():
    return send_from_directory("../resource", "d3.v3.min.js")


if __name__ == '__main__':
    app.run(host="0.0.0.0")