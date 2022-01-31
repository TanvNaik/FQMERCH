from flask import Flask, render_template, Blueprint


blog = Blueprint('blog', __name__)

@blog.route('/blogs')
def blogs():
    return render_template('blogs.html')

@blog.route('/singleblog')
def singleblog():
    return render_template('singleblog.html')

@blog.route('/')
def index():
    return render_template('index.html')