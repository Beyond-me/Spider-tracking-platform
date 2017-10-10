# coding=utf-8
import MySQLdb
import os

dbname = 'spidermanage'

connect = MySQLdb.connect(
    user="root",
    passwd="mysql",
    host="127.0.0.1",
    db=dbname,
    charset="utf8",
    port=3306
)

os.system("mysqldump -uroot -pmysql %s > smsql.sql"%dbname)

connect.close()