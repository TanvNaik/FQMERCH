import sys

from flask import render_template, Blueprint, session
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
    if session['id'] == None:
        session['login'] = False
    filename = os.path.join(app.static_folder, 'json/feature.json') 
    f = open(filename) 
    file = json.load(f) 
    products = db.child("products").get().val()
    hotdealsproductfromDB = db.child('hotdealsproduct').get().val()
    unpackedproduct = {}
    hotdealsid = ""
    for key,value in hotdealsproductfromDB.items():
        unpackedproduct = value
        hotdealsid = key
    hotdealsproduct = {
        'hotdealsimage' : unpackedproduct['image'],
        'hotdealsname': unpackedproduct['productname'],
        'hotdealsprice': unpackedproduct['price'],
        'hotdealsoriginalprice': unpackedproduct['originalprice'],
        'hotdealsreleasedate': unpackedproduct['releaseDate']
    }
    return render_template('index.html', data=file , hotdealsid = hotdealsid , **hotdealsproduct, products=products)

    