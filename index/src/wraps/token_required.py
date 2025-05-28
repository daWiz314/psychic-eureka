

import jwt 													# For JWT token generation and verification
from datetime import datetime, timedelta, timezone			# For JWT token generation
from flask_bcrypt import Bcrypt as bcrypt                   # For password hashing
from flask import request, current_app
from functools import wraps									# For creating decorators

call_back_function = None

def set_callback_function(func):
	"""
	Sets a callback function that will be called when the user is not authenticated.
	"""
	global call_back_function
	call_back_function = func

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.cookies.get('jwt_token')

		if not token:
			return call_back_function(message="You need to be logged in!")
		
		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
			current_user = data['user']
		except:
			return call_back_function(message="You need to be logged in!")
		
		return f(current_user, *args, **kwargs)
	return decorated

def hash_password(password):
	"""
	Hashes the provided password using bcrypt.
	"""
	return bcrypt().generate_password_hash(password).decode('utf-8')

def check_password(db_password, password):
	"""
	Checks if the provided password matches the hashed password from the database.
	"""
	return bcrypt().check_password_hash(db_password, password)

def create_token(user):
	"""
	Creates a JWT token for the given user.
	"""
	return jwt.encode({"user": user, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, current_app.config['SECRET_KEY'], algorithm='HS256')