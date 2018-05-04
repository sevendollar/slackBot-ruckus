#-*- coding: utf-8 -*-
import pymysql

def InsertData(wifi,newwifi):
    try:
        conn = pymysql.connect(host='localhost', user='USER', password='PASSWORD', port=3306, db='DB', charset="utf8")
        cur = conn.cursor()
        COLstr = ''  # 列的字段
        ROWstr = ''  # 行字段

        ColumnStyle = ' CHAR(20)'

	sql_looping_list = ["mac", "team_name", "team_user", "customer"]
        for key in sql_looping_list:
            COLstr = COLstr + ' ' + key + ColumnStyle + ','
            ROWstr = (ROWstr + '"%s"' + ',') % (newwifi.get(key))

            #判斷該列表是否存在，存在將執行try，不存執行except(新建表)，再insert資料
        try:
            cur.execute("SELECT * FROM  %s" % (wifi))
            cur.execute("INSERT INTO %s VALUES (%s)" % (wifi, ROWstr[:-1]))

        except pymysql.Error as e:
            cur.execute("CREATE TABLE %s (%s)" % (newwifi, COLstr[:-1]))
            cur.execute("INSERT INTO %s VALUES (%s)" % (newwifi, ROWstr[:-1]))
        conn.commit()
        cur.close()
        conn.close()

    except pymysql.Error as e:
        print
        "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
    newwifi = { "team_user": "Bob", "team_name": "IT","mac": "11:22:33:44:55:66","customer": "Tom"}
    InsertData('wifi', newwifi)
