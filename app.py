from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import random
import json

import model
import util

app = Flask(__name__)
Bootstrap(app)

from flask import request

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route("/subjects")
def list():
    subjects = model.getAll()
    if request_wants_json():
        return json.dumps(subjects)
    else:
        hack = []
        for key in subjects:
            hack.append({**{'subject': key}, **subjects[key]}) 
        return render_template('index.html', subjects=hack)

@app.route("/subjects/<subject>", methods=['DELETE'])
def remove(subject):
    return model.delete(subject)

@app.route("/subjects/<subject>", methods=['PUT'])
def update(subject):
    print(request);
    return model.update(subject, request.json)

@app.route("/momo", methods=['GET', 'POST'])
def momo():
    subject = request.json[0]['msys']['relay_message']['content']['subject']
    m = model.get(subject)
    if m:
        engage = m['engage_percent'] >= random.random()
        if engage:
            util.fakeEngagement(request.json[0]['msys']['relay_message']['content']['html'])
        model.incr(subject, m['engage_percent'] >= random.random())
    else:
        model.incr(subject, 0)
    return ''
