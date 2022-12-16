from db_config import db_config
import mysql.connector

mydb = mysql.connector.connect(**db_config)
if mydb:
    print('connect database successfully')
else:
    print('failed db connection')