from index.src.classes import *
from index.src.sqlite import * #sql_set_up, add_user, get_hashed_password, get_feed, create_message
from index.src.wraps import *

from flask import Blueprint, redirect, url_for, request, render_template, make_response, current_app, send_file

index_blueprint = Blueprint('index',
                             __name__,
                             template_folder='templates',
                             static_folder='static')

SQLObject = SQLiteHandler()

def setup_blueprint() -> None:
    # sql_set_up()  # Set up the database
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

# For the PWA
@index_blueprint.route('/manifest.json')
def serve_manifest():
      return send_file('index/static/pwa/manifest.json', mimetype='application/manifest+json')

# For the PWA service worker
@index_blueprint.route('/sw.js')
def serve_service_worker():
    return send_file('index/static/pwa/sw.js', mimetype='application/javascript')

# Success for logging in, will update later
@index_blueprint.route('/profile')
@token_required
def profile(user):
    return render_template('/index/profile.html')

@index_blueprint.route('/logout')
def logout():
	response = make_response(redirect(url_for('index.index'), code=301))
	response.set_cookie('jwt_token', '', None, expires=0)
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
			add_user(user, hashed_password)

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
	feed = SQLObject.get_feed()

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

        SQLObject.create_message(user, title, message)
        
        return redirect(url_for('index.feed'), code=301)


@index_blueprint.route('/create-note', methods=['GET', 'POST'])
@token_required
def create_note(user):

    form_note = NoteForm()

    notes, _ = SQLObject.get_notes(user)
    if notes:
        print("Notes found for user:", user)
    else:
        print("No notes found for user:", user)

    print("Called by method:", request.method)

    if request.method == 'GET':
        # form_note = NoteForm()
        return render_template('index/create_note.html', form=form_note, notes=notes)

    if form_note.validate_on_submit():
        note = form_note.note.data
        print("Creating note:", note)
        SQLObject.create_note(user, note)
        return redirect(url_for('index.view_notes'), code=301)
    else:
        print("Form validation failed:", form_note.errors)
        
        return render_template('index/create_note.html', form=form_note, notes=notes, error=form_note.errors)

@index_blueprint.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@token_required
def edit_note(user, note_id):
    form_note = NoteForm()
    notes = sql_get_notes(user)


@index_blueprint.route('/view-notes')
@token_required
def view_notes(user):
    notes, shared_with = SQLObject.get_notes(user)
    print("Notes for user:", user)
    print(notes)
    return render_template('index/view_notes.html', user_notes=notes, shared_with=shared_with)


if __name__ == '__main__':
    print("What are you doing? This is not a main file!")
    exit(1)
# This file is not meant to be run directly. It is a Flask blueprint for routing.
# It should be imported and registered in a Flask application.