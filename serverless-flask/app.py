from flask import Flask, request, jsonify
import re
import os
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def regex_matcher():
    req_data = request.get_json()
    jsonify(req_data)
