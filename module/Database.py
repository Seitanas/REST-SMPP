import mysql.connector as mariadb
from module import Config

"""Class for SQL queries"""

class QueryDB(object):

    def __init__(self):

        cfg = Config.ReadConfig()
        mysql_host = cfg.config.get('mysql', 'host')
        mysql_user = cfg.config.get('mysql', 'user')
        mysql_pass = cfg.config.get('mysql', 'password')
        mysql_db = cfg.config.get('mysql', 'db')
        self.conn = mariadb.connect(host=mysql_host, port='3306', user=mysql_user, passwd=mysql_pass, db=mysql_db)
        self.cursor = self.conn.cursor()

    def execute(self, query_string):
        self.cursor.execute(query_string)
        result = self.cursor.fetchall()
        return result

    def commit(self, query_string):
        self.cursor.execute(query_string)
        self.conn.commit()

    def close(self):
        self.conn.close()
