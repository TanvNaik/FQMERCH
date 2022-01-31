from flask import render_template, redirect, url_for, session, jsonify, Blueprint
from karma.pages.forms import RegisterForm, LoginForm
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
        return redirect(url_for('blog.index'))

    return render_template('login.html', form=form)

@pages.route('/tracking')
def tracking():
    if session['login']:
        return render_template('tracking.html')
    else:
        return redirect(url_for('blog.index'))

@pages.route('/logout')
def logout():
    session.clear()
    session['login'] = False
    return redirect(url_for('blog.index'))







# @pages.route('/elements')
# def elements():
#     return render_template('elements.html')
