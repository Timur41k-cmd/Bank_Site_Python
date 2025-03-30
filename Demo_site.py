from flask import Flask, redirect, url_for, render_template, request, session
from main import check_create
from transfer import email_transfer_func
from transfer import phone_transfer_func
from transfer import check_transfer
from main import profile
from login import f_login
import mysql.connector
from main import database_refresh
from main import check_delete_func
from user_create import user_create_func

def checks_load(id):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootroot",
        database="bank"
    )


    mycursor = mydb.cursor()

    sql = ("select check_num,amount,currency,check_name from checks"
                   " inner join user on user.id = checks.user_id"
                   " where user.id = %s")
    adr = (f"{id}",)
    mycursor.execute(sql, adr)
    response = mycursor.fetchall()
    mydb.close()
    return response

app = Flask(__name__)

app.secret_key = "hello"

@app.route("/reg",methods=["POST","GET"])
def reg():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        adress = request.form['adress']
        phone_number = request.form['phone_number']
        surname = request.form['surname']
        user_create_func(email,password, name, surname, phone_number, adress)
        return render_template("log.html")
    else:
        return render_template("reg.html")



@app.route("/",methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form['nm']
        password = request.form['pass']
        if f_login(user,password) != False:
            res = f_login(user, password)
            session["user"] = res[0][0]
            return redirect(url_for('user'))
        else:
            return render_template("log.html")
    else:
        return render_template("log.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        print(user)
        id = checks_load(user)
        user_data_temp=profile(int(user))
        return render_template('profile.html',content=id,user_data=user_data_temp[0])
    else:
        return redirect(url_for("login"))


@app.route("/create")
def create_check_func():
    if "user" in session:
        user = session["user"]
        id = checks_load(user)
        return render_template('create_check.html',content=id)
    else:
        return redirect(url_for("login"))


@app.route("/check/<id>", methods=["POST","GET"])
def check_ul(id):
    if request.method == "POST":
        print(1)
        if request.form["delete"] == "delete":
            user = session["user"]
            print(1)
            check_delete_func(int(user),int(id))
            checks = checks_load(session["user"])
            id = checks_load(user)
            user_data_temp = profile(int(user))
            return render_template('profile.html',content=id,user_data=user_data_temp[0])
    if "user" in session:
        database_refresh()
        id = int(id)
        checks = checks_load(session["user"])

        return render_template('check.html', content=checks,check_id = id)
    else:
        return redirect(url_for("login"))



@app.route("/check/<id>/email", methods=["POST","GET"])
def email_transfer(id):
    if "user" in session:
        id = int(id)
        database_refresh()
        checks = checks_load(session["user"])
        if request.method == "POST":
            try:
                user_email = request.form['email']
                sum_to_transfer = int(request.form['sum'])
                if (len(user_email) != 0) or (len(user_email) != 0):
                    if checks[id][1] - sum_to_transfer >= 0:
                        res = email_transfer_func(user_email, sum_to_transfer, id, session["user"])
                        print(res)
                        if res != False:
                            checks = checks_load(session["user"])
                            return render_template('email.html', content=checks, check_id=id, answer="Succesfuly")
                        else:
                            return render_template('email.html', content=checks, check_id=id, answer="Error, user havent finded")
                    else:
                        return render_template('email.html', content=checks, check_id=id, answer="Error, Not enough money")
            except:
                return render_template('email.html', content=checks, check_id=id, answer="Error, Bullshit data have inserted")
    else:
        return redirect(url_for("login"))
    return render_template('email.html', content=checks,check_id = id)

@app.route("/check/<id>/phone", methods=["POST","GET"])
def phone_transfer(id):
    if "user" in session:
        id = int(id)
        database_refresh()
        checks = checks_load(session["user"])
        if request.method == "POST":
            try:
                user_email = request.form['phone']
                sum_to_transfer = int(request.form['sum'])
                if (len(user_email) != 0) or (len(user_email) != 0):
                    if checks[id][1] - sum_to_transfer >= 0:
                        res = phone_transfer_func(user_email, sum_to_transfer, id, session["user"])
                        print(res)
                        if res != False:
                            checks = checks_load(session["user"])
                            return render_template('phone.html', content=checks, check_id=id, answer="Succesfuly")
                        else:
                            return render_template('phone.html', content=checks, check_id=id, answer="Error, user havent finded")
                    else:
                        return render_template('phone.html', content=checks, check_id=id, answer="Error, Not enough money")
            except:
                return render_template('phone.html', content=checks, check_id=id, answer="Error, Bullshit data have inserted")
    else:
        return redirect(url_for("login"))
    return render_template('phone.html', content=checks,check_id = id)


@app.route("/check/<id>/check_tr", methods=["POST","GET"])
def other_check(id):
    if "user" in session:
        id = int(id)
        database_refresh()
        checks = checks_load(session["user"])
        if request.method == "POST":
            try:
                check_select = request.form.get('check_select')

                sum_to_transfer = int(request.form['sum'])
                if (len(check_select) != 0) or (len(check_select) != 0):

                    if checks[id][1] - sum_to_transfer >= 0:
                        print(check_select,sum_to_transfer)
                        res = check_transfer(check_select, sum_to_transfer, id, session["user"])


                        if res != False:

                            checks = checks_load(session["user"])
                            return render_template('other_check.html', content=checks, check_id=id, answer="Succesfuly")
                        else:
                            return render_template('other_check.html', content=checks, check_id=id, answer="Error, user havent finded")
                    else:
                        return render_template('other_check.html', content=checks, check_id=id, answer="Error, Not enough money")
            except:
                return render_template('other_check.html', content=checks, check_id=id, answer="Error, Bullshit data have inserted")
    else:
        return redirect(url_for("login"))
    return render_template('other_check.html', content=checks,check_id = id)





@app.route("/create", methods=["POST","GET"])
def check_create_func():
    if "user" in session:
        if request.method == "POST":
            user = session["user"]
            id = checks_load(user)
            check_name_temp = request.form['check_name']
            currency = request.form.get('currency_select')
            check_create(int(user),currency,check_name_temp)
            user_data_temp = profile(int(user))
            id = checks_load(user)
            return render_template('profile.html', content=id, user_data=user_data_temp[0])
if __name__ == "__main__":
    app.run(debug=True)