# Main landing point for flask application
import sqlite3

from flask import Flask, Blueprint, redirect, url_for, request, render_template
from flask_bcrypt import Bcrypt                            # For password hashing
from flask_wtf import FlaskForm                             # For CSRF and forms
from wtforms import StringField, PasswordField, SubmitField # For better form support
from wtforms.validators import InputRequired, EqualTo        # For form validation


class MessageForm(FlaskForm):
    # Form for user to enter their name and message
    name = StringField('Name', validators=[InputRequired()])
    password = PasswordField('Message', validators=[InputRequired(), EqualTo('confirm_password', message="Passwords must match.")])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], id="confirm_password")
    submit = SubmitField('Submit')

def set_up():
    # Set up the database
    db = sqlite3.connect('database.db', check_same_thread=False)
    # Delete the table after every set up of server
    db.execute('''
                DROP TABLE IF EXISTS users
                ''')
    # Create new table with 2 columns
    # Name and message
    db.execute('''
               CREATE TABLE IF NOT EXISTS users \
               (name TEXT, message TEXT)
               ''')
    db.commit()
    db.close()
    print("Database set up complete.")

index_blueprint = Blueprint('index',
                             __name__,
                             template_folder='templates',
                             static_folder='static')

bcrypt = Bcrypt()  # Initialize bcrypt for password hashing

# Test route
@index_blueprint.route('/test', methods=['GET', 'POST'])
def test():
    form = MessageForm()
    if form.validate_on_submit():
        print(form.name.data)
        print(form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_password)
        print(f"Is valid:  {bcrypt.check_password_hash(hashed_password, form.password.data)}")
        return "Got data!"
        
    return render_template('index/test.html', form=form)

# Main index route
@index_blueprint.route('/')
def hello_world():
    return render_template('index/index.html')

# Redirect to main index route, but we have to call it index, because a URL_FOR cannot use a /
@index_blueprint.route('/index')
def index():
    return redirect('/')

# Success for logging in, will update later
@index_blueprint.route('/success')
def success():
    connect = sqlite3.connect('database.db')
    cur = connect.cursor()
    # Get everything and pass it to webpage
    cur.execute('''
                SELECT * FROM users
                ''')
    data = cur.fetchall()
    connect.close()

    return render_template('/index/success.html', data=data)

# Login route
# Will update later to help against CSRF
@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        message = request.form['message']
        print(user)
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(''' INSERT INTO users (name, message) VALUES (?,?) ''', (user, message))
            con.commit()
        return redirect(url_for('index.success'), code=301)
    else:
        return render_template('index.index.html')