from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, Blueprint


pages = Blueprint('pages', __name__)

@pages.route('/login')
def login():
    return render_template('login.html')

@pages.route('/tracking')
def tracking():
    return render_template('tracking.html')

@pages.route('/elements')
def elements():
    return render_template('elements.html')