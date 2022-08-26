import matplotlib.pyplot as plt
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask import render_template, Response, json, make_response
import os

from utils.util import *

FILE_ABS_PATH = os.path.dirname(__file__)
DATA_DIR = os.path.join(FILE_ABS_PATH, 'data')

app = Flask(__name__)
CORS(app)


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    main()
