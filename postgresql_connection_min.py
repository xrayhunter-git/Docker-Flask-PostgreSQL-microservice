#/usr/bin/python3

import psycopg2 as I_sql
from psycopg2.extras import RealDictCursor

# Enums
class ENUM_CursorType():
    DEFAULT = 0
    REALDICTCURSOR = 1

class ENUM_FETCHAMOUNTTYPE():
    NONE = 0
    ALL = 1
    ONE = 2
    MANY = 3

# SQL Base
class SQL:
    con = None
    host = ""
    username = ""
    password = ""
    databaseTarget = ""
    schemaTarget = ""
    debug = False
    CursorType = ENUM_CursorType.DEFAULT
    FetchType = ENUM_FETCHAMOUNTTYPE.ALL
    def __init__(self):
        pass
     
    def connect(self, host, user, password, dbName = ""):
        """
        Connects to a PostgreSQL service.

        Creates a Database, if necessary, then reconnect to that database.
        
            :param self: 
            :param host:str: 
            :param user:str: 
            :param password:str: 
            :param dbName="": 
        """   
        self.host = host
        self.username = user
        self.password = password

        if self.debug:
            print("Connecting to PostgreSQL")

        try:
            self.con = I_sql.connect('user=%s password=%s' % (self.username, self.password))

            if self.debug:
                print("Connected to PostgreSQL")

            self.con.set_isolation_level(I_sql.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            if dbName != "":
                self.useDatabase(dbName)
        except (Exception, I_sql.DatabaseError) as error:
                print("SQL Connection Error Occured >> ")
                print(error)
        return self.con

    def close(self):
        """
            Closes existing connection.
            :param self: 
        """   
        if self.con is not None:
            self.con.close()

            if self.debug:
                print("Disconnecting from PostgreSQL")

    def query(self, sql, parameters, table = "", ENUM_CursorType = ENUM_CursorType.DEFAULT, ENUM_FETCHAMOUNTTYPE = ENUM_FETCHAMOUNTTYPE.ALL, fetchAmount = 1):
        """
            Runs a Query Command to the connected Database.
                :param self: 
                :param sql:str: 
                :param parameters:list: 
                :param table="": 
                :param ENUM_CursorType=ENUM_CursorType.DEFAULT: 
                :param ENUM_FETCHAMOUNTTYPE=ENUM_FETCHAMOUNTTYPE.ALL: 
                :param fetchAmount=1: 
        """   
        if self.con is not None:
            if self.con.closed == 0:
                query = SQL_Query(self.con, self.debug)
                return query.execute(sql, parameters, table, self.CursorType, self.FetchType, fetchAmount)
            elif self.con.closed == 1:
                print("Failed to Execute: " + sql + "\nError: No SQL Connection.")
        return False

    def useDatabase(self, database):
        """
            Connects to a Database, if it exists, otherwise it will create the database.
            :param self: 
            :param database:str: 
        """   
        self.createDatabase(database)
        
        if self.debug:
            print("Connecting to PostgreSQL > Database > " + database)
        
        try:
            self.con = I_sql.connect('dbname=%s user=%s password=%s' % (database, self.username, self.password))
            
            if self.debug:
                print("Connected to PostgreSQL > Database > " + database)
            
            self.con.set_isolation_level(I_sql.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.databaseTarget = database
        except (Exception, I_sql.DatabaseError) as error:
                print("SQL Connection Error Occured >> ")
                print(error)
        return self.con

    def useSchema(self, schema):
        """
            Sets the target Schema.
            :param self: 
            :param schema:str: 
        """
        self.createSchema(schema)
        self.schemaTarget = schema
        return self.con

    def get(self, table, where):
        """
            Selects the data within the table it is targeting.
            :param self: 
            :param table:str: 
            :param where:list: 
        """   
        whereClasues = ' '.join(where)
        return self.query("SELECT * FROM {} {}", (((" WHERE " + whereClasues) if len(where) != 0 else "")), table)

    def deleteTableRow(self, table, where):
        """
            Deletes a Table Row from the Table.
            :param self: 
            :param table:str: 
            :param where:list: 
        """   
        whereClasues = ' AND '.join(where)
        return self.query("DELETE FROM {} {}", (((" WHERE " + whereClasues) if len(where) != 0 else "")), table)

    def deleteTable(self, table):
        """
            Deletes an entire table from a schema.
            :param self: 
            :param table:str: 
        """   
        return self.query("DROP TABLE IF EXISTS {}", (), table)

    def deleteSchema(self, schema):
        """
            Deletes an entire schema from a database.
            :param self: 
            :param schema:str: 
        """   
        if self.schemaTarget == schema:
            self.schemaTarget = ""
        return self.query("DROP SCHEMA IF EXISTS {}", (), schema)

    def deleteDatabase(self, database):
        """
            Deletes an entire database from the PostgreSQL service.
            :param self: 
            :param database:str: 
        """
        if self.databaseTarget == database:
            self.connect(self.host, self.username, self.password)
        return self.query("DROP DATABASE IF EXISTS {}", (), database)

    def insert(self, table, fields):
        """
            Inserts fields into a table.
            :param self: 
            :param table:str: 
            :param fields:dict: 
        """   
        field_keys = ', '.join(fields.keys())
        _fields = '\',\''.join(fields.values())
        return self.query("INSERT INTO {} ({}) VALUES ({})", (field_keys, _fields), table)

    def createTable(self, name, fields):
        """
            Creates a Table within a Schema.
            :param self: 
            :param name:str: 
            :param fields:list: 
        """   
        field_keys = ', '.join(fields)
        return self.query("CREATE TABLE IF NOT EXISTS {} ({})", (field_keys), name)

    def createSchema(self, name):
        """
            Creates a Schema within a Database.
            :param self: 
            :param name:str: 
        """   
        if self.databaseTarget is not "":
            if not self.checkIfSchemaExists(name):
                return self.query("CREATE SCHEMA {}", (), name)
        return False

    def createDatabase(self, name):
        """
            Creates a Database within the PostgreSQL service.
            :param self: 
            :param name:str: 
        """   
        if not self.checkIfDatabaseExists(name):
            return self.query("CREATE DATABASE {}", (), name)
            
        return False

    def update(self, table, where, fields):
        """
            Updates rows within a table, when given a where clause with the fields given.
            :param self: 
            :param table:str: 
            :param where:list: 
            :param fields:dict: 
        """   
        whereClasues = ' AND '.join(where)
        _resolvedFields = []
        for key in fields.keys():
            _resolvedFields.append(key + " = '" + fields[key] + "'")
        
        _resolvedFieldsToStr = ', '.join(_resolvedFields)
        
        return self.query("UPDATE {} SET {} {}", (_resolvedFieldsToStr, ((" WHERE " + whereClasues) if len(where) != 0 else "")), table)

    def checkIfDatabaseExists(self, name):
        """
            Checks if a Database Exists within the PostgreSQL service.
            :param self: 
            :param name:str: 
        """   
        result = self.query(
            """
            SELECT EXISTS(
                SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower({})
            );
            """, (name))
        value = str(result[0]).replace("(", "").replace(")", "").replace(",", "")
        return True if 'true' in value.lower() else False 
    
    def checkIfSchemaExists(self, name):
        """
            Checks if a Schema Exists within the targeted Database.
            :param self: 
            :param name:str: 
        """   
        result = self.query(
            """
            SELECT EXISTS(
                SELECT schema_name FROM information_schema.schemata WHERE schema_name = {}
            );
            """, (name))
        value = str(result[0]).replace("(", "").replace(")", "").replace(",", "")
        return True if 'true' in value.lower() else False 
    
    def setDebugMode(self, debugMode):
        """
            Sets the Debugger Mode.
            (Enabled) will display all the SQL Commands within the console.
            :param self: 
            :param debugMode: 
        """   
        self.debug = debugMode
    
    def setCursorType(self, cursorType):
        self.CursorType = cursorType

    def setFetchType(self, fetchType):
        self.FetchType = fetchType

    def __targetTable(self, table):
        """
            [PRIVATE]
            Constructs a string to target the Schema and Tables.
            :param self: 
            :param table:str: 
        """   
        return (self.schemaTarget + "." + table) if self.schemaTarget != "" else table

# Query Instance
class SQL_Query:
    con = None
    debug = False
    noFetch = ['DELETE', 'CREATE', 'UPDATE', 'INSERT']
    affectedRows = 0
    lastRowID = None
    arraySize = 1
    errors = []
    results = False
    def __init__(self, con, debug = False):
        self.con = con
        self.debug = debug

    def execute(self, sql, parameters, fields = [], table = "", ENUM_CursorType = ENUM_CursorType.DEFAULT, ENUM_FETCHAMOUNTTYPE = ENUM_FETCHAMOUNTTYPE.ALL, fetchAmount = 1):
        """
            Executes a Query when given.
            :param self: 
            :param sql:str: 
            :param parameters:tuple: 
            :param fields=[]: 
            :param table="": 
            :param ENUM_CursorType=ENUM_CursorType.DEFAULT: 
            :param ENUM_FETCHAMOUNTTYPE=ENUM_FETCHAMOUNTTYPE.ALL: 
            :param fetchAmount=1: 
        """   
        self.errors.clear()
        results = False
        cur = None

        if self.debug:
            print(sql)

        if self.con is not None:
            try:
                if ENUM_CursorType == ENUM_CursorType.REALDICTCURSOR:
                    self.con.cursor_factory = RealDictCursor
                    if self.debug:
                        print("SQL Connection has been set to RealDictCursor! [The Connection would have to be terminated to be returned.]")

                cur = self.con.cursor()
                
                cur.execute(sql, parameters)

                hasNoFetch = False
                for word in self.noFetch:
                    if word in sql:
                        hasNoFetch = True
                        break

                if not hasNoFetch:
                    if ENUM_FETCHAMOUNTTYPE == ENUM_FETCHAMOUNTTYPE.ALL:
                        results = cur.fetchall()     
                    elif ENUM_FETCHAMOUNTTYPE == ENUM_FETCHAMOUNTTYPE.MANY:
                        results = cur.fetchmany(fetchAmount)     
                    elif ENUM_FETCHAMOUNTTYPE == ENUM_FETCHAMOUNTTYPE.ONE:
                        results = cur.fetchone()
                
                self.affectedRows = cur.rowcount()
                self.arraySize = cur.arraySize()
                self.lastRowID = cur.lastrowid()
            except (Exception, I_sql.DatabaseError) as error:
                if self.debug:
                    print("SQL Error Occured >> ")
                    print(error)
                self.errors.append(error)
            finally:
                if cur is not None:
                    cur.close()
        return self

    def commit(self, sql, parameters, fields = [], table = "", ENUM_CursorType = ENUM_CursorType.DEFAULT, ENUM_FETCHAMOUNTTYPE = ENUM_FETCHAMOUNTTYPE.ALL, fetchAmount = 1):
        """
            Similiar to the Execute function, just adds pending transaction to the database.
            :param self: 
            :param sql:str: 
            :param parameters:tuple: 
            :param fields=[]: 
            :param table="": 
            :param ENUM_CursorType=ENUM_CursorType.DEFAULT: 
            :param ENUM_FETCHAMOUNTTYPE=ENUM_FETCHAMOUNTTYPE.ALL: 
            :param fetchAmount=1: 
        """
        self.errors.clear()
        results = False
        cur = None

        if self.debug:
            print(sql)

        if self.con is not None:
            try:
                if ENUM_CursorType == ENUM_CursorType.REALDICTCURSOR:
                    self.con.cursor_factory = RealDictCursor
                    if self.debug:
                        print("SQL Connection has been set to RealDictCursor! [The Connection would have to be terminated to be returned.]")

                cur = self.con.cursor()

                cur.execute(sql, parameters)

                hasNoFetch = False
                for word in self.noFetch:
                    if word in sql:
                        hasNoFetch = True
                        break

                if not hasNoFetch:
                    if ENUM_FETCHAMOUNTTYPE == ENUM_FETCHAMOUNTTYPE.ALL:
                        results = cur.fetchall()     
                    elif ENUM_FETCHAMOUNTTYPE == ENUM_FETCHAMOUNTTYPE.MANY:
                        results = cur.fetchmany(fetchAmount)     
                    elif ENUM_FETCHAMOUNTTYPE == ENUM_FETCHAMOUNTTYPE.ONE:
                        results = cur.fetchone()
                
                self.con.commit()

                self.affectedRows = cur.rowcount()
                self.arraySize = cur.arraySize()
                self.lastRowID = cur.lastrowid()
            except (Exception, I_sql.DatabaseError) as error:
                if self.debug:
                    print("SQL Error Occured >> ")
                    print(error)
                self.errors.append(error)
            finally:
                if cur is not None:
                    cur.close()
        return self

    def hasErrors(self):
        return (self.errors.count > 0)

    def getErrors(self):
        return self.errors

    def getAffectedRowsCount(self):
        """
            Gets the amount of rows that were affected by the last Execution.
            :param self: 
        """   
        return self.affectedRows
    
    def getArraySize(self):
        """
            Gets the array size from the last Execution.
            :param self: 
        """  
        return self.arraySize
    
    def getLastRowID(self):
        """
            Gets the ID of the last Row in the last Execution.
            :param self: 
        """   
        return self.lastRowID

    def getResults(self):
        return self.results
    
