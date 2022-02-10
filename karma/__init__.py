from flask import Flask, render_template, request, url_for
import smtplib
import pyrebase

firebaseConfiguration = {
"apiKey": "AIzaSyAlzqAG9Ag670HIBzzjnIum6zpnk0o80t8",
  "authDomain": "ecommerce-flask.firebaseapp.com",
  "projectId": "ecommerce-flask",
  "storageBucket": "ecommerce-flask.appspot.com",
  "messagingSenderId": "180291136079",
  "appId": "1:180291136079:web:61b4affc41900d387c183a",
  "measurementId": "G-9C493M27G0",
  "databaseURL": "https://ecommerce-flask-default-rtdb.firebaseio.com/"
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

app.register_blueprint(shop)
app.register_blueprint(blog)
app.register_blueprint(pages)
app.register_blueprint(additem)


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
        send_email(sender_email, email_pass, email, "ThankYou", "Thankyou For subscribing NewsLetter")
        return render_template('index.html')

