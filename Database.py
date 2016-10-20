import os
import json
import psycopg2


class database():
    port = None
    vcap = None
    port = None
    vcap = None
    jdbc_uri = None
    database_name = None
    username = None
    password_str = None
    db_host = None
    db_port = None
    connected = False
    conn = None
    cur = None


    def __init__(self, jdbc_uri=None, database_name=None, username=None, password_str=None, db_host=None, db_port=None):
        self.restart_conn(jdbc_uri, database_name, username, password_str, db_host, db_port)

    def restart_conn(self, jdbc_uri=None, database_name=None, username=None, password_str=None, db_host=None, db_port=None):
        services = os.getenv("VCAP_SERVICES")

        if services is not None:
            vcap = json.loads(services)

        if vcap is not None:
            postgres = vcap['postgres'][0]['credentials']
            if postgres is not None:
                self.jdbc_uri = postgres['jdbc_uri']
                self.database_name = postgres['database']
                self.username = postgres['username']
                self.password_str = postgres['password']
                self.db_host = postgres['host']
                self.db_port = postgres['port']

        if jdbc_uri is not None: self.jdbc_uri = jdbc_uri
        if database_name is not None: self.database_name = database_name
        if username is not None: self.username = username
        if password_str is not None: self.password_str = password_str
        if db_host is not None: self.db_host = db_host
        if db_port is not None: self.db_port = db_port

        try:
            self.conn = psycopg2.connect(database=self.database_name, user=self.username, password=self.password_str,
                                         host=self.db_host, port=self.db_port)
            self.connected = True
            self.cur = self.conn.cursor()
        except:
            self.connected = False

    def execute_query_no_fetch(self, query):
        if self.cur is not None:
            print query
            try:
                self.cur.execute(query)
                self.conn.commit()
            except:
                self.restart_conn()

    def execute_query(self, query):
        rows = None
        if self.cur is not None:
            print query
            try:
                self.cur.execute(query)
                self.conn.commit()
                rows = self.cur.fetchall()
            except:
                self.restart_conn()
        return rows

    def get_json_from_query(self, query):
        response = json.dumps(self.execute_query(query))
        return response