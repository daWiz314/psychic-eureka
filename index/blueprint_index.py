# Main landing point for flask application
import sqlite3

from datetime import datetime, timedelta, timezone			# For JWT token generation
from functools import wraps									# For creating decorators
from flask import Blueprint, redirect, url_for, request, render_template, make_response, current_app
from flask_bcrypt import Bcrypt as bcrypt                   # For password hashing
from flask_wtf import FlaskForm                             # For CSRF and forms
import jwt 													# For JWT token generation and verification
from wtforms import StringField, TextAreaField, PasswordField, SubmitField # For better form support
from wtforms.validators import InputRequired, EqualTo       # For form validation

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.cookies.get('jwt_token')

		if not token:
			return hello_world(message="You need to be logged in!")
		
		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
			current_user = data['user']
		except:
			return hello_world(message="You need to be logged in!")
		
		return f(current_user, *args, **kwargs)
	return decorated

class MessageForm(FlaskForm):
    # Form for user to enter their name and message
    title = StringField('Title', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit')

class signupForm(FlaskForm):
    # Form for user to create an account
    name = StringField('Name', validators=[InputRequired()], id="signup_name")
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('signup_confirm_password', message="Passwords must match.")], id="signup_password")
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], id="signup_confirm_password")
    submit = SubmitField('Submit')

class loginForm(FlaskForm):
    # Form for user to login
    name = StringField('Name', validators=[InputRequired()], id="login_name")
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('login_confirm_password', message="Passwords must match.")], id="login_password")
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], id="login_confirm_password")
    submit = SubmitField('Submit')

def set_up():
    # Set up the database
	db = sqlite3.connect('database.db', check_same_thread=False)
    # Delete the table after every set up of server
	db.execute('''
                DROP TABLE IF EXISTS users
                ''')
    # Create new table with 3 columns
    # Name, message, password
	db.execute('''
               CREATE TABLE IF NOT EXISTS users (
                    name TEXT, 
					title TEXT,
                    message TEXT,
                    password TEXT,
					id INTEGER PRIMARY KEY AUTOINCREMENT
               )
               ''')
	db.commit()
	db.close()
	print("Database set up complete.")

	# Remove old JWT token
	
index_blueprint = Blueprint('index',
                             __name__,
                             template_folder='templates',
                             static_folder='static')


# Main index route
@index_blueprint.route('/')
def hello_world(message="None"):
	signup_form = signupForm()
	login_form 	= loginForm()
	signup_form = signupForm()
	login_form 	= loginForm()
	forms 		= {
				'signup_form': 	signup_form,
				'login_form':  	login_form,
				'messages':		[]
	}
	if message != "None":
		forms['messages'].append(message)
	return render_template('index/index.html', forms=forms)

# Route for the main page
@index_blueprint.route('/index')
def index():
     return redirect('/', code=301)

# Success for logging in, will update later
@index_blueprint.route('/success')
def success():
    

    return render_template('/index/success.html')

# Login route
# Will update later to help against CSRF
@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = request.form['name']
		password = request.form['password']
        # Check if user exists in database
		# If so, check if password is correct
		with sqlite3.connect("database.db") as con:
			cur = con.cursor()
			cur.execute('''
						SELECT password FROM users WHERE name = ?
						''', (user,))
			data = cur.fetchone()
			print(data)
			if data is None:
				return hello_world(message="User does not exist!")
			else:
				# Check if password is correct
				if bcrypt().check_password_hash(data[0], password):
					token = jwt.encode({"user": user, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, current_app.config['SECRET_KEY'], algorithm='HS256')

					response = make_response(redirect(url_for('index.success'), code=301))
					response.set_cookie('jwt_token', token, secure=True, samesite='Strict')

					return response
				else:
					return hello_world(message="Incorrect password!")
	else:
		return hello_world(message="Please fill out a form!")

@index_blueprint.route('/create_account', methods=['GET', 'POST'])
def create_account():
	if request.method == 'POST':
		if request.form['password'] == request.form['confirm_password']:
			print(request.form['password'])
			user = request.form['name']
			password = request.form['password']
			hashed_password = bcrypt().generate_password_hash(password).decode('utf-8')

			# Check if user already exists
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute('''
						SELECT name FROM users WHERE name = ?
						''', (user,))
				data = cur.fetchone()
				if data is not None:
					return hello_world(message="User already exists!")
				else:
					print("User does not exist, creating account.")
			
			# User does not exist, continue with input
               
			with sqlite3.connect("database.db") as con:
				cur = con.cursor()
				cur.execute('''
                INSERT INTO users (
                	name,  
                	password
                ) 
                VALUES (?,?) ''', (user, hashed_password))
				con.commit()
				
			token = jwt.encode({"user": user, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, current_app.config['SECRET_KEY'], algorithm='HS256')

			response = make_response(redirect(url_for('index.success'), code=301))
			response.set_cookie('jwt_token', token, secure=True, samesite='Strict')

			return response
	else:
		return hello_world(message="Please fill out a form!")
	

@index_blueprint.route('/feed')
@token_required
def feed(user):
	# Get all usernames from database
	connect = sqlite3.connect('database.db')
	cur = connect.cursor()

	cur.execute('''
				SELECT name FROM users
				''')
	data = cur.fetchall()

	# House all the data together
	# in a list of dictionaries
	feed = []

	# Get all messages from each name
	for name in data:
		cur.execute('''
					SELECT message FROM users WHERE name = ?
					''', (name[0],))
		messages = cur.fetchall()
		cur.execute('''
			  		SELECT title FROM users WHERE name = ?
			  		''', (name[0],))
		titles = cur.fetchall()

		feed.append({
			'name'		: name[0],
			'count'		: len(messages),
			'messages'	: [titles[0], messages[0]]
		})
	connect.close()
	return render_template('/index/feed.html', data=feed)

@index_blueprint.route('/create-message', methods=['GET', 'POST'])
@token_required
def create_message(user, display_message="None"):
	form_message = MessageForm()

	if request.method == 'GET':
		form_message = MessageForm()
		display_message = "None"
		return render_template('/index/create_message.html', form=form_message, display_message=display_message)

	if form_message.validate_on_submit():
		message = form_message.message.data
		title = form_message.title.data
		with sqlite3.connect("database.db") as con:
			cur = con.cursor()
			cur.execute(''' 
						UPDATE users SET message = ? WHERE name = ?;
						''', (message, user))
			cur.execute('''
			   			UPDATE users SET title = ? WHERE name = ?;
			   			''', (title, user))
			con.commit()
		return redirect(url_for('index.feed'), code=301)