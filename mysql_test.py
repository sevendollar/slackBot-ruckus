import pymysql
import csv


class Sql:
    def __init__(self, host='localhost', port=3306, user='root', password=None, db=None):
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
        print('db connection started!')
        return self.conn, self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.cur.close()
            self.conn.close()
            print('db connection closed!')


db = 'ruckus'
table = 'wifi'
port = 32772
pw = 'jef'
host = '10.5.1.65'
fields = ('TeamName', 'TeamUser', 'CustermerName', 'ID', 'MAC')

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
# sql_insert = f'''insert into {db}.{table}({', '.join(fields)}) values{values};'''

if __name__ == '__main__':
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
                with open('Book1.csv', 'r') as csv_file:
                    for value in csv.reader(csv_file):  # loop through the whole csv.
                        # insert records only if it's not duplicated in the DB.
                        if not cur.execute(f'select MAC from {db}.{table} where MAC = \'{value[-1]}\';'):
                            cur.execute(f'''insert into {db}.{table}({', '.join(fields)}) values{tuple(value)};''')
                        else:
                            print(f'{value[-1]} existed!')
                    conn.commit()
        except pymysql.err.InternalError as E:
            print(E)
