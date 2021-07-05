"""import pymysql.cursors
import os

connection = pymysql.connect(host='localhost',
                            port=3306,
                            database=os.getenv('MYSQL_DATABASE'),
                            user=os.getenv('MYSQL_USER_NAME'),
                            password=os.getenv('MYSQL_ROOT_PASSWORD'),
                            cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        for line in open('events_table.sql'):
            cursor.execute(line)


    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()"""


import MySQLdb
db = MySQLdb.connect('localhost',os.getenv('MYSQL_USER_NAME'),os.getenv('MYSQL_ROOT_PASSWORD'),os.getenv('MYSQL_DATABASE'))
cursor = db.cursor()
for line in open("events_table.sql"):
    cursor.execute(line)
db.close()