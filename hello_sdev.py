'''
Created on Apr 26, 2022

@author: gherwane
'''
from datetime import date
import logging
from flask import Flask, render_template
from flask import request, session, flash
from passlib.hash import sha256_crypt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(username)s:%(password)s')
file_handler = logging.FileHandler('logerror.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.secret_key = 'w&nuvOphebraSwig-x9N'
@app.route('/')
def index():
    '''index page function'''
    return render_template('index.html' , date = date.today())
@app.route('/about')
def about():
    '''about page function'''
    return render_template('about.html', date = date.today())
@app.route('/services')
def services():
    ''' services function'''
    return render_template('services.html', date = date.today())
@app.route("/login", methods=['GET', 'POST'])
def login():
    '''login page with screening for correct authentication'''
    if not session.get('logged_in'):
        if request.method == "POST":
            password = request.form['password']
            for line in open("CommonPassword.txt","r", encoding="utf8").readlines():
                creds = line.split(",")
                hashpass = creds[2]
                hashpass = hashpass.rstrip('\n')
                if (password != creds[0]) and (sha256_crypt.verify(password, hashpass)):
                    session['logged_in'] = True
                    flash("Successful logging!")
                    return render_template("login.html", date = date.today())
                return None
        else:
            flash("You must enter a more complex password!")
        return  render_template("login.html", date = date.today())
    return None
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''registration page'''
    if request.method == "POST":
        req = request.form
        username= req.get("username")
        email = request.form['email']
        password = request.form['password']
        if (any(x.isupper() for x in password) and any(x.islower() for x in password)and any(x.isdigit() for x in password) and len(password) >= 12):
            hash_pass = sha256_crypt.hash(password)
            file = open("userinfo.txt","a",encoding="utf8")
            file.write(username)
            file.write(",")
            file.write(email)
            file.write(",")
            file.write(hash_pass)
            file.write("\n")
            file.close()
        for line in open("userinfo.txt","r",encoding="utf8").readlines():
            creds = line.split(",")
            current_username = creds[0]
            current_email = creds[1]
            if (current_username == username) or (current_email == email):
                flash("This username and/or email already exist, try to login!")
            return render_template("login.html")
    return render_template("register.html")
@app.route('/passwordreset')
def passwordreset():
    '''password update page function'''
    if request.method == "POST":
        with open('CommonPassword.txt') as f:
            lines = f.readlines()
        for line in lines :
            if line == request.form['password']:
                flash("Your password is easily to guess, please use a different one!")
            return render_template("passwordreset.html", date = date.today())
    return render_template('passwordreset.html' , date = date.today())
@app.route('/logout')
def logout():
    '''Exit screen'''
    return render_template("logout.html", date = date.today())
if __name__ == "__main__":
    app.run(debug = True)
