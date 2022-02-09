from flask import render_template,  Blueprint, session, redirect, url_for
from karma import db

shop = Blueprint('shop', __name__)


@shop.route('/category')
def category():
    if session['login']:
        products = db.child("products").get().val() 
        brands = db.child("brands").get().val()
        colors = db.child("colors").get().val()
        categories = db.child("categories").get().val()
        return render_template('category.html', products=products, brands = brands, colors = colors, categories = categories)
    else:
        return redirect(url_for('blog.index')) 


@shop.route('/cart')
def cart():
    if session['login']:
        data = db.child("cart").child(session['id']).get().val()
        return render_template('cart.html', data = data)
    else:
        return redirect(url_for('blog.index'))


