from app import app, sql
from flask import render_template, request
import json as json

@app.route('/', methods=['GET'])
def index():
    print(sql.get('users', ["name = 'testUser'"]))
    jsonInfo = json.JSONEncoder().encode({})

    return render_template('index.html', jsonInfo=jsonInfo)