import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='agAARYA@3075',
        database='art_commission_db'
    )
    return connection
