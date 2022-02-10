from flask import Flask, redirect, render_template, url_for

import razorpay
from karma import app


@app.route('/charge', methods=["GET","POST"])
def charge():
    return redirect(url_for('pay'))

@app.route('/pay',methods=["GET","POST"])
def pay():
    username = session['username']
    amount = int(2)*100
    client = razorpay.Client(auth=("rzp_test_aFHgpPQ2Qr3esy", "wJPj0PREZEPGzNTS25e4p4Ac"))
    payment = client.order.create({'amount': int(amount), 'currency':'INR', 'payment_capture':'1'})
    print(payment)
    return render_template('pay.html', payment=payment, amount=amount) 


if __name__ == "__main__":
    app.run(debug=True)
