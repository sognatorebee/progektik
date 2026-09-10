import hashlib
from flask import Flask, render_template, request, jsonify
import mysql.connector


app = Flask(__name__)  

@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json()
    cnx = mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123")
    
    name = req['name']
    login = req['email']
    password = request.json['password']
    password_hash=hashlib.sha256(password.encode()).hexdigest()
    date = (name, login, password)
    cur = cnx.cursor()
    try:
        rows = cur.execute('INSERT INTO users (`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', (name, login, password_hash))
    except:
        return{'result':False}
    cnx.commit()
    cnx.close()

    return{'result':True,'id': cur.lastrowid}

@app.route('/user_avtorization', methods=['POST'])
def user_avtorization():
    req = request.get_json()
    cnx = connect()
    login = req['email']
    password = req['password']
    date = ( login, password)
    cur = cnx.cursor()
    try:
        rows = cur.execute('SELECT * FROM  users WHERE email=%s AND password=%s', date )
    except:
        return{'result':False}
    cnx.commit()
    cnx.close()

    return{'result':True,'user': cur.fetchall}

# # Fetch one result
# row = cur.fetchone()
# print("Current date is: {0}".format(row[0]))

# # Close connection
# cnx.close()

@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/login")
def login():
    return render_template('login.html')
app.run(port=8000)
