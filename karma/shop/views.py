from flask import render_template,  Blueprint


shop = Blueprint('shop', __name__)


@shop.route('/category')
def category():
    return render_template('category.html')

@shop.route('/cart')
def cart():
    return render_template('cart.html')




# @shop.route('/singleproduct')
# def singleproduct():
#     return render_template('singleproduct.html')

# @shop.route('/checkout')
# def checkout():
#     return render_template('checkout.html')

# @shop.route('/confirmation')
# def confirmation():
#     return render_template('confirmation.html')

