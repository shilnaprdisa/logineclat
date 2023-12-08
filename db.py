#database
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database ="eclatdatabase",
    password="",
)
if conn.is_connected():
    print("terhubung")
