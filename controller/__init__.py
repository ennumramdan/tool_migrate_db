from ConfigParser import ConfigParser
from library.qbuilder import QBuilder
import MySQLdb
import logging

__author__ = 'ennumramdan'


class Controller:
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)
        self.pool_main = PersistentDB(
            MySQLdb, host=self.config.get('database_server', 'dbhost'),
            user=self.config.get('database_server', 'dbuser'),
            passwd=self.config.get('database_server', 'dbpwd'),
            db=self.config.get('database_server', 'dbname'), charset='utf8')
        self.pool_local = PersistentDB(
            MySQLdb, host=self.config.get('database_local', 'dbhost'),
            user=self.config.get('database_local', 'dbuser'),
            passwd=self.config.get('database_local', 'dbpwd'),
            db=self.config.get('database_local', 'dbname'), charset='utf8')
        self.query_builder = QBuilder()

        self.logger = logging.getLogger('db')
        handler = logging.FileHandler('/var/log/db.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.WARNING)


class PersistentDB:
    def __init__(self, creator, *args, **kwargs):
        from DBUtils.PersistentDB import PersistentDB
        self.pool = PersistentDB(creator, *args, **kwargs)
        self._creator = creator
        self._args, self._kwargs = args, kwargs

    def connection(self):
        connection = self.pool.connection()
        return connection
