import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
)
mycursor = mydb.cursor()

email = input()
amount = int(input())

print("Select check:")

#

sql = "SELECT checks.id,checks.amount,user.id,checks.currency,checks.check_num FROM checks INNER JOIN user ON user.id = checks.user_id WHERE user.email = %s"
adr = (email,)
mycursor.execute(sql,adr)
myresult = mycursor.fetchall()

amount = myresult[0][1] + amount
for x in range(len(myresult)):
    print(f"check num {x} - {myresult[x][4]}, {myresult[x][1]} {myresult[x][3]}")

print("Select where to add:")
num = int(input())



sql = "UPDATE checks SET amount = %s WHERE id = %s"
adr = (amount,myresult[num][0],)
mycursor.execute(sql, adr)

mydb.commit()



