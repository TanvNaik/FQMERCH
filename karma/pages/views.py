from re import U
from flask import render_template, redirect, url_for, session, request, jsonify, Blueprint
from karma.pages.forms import RegisterForm, LoginForm
import pyrebase
from karma import db, auth

pages = Blueprint('pages', __name__)

@pages.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = {
            'username' : form.username.data,
            'email' : form.email.data,
            'password' : form.password.data,
            'confirmpassword' : form.confirmpassword.data
        }

        name = db.child("users").child(user['username']).get().val()
        if name != None:
            return jsonify({"error":"User Already Exists"})
        users = auth.create_user_with_email_and_password(user['email'], user['password'])
        db.child("users").child(user['username']).set(user)
        return redirect(url_for('pages.login'))

    return render_template('register.html', form = form)

@pages.route('/login', methods=['POST','GET'])
def login():

    form = LoginForm()
    print("Before Validate")
    if form.validate_on_submit():
        print("Validate")
        email = form.email.data
        password = form.password.data
        print("before Auth")
        login = auth.sign_in_with_email_and_password(email, password)
        user = db.child("users").child(email).get().val()
        session['email'] = email
        session['login'] = True
        form.email.data = ""
        form.password.data = ""
        print("After Auth")
        return redirect(url_for('blog.index'))

    return render_template('login.html', form=form)

@pages.route('/tracking')
def tracking():
    if session['login']:
        return render_template('tracking.html')
    else:
        return render_template('tracking.html')

@pages.route('/elements')
def elements():
    return render_template('elements.html')

@pages.route('/logout')
def logout():
    session.clear()
    session['login'] = False
    return redirect(url_for('blog.index'))