from flask import render_template, Blueprint, url_for, session, jsonify, request, redirect
from karma import db
from datetime import datetime
import random
from karma.pages.forms import ProductForm
from karma.pages.picture_handler import add_pic


additem = Blueprint('additem',__name__)


@additem.route('/addproduct', methods=["POST","GET"])
def add():
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
        db.child("products").child(id).set(item)

    return render_template('product.html', form=form)


@additem.route('/addtocart', methods=["POST","GET"])
def addtocart():
    productid = request.form['productid']
    userid = session['id']
    data = db.child("products").child(productid).get().val()
    db.child("cart").child(userid).child(productid).set(data)
    return redirect(url_for('shop.cart'))

@additem.route('/deletefromcart', methods=["POST","GET"])
def deletefromcart():
    productid = request.form['productid']
    userid = session['id']
    db.child("cart").child(userid).child(productid).remove()
    return redirect(url_for('shop.cart'))
