import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="bank"
)
mycursor = mydb.cursor()
def user_create_func(email,password,name,surname,phone_number,adress):


    sql = ("SELECT email from user where email = %s")
    adr = (email,)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        sql = ("INSERT INTO user (name,surname,email,phone_number,password,adress) values(%s,%s,%s,%s,%s,%s)")
        adr = (name,surname,email,phone_number,password,adress)
        mycursor.execute(sql,adr)
        mydb.commit()

        sql = "SELECT id FROM user WHERE email = %s"
        adr = (email,)
        mycursor.execute(sql,adr)
        myresult = mycursor.fetchall()

        sql = ("INSERT INTO checks (user_id,amount,currency,check_num,check_name) VALUES (%s,%s,%s,%s,%s)")
        currency = "EUR"
        num = 0
        adr = (myresult[0][0], num,currency,num, "main")
        mycursor.execute(sql,adr)
        mydb.commit()
    else:
        print("Error, Email already exists")
