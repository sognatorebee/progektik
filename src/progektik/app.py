
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
    date = (name, login, password_hash)
    cur = cnx.cursor()
    try:
        rows = cur.execute('INSERT INTO users (`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
    except Exception as e:            
        print(f"Ошибка БД: {e}")   
        return {'result': False}
    new_id = cur.lastrowid
    cnx.commit()
    cnx.close()

    return {'result': True, 'id': new_id}
    

    #try:
        #rows = cur.execute('INSERT INTO users (`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
    #except:
        #return{'result':False}
    #cnx.commit()
    #cnx.close()

    #return{'result':True,'id': cur.lastrowid}

@app.route('/user_avtorization', methods=['POST'])
def user_avtorization():
    req = request.get_json()
    cnx = mysql.connector.connect()
    login = req['email']
    password=req['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    date = (login, password_hash)
    cur = cnx.cursor(buffered= True)
    try:
        rows = cur.execute('SELECT * FROM users WHERE email=%s AND password_hash=%s', date)
    except Exception as e: 
        print(f"Ошибка авторизации: {e}")
        return {'result': False}

    user_data = cur.fetchall()
    cnx.commit()
    cnx.close()       

    if not user_data:    
        return {'result': False}

    return {'result': True, 'user': user_data[0]} 
# # Fetch one result
# row = cur.fetchone()
# print("Current date is: {0}".format(row[0]))

# # Close connection
# cnx.close()
####
@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/login")
def login():
    return render_template('login.html')
app.run(port=8000)
