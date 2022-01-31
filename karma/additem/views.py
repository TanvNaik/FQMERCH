from flask import render_template, Blueprint, url_for
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
            print("Image comes")
            pic = add_pic(form.image.data, form.productname.data)
        picture = url_for('static', filename='category/'+pic)
        item['image'] = picture
        id = random.randint(100000, 1000000000)
        db.child("products").child(item['productcategory']).child(id).set(item)

    return render_template('product.html', form=form)



