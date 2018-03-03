from controller import Controller
from datetime import datetime

import MySQLdb
import time

__author__ = 'ennumramdan'


class Utility(Controller):
    def __init__(self, config_file):
        Controller.__init__(self, config_file)

    def server_to_client(self, table_name, keyid, last_day):
        conn = self.pool_main.connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        conn_migration = self.pool_local.connection()
        cursor_migration = conn_migration.cursor(MySQLdb.cursors.DictCursor)
        db_name = self.config.get('database_server', 'dbname')

        try:
            self.migrate_db(cursor, conn_migration, cursor_migration, db_name, table_name, keyid, last_day)
        except Exception, e:
            print "{} [ERROR]: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), e)
        finally:
            cursor_migration.close()
            conn_migration.close()
            cursor.close()
            conn.close()

    def client_to_server(self, table_name, keyid, last_day):
        conn = self.pool_local.connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        conn_migration = self.pool_main.connection()
        cursor_migration = conn_migration.cursor(MySQLdb.cursors.DictCursor)
        db_name = self.config.get('database_local', 'dbname')

        try:
            self.migrate_db(cursor, conn_migration, cursor_migration, db_name, table_name, keyid, last_day)
        except Exception, e:
            print "{} [ERROR]: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), e)
            self.logger.error(e)
        finally:
            cursor_migration.close()
            conn_migration.close()
            cursor.close()
            conn.close()

    def migrate_db(self, cursor, conn_migration, cursor_migration, db_name, table_name, keyid, last_day):
        try:
            cursor.execute("""SHOW TABLES""")
            results = cursor.fetchall()
            tables = list()
            for result in results:
                tables.append(result['Tables_in_{}'.format(db_name)])

            for table in tables:
                if table_name == table or table_name == "all":
                    start = 0
                    rows = 500
                    cursor.execute("SHOW KEYS FROM {} WHERE Key_name = 'PRIMARY'".format(table))
                    key = cursor.fetchone()['Column_name']
                    while True:
                        if keyid is not None:
                            where = 'WHERE `{0}` > {1} '.format(key, keyid)
                        else:
                            where = 'WHERE `{0}` > 0 '.format(key)

                        if last_day:
                            cursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS "
                                           "WHERE TABLE_SCHEMA='{}' AND "
                                           "TABLE_NAME='{}' AND "
                                           "COLUMN_NAME='updated_at'".format(db_name, table))
                            if cursor.fetchone():
                                where += ' AND updated_at >= NOW() - INTERVAL {} DAY'.format(last_day)

                        sql = "SELECT * FROM {0} {1} ORDER BY {2} ASC LIMIT {3}, {4}". \
                            format(table, where, key, start, rows)
                        cursor.execute(sql)
                        datas = cursor.fetchall()

                        if len(datas) < 1:
                            break
                        else:
                            try:
                                for data in datas:
                                    cursor_migration.execute("SET NAMES utf8mb4;")
                                    cursor_migration.execute("SET CHARACTER SET utf8mb4;")
                                    cursor_migration.execute("SET character_set_connection=utf8mb4;")

                                    insertsql = self.query_builder.insert_update(data, key, table, key)
                                    cursor_migration.execute(insertsql)
                                    conn_migration.commit()

                                    print "{} [INFO]: Id {} IN TABLE {} INSERTED".format(
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[key], table)
                                    self.logger.info("{} [INFO]: Id {} IN TABLE {} INSERTED".format(
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[key], table))
                                    keyid = data[key]
                            except Exception, e:
                                print e
                                raise
        except Exception, e:
            raise
