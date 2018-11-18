#/usr/bin/python3

from flask import Flask, request, make_response
from postgresql_connection_min import SQL, ENUM_CursorType, ENUM_FETCHAMOUNTTYPE

app = Flask(__name__, static_folder='./assets')

sql = SQL()
sql.setDebugMode(True)
sql.setCursorType(ENUM_CursorType.REALDICTCURSOR)
sql.setFetchType(ENUM_FETCHAMOUNTTYPE.ALL)

@app.route('/execute', methods=['POST'])
def execute():
    json = request.get_json()
    query = json['query']
    args = json.get('data', {})
    sql.connect(host='127.0.0.1', user='postgres', password='postgres', dbName='google_codein') 
    q = sql.query(query, args, "", ENUM_CursorType.REALDICTCURSOR, ENUM_FETCHAMOUNTTYPE.ALL)

    if q is None or q.getResults() is False or q.hasErrors():
        resp = make_response('{"status":"fail"}')
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp
    
    resp = make_response(
        json.dumps({
            'status':'ok',
            'results': q.getResults()
        })
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)