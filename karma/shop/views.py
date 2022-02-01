from flask import render_template,  Blueprint, session, redirect, url_for
from karma import db

shop = Blueprint('shop', __name__)


@shop.route('/category')
def category():
    return render_template('category.html')

@shop.route('/cart')
def cart():
    if session['login']:
        data = db.child("cart").child(session['id']).get().val()
        return render_template('cart.html', data = data)
    else:
        return redirect(url_for('blog.index'))


