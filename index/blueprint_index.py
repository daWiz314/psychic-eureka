# Main landing point for flask application

from flask import Flask, Blueprint, redirect, url_for, request, render_template

index_blueprint = Blueprint('index',
                             __name__,
                             template_folder='templates',
                             static_folder='static')

# Main index route
@index_blueprint.route('/')
def hello_world():
    return render_template('index/index.html')

# Redirect to main index route, but we have to call it index, because a URL_FOR cannot use a /
@index_blueprint.route('/index')
def index():
    return redirect('/')

# Success for logging in, will update later
@index_blueprint.route('/success/<name>')
def success(name):
    return render_template('/index/success.html', name=name)

# Login route
# Will update later to help against CSRF
@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('index.success', name=user), code=301)
    else:
        return render_template('index.html')