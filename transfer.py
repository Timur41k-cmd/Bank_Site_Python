import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot",
  database="bank"
)
mycursor = mydb.cursor()




def email_transfer_func(email,sum,check_id,user_id):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
  )
  mycursor = mydb.cursor()
  sql = "SELECT id,name,surname,phone_number FROM user WHERE email = %s"
  adr = (email,)
  mycursor.execute(sql, adr)
  myresult = mycursor.fetchall()
  if len(myresult) != 0:
    sql = "SELECT checks.amount,checks.id FROM checks INNER JOIN user ON user.id = checks.user_id WHERE user.id = %s AND checks.check_num = %s"
    adr = (user_id, int(check_id))
    mycursor.execute(sql, adr)
    myresult_user = mycursor.fetchall()

    sql = "UPDATE checks SET amount = %s WHERE id = %s"
    adr = (myresult_user[0][0] - sum, myresult_user[0][1])

    mycursor.execute(sql, adr)
    mydb.commit()

    sql = "SELECT checks.id,checks.amount FROM checks INNER JOIN user ON user.id = checks.user_id WHERE user.id = %s AND checks.check_num = 0"
    adr = (myresult[0][0],)
    mycursor.execute(sql, adr)
    myresult_user = mycursor.fetchall()
    amount = int(myresult_user[0][1]+sum)

    sql = "UPDATE checks SET amount = %s WHERE id = %s"
    adr = (amount,myresult_user[0][0])
    mycursor.execute(sql, adr)
    mydb.commit()
    mydb.close()
    mydb.connect()
    return True
  else:
    return False



#email_transfer_func("gleb@gmail.com",20,0)

def phone_transfer_func(phone,sum,check_id,user_id):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
  )
  mycursor = mydb.cursor()
  sql = "SELECT id,name,surname,email FROM user WHERE phone_number = %s"
  adr = (phone,)
  mycursor.execute(sql, adr)
  myresult = mycursor.fetchall()
  if len(myresult) != 0:
    sql = "SELECT checks.amount,checks.id FROM checks INNER JOIN user ON user.id = checks.user_id WHERE user.id = %s AND checks.check_num = %s"
    adr = (user_id, int(check_id))
    mycursor.execute(sql, adr)
    myresult_user = mycursor.fetchall()

    sql = "UPDATE checks SET amount = %s WHERE id = %s"
    adr = (myresult_user[0][0] - sum, myresult_user[0][1])

    mycursor.execute(sql, adr)
    mydb.commit()

    sql = "SELECT checks.id,checks.amount FROM checks INNER JOIN user ON user.id = checks.user_id WHERE user.id = %s AND checks.check_num = 0"
    adr = (myresult[0][0],)
    mycursor.execute(sql, adr)
    myresult_user = mycursor.fetchall()
    amount = int(myresult_user[0][1]+sum)

    sql = "UPDATE checks SET amount = %s WHERE id = %s"
    adr = (amount,myresult_user[0][0])
    mycursor.execute(sql, adr)
    mydb.commit()
    mydb.close()
    mydb.connect()
    return True
  else:
    return False


def check_transfer(check_to,sum,check_from,user_id):
  sql = ("select check_num,amount,currency,check_name,checks.id from checks"
         " inner join user on user.id = checks.user_id"
         " where user.id = %s")
  adr = (f"{user_id}",)
  mycursor.execute(sql, adr)
  response = mycursor.fetchall()
  print(check_to,check_from)
  check_from_tr = response[int(check_from)]
  check_to_tr = response[int(check_to)]
  print(check_from_tr,check_to_tr)
  if check_from_tr[2] == check_to_tr[2]:

    if check_from_tr[1] - sum >= 0:
      #from check
      sql = ("UPDATE checks SET amount = %s WHERE id = %s")
      adr = (check_from_tr[1]-sum,check_from_tr[4])
      mycursor.execute(sql, adr)
      mydb.commit()
      mydb.close()
      mydb.connect()
      #to check
      sql = ("UPDATE checks SET amount = %s WHERE id = %s")
      adr = (check_to_tr[1]+sum,check_to_tr[4])
      mycursor.execute(sql, adr)
      mydb.commit()
    else:
      print("not enough")
  else:
    print("Error, different currency")




def transfer_func(user_data):
  print(user_data)
  print("Select transfer method:\n1 - email transfer\n2 - phone number transfer\n3 - other check transfer")
  answ = int(input())
  choises = [lambda func_select: email_transfer_func(user_data), lambda func_select: phone_transfer(user_data), lambda func_select: check_transfer(user_data)]
  choises[answ - 1](user_data)
