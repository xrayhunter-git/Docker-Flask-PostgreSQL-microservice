from app import app, sql
from flask import render_template, request
import json as json

@app.route('/', methods=['GET'])
def index():
    query = sql.query(request.args.get('query', ''), request.args.get('params', ''))
    print(query)
    jsonInfo = json.JSONEncoder().encode(query)

    return jsonInfo