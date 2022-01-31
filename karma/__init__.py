from flask import Flask, render_template, request
import smtplib
import os 


app = Flask(__name__)
app.secret_key = os.environ.get("secretKey")

sender_email = os.environ.get('senderEmail')
email_pass = os.environ.get('emailPass')


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

app.register_blueprint(shop)
app.register_blueprint(blog)
app.register_blueprint(pages)

@app.route('/')
def index():
    return render_template('index.html')

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
        return render_template('index.html')

