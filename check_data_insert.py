import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot",
  database="bank"
)
mycursor = mydb.cursor()

mycursor.execute("SELE")