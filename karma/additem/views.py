from flask import render_template, Blueprint, url_for, json, session, jsonify, request, redirect
from karma import db
from karma.pages.forms import AddressForm
import razorpay
from datetime import datetime
import random,sys
from karma.pages.forms import ProductForm
from karma.pages.picture_handler import add_pic


additem = Blueprint('additem',__name__)


@additem.route('/addproduct', methods=["POST","GET"])
def add():
    if session['login']:
        form = ProductForm()
        if form.validate_on_submit():
            now = datetime.now()
            now = str(now.strftime("%S%M%H%d%m%Y"))
            item = {
                'productcategory' : form.productcategory.data,
                'productname' : form.productname.data,
                'price' : form.price.data,
                'originalprice' : form.originalprice.data,
                'stock' : form.stock.data,
                'type':form.producttype.data,
                'image' : form.image.data,
                'time': now
            }
            if form.image.data:
                pic = add_pic(form.image.data, form.productname.data)
            picture = url_for('static', filename='category/'+pic)
            item['image'] = picture
            id = random.randint(100000, 1000000000)
            if db.child("brands").child(item['brand']).get().val() == None:
                db.child("brands").child(item['brand']).set(item['brand'])

            if db.child("colors").child(item['color']).get().val() == None:
                db.child("colors").child(item['color']).set(item['color'])

            db.child("products").child(id).set(item)
        return render_template('product.html', form=form)
    else:
        return redirect(url_for('blog.index'))


@additem.route('/addtocart', methods=["POST","GET"])
def addtocart():
    if session['login']:
        productid = request.form['productid']
        userid = session['id']
        if request.form['movetocart']:
            db.child("wishList").child(userid).child(productid).remove() 
        check = db.child("cart").child(userid).child(productid).get().val() 
        data = db.child("products").child(productid).get().val() 
        data['count'] = 1
        db.child("cart").child(userid).child(productid).set(data)
        data = db.child("cart").child(userid).get().val()
        totalprice = db.child("cart").child(userid).child("totalprice").get().val()
        if totalprice == None: 
            totalprice = int(0)
        totalprice = int(totalprice)
        if check == None:
            totalprice += int(data[productid]["price"]) 

        db.child("cart").child(userid).child("totalprice").set(totalprice)
        return redirect(url_for('shop.cart'))

    else:
        return redirect(url_for('blog.index'))


# manage count of product in cart
@additem.route('/incdecqty', methods=['POST','GET'])
def incdecqty():
    productid = request.form['productid']
    type = request.form['type']
    userId = session['id']
    cart = db.child('cart').child(userId).get().val()
    if type == "increment":
        cart[productid]['count'] += 1
        if cart[productid]['count'] > cart[productid]['stock']:
            return jsonify({"error":"Product Get Out Of Stock"})
        cart['totalprice'] += int(cart[productid]['price'])
    else:
        cart['totalprice'] -= int(cart[productid]['price'])
        if(cart[productid]['count'] == 1):
            cart.pop(productid)
        else:
            cart[productid]['count'] -= 1
    
    db.child('cart').child(userId).set(cart)
    return redirect(request.referrer)


@additem.route('/deletefromcart', methods=["POST","GET"])
def deletefromcart():
    if session['login']:
        productid = request.form['productid']
        userid = session['id']
        totalprice = db.child("cart").child(userid).child("totalprice").get().val()
        data = db.child("cart").child(userid).get().val()
        db.child("cart").child(userid).child(productid).remove()
        if totalprice == None: 
            totalprice = int(0)
        totalprice = int(totalprice)
        totalprice -= int(data[productid]["price"])

        db.child("cart").child(userid).child("totalprice").set(totalprice)
        return redirect(url_for('shop.cart'))
    
    else:
        return redirect(url_for('blog.index'))

@additem.route('/addToWishList', methods=['POST','GET'])
def addToWishList():
    if session['login']:
        productId = request.form['productid']
        userId = session['id']
        productData = db.child('products').child(productId).get().val()
        db.child('wishList').child(userId).child(productId).set(productData)
        return redirect(url_for('shop.wishList'))

    else:
        return redirect(url_for('blog.index'))

@additem.route('/deleteFromWishList', methods=['POST','GET'])
def deleteFromWishList():
    if session['login']:
        productid = request.form['productid']
        userid = session['id']
        db.child("wishList").child(userid).child(productid).remove()
        return redirect(url_for('shop.wishList'))

    else:
        return redirect(url_for('blog.index'))


# @additem.route('/movetocart', methods=["POST","GET"])
# def movetocart():
#     if session['login']:
#         productid = request.form['productid']
#         userid = session['id']
#         db.child("wishList").child(userid).child(productid).remove() 
#         return redirect(url_for('shop.cart'))
#     else:
#         return redirect(url_for('blog.index'))


@additem.route('/filter', methods=["POST","GET"])
def filter():
    if session['login']:
        filter = request.form['filter']
        filtervalue = request.form['filtervalue']
        categories = db.child("categories").get().val()
        products = db.child("products").order_by_child(filter).equal_to(filtervalue).get().val()
        msg = "Results for products of "+filter+" "+filtervalue
        return render_template('category.html', products=products, categories = categories, msg = msg)
    else:
        return redirect(url_for('blog.index'))

@additem.route('/filterprice', methods=["POST","GET"])
def filterprice():
    if session['login']:
        startprice = int(request.form['startprice'])
        endprice = int(request.form['endprice'])
        brands = db.child("brands").get().val()
        colors = db.child("colors").get().val()
        categories = db.child("categories").get().val()
        products = db.child("products").order_by_child('price').start_at(startprice).end_at(endprice).get().val()
        msg = "Results for products in range of $"+str(startprice)+"-"+str(endprice)
        return render_template('category.html', products=products, brands = brands, colors = colors, categories = categories, msg=msg) 
    
    else:
        return redirect(url_for('blog.index'))


@additem.route('/orderSummary', methods=['POST','GET'])
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
            db.child('cart').child(session['id']).remove()
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


@additem.route('/address', methods=['POST','GET'])
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
            return redirect(url_for('additem.orderSummary'))