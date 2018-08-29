# -*- coding: utf-8 -*-
import pymysql


class Sql:
    def __init__(self, host='localhost', port= 3306, user='royce', password=None, db=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password or None
        self.db = db or None

    def __enter__(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.password,
                                    db=self.db,
                                    use_unicode=True,
                                    charset='utf8',)
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.cur.close()
            self.conn.close()


db = 'ruckus'
table = 'wifi'
port = 3306
pw = 'Royce898O4142'
host = '10.5.1.113'
fields = ('team_name', 'team_user', 'customer_name', 'customer_id', 'mac')
new_key = []
new_value = []


sql_use_db = f'use {db};'
sql_create_db = f'create database {db};'
sql_is_db_exist = f'show databases like \'{db}\';'
sql_is_table_exist = f'show tables like \'{table}\';'
sql_create_table = f'''create table {db}.{table}(
                        {fields[0]} CHAR(20),  
                        {fields[1]} CHAR(20),
                        {fields[2]} CHAR(20),
                        {fields[3]} CHAR(20),
                        {fields[-1]} CHAR(20) PRIMARY KEY);'''

def InsertData(new_words):
    new_value = []
    new_key = []
    with Sql(host=host, port=port, password=pw) as (conn, cur):
        try:
            if not cur.execute(sql_is_db_exist):  # create DB only if it doesn't exist.
                cur.execute(sql_create_db)
                cur.execute(sql_use_db)
                if not cur.execute(sql_is_table_exist):  # create TABLE only if it doesn't exist.
                    cur.execute(sql_create_table)
            else:
                cur.execute(sql_use_db)
                if not cur.execute(sql_is_table_exist):  # create TABLE only if it doesn't exist.
                    cur.execute(sql_create_table)
            if cur.execute(sql_is_db_exist) and cur.execute(sql_is_table_exist):
                for key, value in new_words.items():
                    new_key.append(key)
                    new_value.append(value)
                    V = ','.join("'" + i + "'" for i in new_value)
                    K = ', '.join(new_key)
                if not cur.execute(f'select mac from {db}.{table} where mac = \'{new_value[-1]}\';'):
                    cur.execute(f'''INSERT INTO {db}.{table}({K})  VALUES ({V});''')
                    conn.commit()
                    if cur.execute(f'select mac from {db}.{table} where mac = \'{new_value[-1]}\';'):
                        return True
                    else:
                        return False
                else:
                    return False or None
            else:
                return False or None

        except pymysql.err.InternalError as E:
            print(E)