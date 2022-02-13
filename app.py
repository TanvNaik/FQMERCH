from flask import Flask, redirect, render_template, url_for, session
import razorpay
from karma import app
from karma.pages.forms import AddressForm

@app.route('/pay',methods=["GET","POST"])
def pay():
    if session['login']:
        form = AddressForm('/blog.index')
        username = session['username']
        amount = int(2)*100
        client = razorpay.Client(auth=("rzp_test_aFHgpPQ2Qr3esy", "wJPj0PREZEPGzNTS25e4p4Ac"))
        payment = client.order.create({'amount': int(amount), 'currency':'INR', 'payment_capture':'1'})
        print(payment)
        return render_template('pay.html', form=form, payment=payment, amount=amount)
    else:
        return redirect(url_for('blog.index')) 


if __name__ == "__main__":
    app.run(debug=True)
