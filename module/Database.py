import mysql.connector as mariadb
from module import Config
import logging

"""Class for SQL queries"""


class QueryDB(object):

    def __init__(self):

        self.logger = logging.getLogger('REST-SMPP')
        cfg = Config.ReadConfig()
        mysql_host = cfg.config.get('mysql', 'host')
        mysql_user = cfg.config.get('mysql', 'user')
        mysql_pass = cfg.config.get('mysql', 'password')
        mysql_db = cfg.config.get('mysql', 'db')
        mysql_port = cfg.config.get('mysql', 'port')
        try:
            self.conn = mariadb.connect(host=mysql_host,
                                        port=mysql_port,
                                        user=mysql_user,
                                        passwd=mysql_pass,
                                        db=mysql_db)
            self.cursor = self.conn.cursor()
        except Exception as ex:
            self.logger.error("Database error occurred: %s", ex)
            return None

    def execute(self, query_string):
        try:
            self.cursor.execute(query_string)
            result = self.cursor.fetchall()
            return result
        except Exception as ex:
            self.logger.error("Database error occurred: %s", ex)
            return None

    def commit(self, query_string):
        try:
            self.cursor.execute(query_string)
            self.conn.commit()
        except Exception as ex:
            self.logger.error("Database error occurred: %s", ex)
            return None

    def close(self):
        self.conn.close()
