from check_create import func_check_create
from check_balance import check_balance
from transfer import transfer_func
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
)
mycursor = mydb.cursor()

def check_create(user_id,currency,check_name):
    sql = ("select check_num,amount,currency,check_name from checks"
           " inner join user on user.id = checks.user_id"
           " where user.id = %s")
    adr = (f"{user_id}",)
    mycursor.execute(sql, adr)
    response = mycursor.fetchall()
    response = len(response)
    sql = ("insert into checks (currency,user_id,check_num,check_name,amount) values (%s,%s,%s,%s,0)")
    adr = (currency,user_id,response,check_name)
    mycursor.execute(sql, adr)
    mydb.commit()
def check_delete_func(user_id,check_num):
    sql = ("select check_num,amount,currency,check_name,checks.id from checks"
           " inner join user on user.id = checks.user_id"
           " where user.id = %s")
    adr = (f"{user_id}",)
    mycursor.execute(sql, adr)
    response = mycursor.fetchall()

    print(response)
    print(response[int(check_num)])
    response = response[int(check_num)]
    print(response[1])

    if response[1] == 0:
        sql = ("DELETE FROM checks WHERE id = %s")
        adr = (response[4],)
        mycursor.execute(sql,adr)
        mydb.commit()



def profile(id):
    sql = "SELECT * FROM user WHERE id = %s"
    adr = (f"{id}",)
    mycursor.execute(sql, adr)
    response = mycursor.fetchall()

    return response
def checks_load(id):
    mydb.close()
    mydb.connect()

    mycursor = mydb.cursor()

    sql = ("select check_num,amount,currency,check_name from checks"
                   " inner join user on user.id = checks.user_id"
                   " where user.id = %s")
    adr = (f"{id}",)
    mycursor.execute(sql, adr)
    response = mycursor.fetchall()

    return response

def database_refresh():
    mydb.close()
    mydb.connect()




def acc(user_data):
  while True:
    mydb.close()
    mydb.connect()
    print(f"hi, {user_data[0][1]}")
    checks_load(user_data)
    print("Select operation:")
    print("1 = profile\n"
          "2 = transfer\n"
          "3 = check create\n"
          "4 = check delete")
    answ = int(input())
    if answ == 0:
      break
    choises = [lambda func_select: profile(user_data),
               lambda func_select: transfer_func(user_data),
               lambda func_select: check_create(user_data),
               lambda func_select: check_delete(user_data)]
    choises[answ-1](user_data)

