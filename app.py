from flask import Flask, redirect, render_template, url_for, session
import razorpay, sys
from karma import app
from karma.pages.forms import AddressForm

@app.route('/pay',methods=["GET","POST"])
def pay():
    if session['login']:
        global payment
        form = AddressForm('/blog.index')
        username = session['username']
        # amount = int(2)*100
        amount =session['totalprice']
        client = razorpay.Client(auth=("rzp_test_YpuKMpzBvFaEqL", "g6zFdtaMQqCrP7Tqe4ipdnwx"))
        payment = client.order.create({'amount': amount, 'currency':'INR', 'payment_capture':'1'})
        print(payment, file= sys.stderr)
        return render_template('checkout.html', form=form, payment=payment, amount=amount)
    else:
        return redirect(url_for('blog.index')) 


if __name__ == "__main__":
    app.run(debug=True)
