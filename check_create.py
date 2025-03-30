import mysql.connector
def func_check_create():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
  )
  mycursor = mydb.cursor()

  mycursor.execute("SELE")