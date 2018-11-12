#/usr/bin/python3

from flask import Flask
from postgresql_connection_min import SQL, ENUM_CursorType, ENUM_FETCHAMOUNTTYPE

app = Flask(__name__, static_folder='./assets')

sql = SQL()
sql.connect(host='127.0.0.1', user='postgres', password='postgres', dbName='google_codein') 
sql.createSchema('microservices')
sql.createTable('users', [
    "id SERIAL",
    "username TEXT",
    "password TEXT",
    "PRIMARY KEY(id)"
])
sql.insert('users', {
    'name': 'testUser',
    'password' : "myPassword123"
})
sql.setDebugMode(True)
sql.setCursorType(ENUM_CursorType.REALDICTCURSOR)
sql.setFetchType(ENUM_FETCHAMOUNTTYPE.ALL)

from views import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)