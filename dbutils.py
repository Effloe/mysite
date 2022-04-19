import os
import sqlite3

BASEDIR = os.path.dirname(os.path.abspath(__file__))
SQLITEDB = os.path.join(BASEDIR, 'detect.db')

class DBUtils:
    def __init__(self):
        self.name = SQLITEDB

    def get_con(self):
        try:
            self.conn = sqlite3.connect(self.name)
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Error! :{}".format(e))
        return self.conn, self.cur

    def close_db(self, conn, cur):
        try:
            cur.close()
            conn.close()
        except Exception as e:
            print("Error! :{}".format(e))

    def query(self, sql, *args):
        conn, cursor = self.get_con()
        print(sql)
        cursor.execute(sql, *args)
        res = cursor.fetchall()
        self.close_db(conn, cursor)
        return res

    def execute(self, sql):
        conn, cursor = self.get_con()
        try:
            print(sql)
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print("Error! :{}".format(e))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
