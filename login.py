import mysql.connector
from main import acc
from user_create import user_create_func

def f_login(id,password):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootroot",
        database="bank"
    )
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE email = %s"
    adr = (f"{id}",)
    mycursor.execute(sql,adr)

    response = mycursor.fetchall()
    try:
        if response[0][5] == password:
            return response
    except:
        return False

