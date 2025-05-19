# This project is just a reference for e-commerce, so it doesn't have a lot of functionality.

from flask import Flask, Blueprint, render_template, url_for, redirect

ecom_ref = Blueprint('e_com_ref', 
                     __name__,
                    template_folder='templates',
                    static_folder='static')

# Main index route for e-com reference
@ecom_ref.route('/')
def hello_world():
    return render_template('e_com_ref/index.html')

# Redirect to main index route, but we have to call it index, because a URL_FOR cannot use a /
@ecom_ref.route('/index')
def index():
    return redirect('/e_com_ref/')