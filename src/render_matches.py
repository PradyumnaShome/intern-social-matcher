import json
import flask
from flask import render_template
import requests
import logging
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True
logging.basicConfig(level=logging.DEBUG)

S3_API_URL = os.getenv("S3_API_URL")


def get_intern_groups():
    response = requests.get(S3_API_URL)

    content = response.json()

    logging.debug(content)

    return content


@app.route("/", methods=["GET"])
def home():
    matches = get_intern_groups()
    logging.debug(f"Current Directory: {os.getcwd()}")

    return render_template("matches.html", list_matches=matches)


if __name__ == "__main__":
    app.run()
