from flask import render_template, Blueprint, url_for, jsonify, session, request, redirect
from karma import db
import razorpay
from karma.pages.forms import AddressForm, TrackingForm

payment = Blueprint('payment',__name__)


@payment.route('/orderSummary', methods=['POST','GET'])
def orderSummary():
    if session['login']:
        form = AddressForm()
        pay = request.form['payment']
        amount = int(session['totalprice'])*100
        client = razorpay.Client(auth=("rzp_test_aFHgpPQ2Qr3esy", "wJPj0PREZEPGzNTS25e4p4Ac"))
        if pay == "paymentpage":
            payment_id = request.form['razorpay_payment_id'],
            razorpay_order_id = request.form['razorpay_order_id'],
            razorpay_signature = request.form['razorpay_signature']

            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': razorpay_signature
            }
            data = client.payment.fetch(payment_id[0])
            data['is_delivered'] = False
            data['products'] = session['data']
            db.child('order').child(session['id']).child(data['order_id']).set(data)
            # db.child('cart').child(session['id']).remove()
            return render_template('success.html',**data)
            # result = client.utility.verify_payment_signature(params_dict) 
            # if result is None:
            #     try:
            #         print(data)
            #         client.payment.capture(payment_id, amount)
            #         return render_template('success.html', data = data)
            #     except:
            #         return render_template('success.html', data = "fail")
            # else:
            #     return render_template('success.html', data = "fail")
        else:
            payment = client.order.create({'amount': amount, 'currency':'INR', 'payment_capture':'1'})
            session['order_id'] = payment['id']
            products = session['data']
            return render_template('pay.html', data=products, payment=payment, form=form)
    else:
        return redirect(url_for('blog.index'))


@payment.route('/address', methods=['POST','GET'])
def address():
    if session['login']:
        form = AddressForm()
        if form.validate_on_submit():
            userid = session['id']
            address = {
                'name': form.name.data,
                'mobile': form.mobile.data,
                'pincode': form.pincode.data,
                'address': form.address.data,
                'city': form.city.data,
                'landmark': form.landmark.data,
                'alternatemobile': form.alternatemobile.data,
                'state': form.state.data
            }
            db.child("users").child(userid).child("address").set(address)
            session['address'] = address['name']+","+address['landmark']+","+address['address']+","+address['state']+","+str(address['pincode'])
            return redirect(url_for('payment.orderSummary'))
    return redirect(url_for('blog.index'))


@payment.route('/tracking', methods=['POST','GET'])
def tracking():
    if session['login']:
        form = TrackingForm()
        if form.validate_on_submit():
            orderid = request.form['orderid']
            userid = session['id']
            data = db.child("order").child(userid).child(orderid).get().val()
            # print(data)
            if data is None:
                return jsonify({"error":"Invalid Order ID"})
            products = data['products']
            print(products)
            return render_template('tracking.html', **data, isdata=True, form=form, **products)
        return render_template('tracking.html', isdata=False, form=form)
    
    return redirect(url_for('blog.index'))

