from index.src.classes import *
from index.src.sqlite import * #sql_set_up, add_user, get_hashed_password, get_feed, create_message
from index.src.wraps import *

from flask import Blueprint, redirect, url_for, request, render_template, make_response, current_app

index_blueprint = Blueprint('index',
                             __name__,
                             template_folder='templates',
                             static_folder='static')

def setup_blueprint() -> None:
    sql_set_up()  # Set up the database
    set_callback_function(hello_world)  # Set the callback function for token_required decorator

# Main index route
@index_blueprint.route('/')
def hello_world(message="None"):
	signup_form = SignupForm()
	login_form 	= LoginForm()
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
@index_blueprint.route('/profile')
@token_required
def profile(user):
    

    return render_template('/index/profile.html')

@index_blueprint.route('/logout')
def logout():
	response = make_response(redirect(url_for('index.index'), code=301))
	response.set_cookie('jwt_token', '', '', expires=0)
	return response

# Login route
# Will update later to help against CSRF
@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        password = request.form['password']
        # Check if user exists in database
		# If so, check if password is correct
        hashed_password = get_hashed_password(user)
        if hashed_password is None:
            return hello_world(message="User does not exist!")
        if check_password(hashed_password, password):
            token = create_token(user)
            response = make_response(redirect(url_for('index.profile'), code=301))
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
			hashed_password = hash_password(password)
            # Create user
			print("Creating user:", user)
			add_user(user, None, None, hashed_password)

			# Create JWT token
			token = create_token(user)

			response = make_response(redirect(url_for('index.profile'), code=301))
			response.set_cookie('jwt_token', token, secure=True, samesite='Strict')

			return response
		else:
			return hello_world(message="Passwords do not match!")
	else:
		return hello_world(message="Please fill out a form!")
	
@index_blueprint.route('/feed')
@token_required
def feed(user):
	feed = get_feed()

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
		
        sql_create_message(user, title, message)
        return redirect(url_for('index.feed'), code=301)