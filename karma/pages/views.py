from flask import render_template, redirect, url_for, session, jsonify, Blueprint
from karma.pages.forms import RegisterForm, LoginForm
from karma import db, auth
import bcrypt


pages = Blueprint('pages', __name__)



# hashing password to store in DB
def create_bcrypt_hash(password):
    password_bytes = password.encode()
    salt = bcrypt.gensalt(14)
    password_hash_bytes = bcrypt.hashpw(password_bytes, salt)
    password_hash_str = password_hash_bytes.decode()

    return password_hash_str


@pages.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted_password = create_bcrypt_hash(form.password.data)
        user = {
            'username' : form.username.data,
            'email' : form.email.data,
            'password' : encrypted_password,
            'confirmpassword' : form.confirmpassword.data
        }

        users = auth.create_user_with_email_and_password(user['email'], user['password'])
        db.child("users").child(users['localId']).set(user) 
        return redirect(url_for('pages.login'))

    return render_template('register.html', form = form)



@pages.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        login = auth.sign_in_with_email_and_password(email, password)
        user = db.child("users").child(login['localId']).get().val()
        session['username'] = user['username']
        session['email'] = email
        session['login'] = True
        session['id'] = login['localId']
        if( user['address'] != None):
            session['address'] = user['address']['name']+","+ user['address']['address']+","+ user['address']['city'] + ',' +user['address']['state']+","+str(user['address']['pincode'])
        return redirect(url_for('blog.index'))

    return render_template('login.html', form=form)

@pages.route('/logout')
def logout():
    session.clear()
    session['login'] = False
    return redirect(url_for('blog.index'))

@pages.route('/about')
def about():
    return render_template('about.html')