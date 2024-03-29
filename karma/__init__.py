from flask import Flask, render_template, request, url_for, session, redirect
import smtplib
import os 
import pyrebase


sender_email = os.environ.get('senderEmail')
email_pass = os.environ.get('emailPass')


firebaseConfiguration = {
'apiKey': "AIzaSyDYc_fsQa6MgJZMTQd_Dp-qhvyc93V-XuY",
  'authDomain': "fq-merch.firebaseapp.com",
  'databaseURL': "https://fq-merch-default-rtdb.firebaseio.com",
  'projectId': "fq-merch",
  'storageBucket': "fq-merch.appspot.com",
  'messagingSenderId': "27867821793",
  'appId': "1:27867821793:web:a06f9ca5cd4458ffb0e9a0",
  'measurementId': "G-SKCLJFEJN9"
}
firebase = pyrebase.initialize_app(firebaseConfiguration)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


app = Flask(__name__)
app.secret_key = "mysecretkey"


def send_email(user, pwd, recipient, subject, body):

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    with smtplib.SMTP_SSL(host="mail.stackx.online") as smtp:
        smtp.login(user, pwd)
        smtp.sendmail(user, TO, message)
        smtp.quit()


from karma.shop.views import shop
from karma.blog.views import blog
from karma.pages.views import pages
from karma.additem.views import additem
from karma.payment.views import payment

app.register_blueprint(shop)
app.register_blueprint(blog)
app.register_blueprint(pages)
app.register_blueprint(additem)
app.register_blueprint(payment)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/subscribe', methods=['POST','GET'])
def subscribe():
    email = request.form['email']
    mail_type = request.form['mail_type']
    if mail_type == "query-mail":
        subject = request.form['subject'] 
        message = request.form['message']
        send_email(sender_email, email_pass, email, "Thankyou for contacting us","Our representative will reach to you soon.\nTeam Stackx")
        return render_template('contact.html')

    else:
        send_email("info@stackx.online", "StackX@123", email, "ThankYou", "Thankyou For subscribing NewsLetter")
        return redirect(url_for("blog.index"))

