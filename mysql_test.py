import pymysql


class Sql:
    def __init__(self, host='localhost', port=3306, user='root'):
        self.host = host
        self.port = port
        self.user = user

    def __enter__(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user)
        self.cur = self.conn.cursor()
        print('db connection started!')
        return self.conn, self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.cur.close()
            self.conn.close()
            print('db connection closed!')


with Sql('10.7.12.65', 21771) as (conn, cur):
    db = 'mysql'
    table = 'COOK_HING'

    sql_use_db_mysql = f'use {db};'
    sql_create_table = f'''CREATE TABLE {table}(
        FIRST_NAME  CHAR(20) NOT NULL,
        LAST_NAME  CHAR(20),
        AGE INT,
        SEX CHAR(1),
        INCOME FLOAT);
        '''
    try:
        cur.execute(sql_use_db_mysql)
        cur.execute(sql_create_table)
    except pymysql.err.InternalError:
        print('Oops, some shit happened.')
