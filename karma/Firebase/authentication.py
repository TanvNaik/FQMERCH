from flask import render_template
from firebaseConfig import auth

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return render_template("index.html")
    except:
        return "Invalid email or password"
