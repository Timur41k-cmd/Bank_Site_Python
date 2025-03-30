import mysql.connector
def check_balance(user_data):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
  )
  mycursor = mydb.cursor()

  mycursor.execute("select check_name,amount,currency from checks inner join user on user.id = checks.user_id where user.id = %s")