from flask import render_template, Blueprint
import json
import os
from karma import app, db


blog = Blueprint('blog', __name__)

@blog.route('/blogs')
def blogs():
    return render_template('blogs.html')

@blog.route('/singleblog')
def singleblog():
    return render_template('singleblog.html')

@blog.route('/')
def index():
    filename = os.path.join(app.static_folder, 'json/feature.json')
    f = open(filename)
    file = json.load(f)
    products = db.child("products").get().val() 
    return render_template('index.html', data=file, products=products) 

    