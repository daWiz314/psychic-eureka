from flask_wtf import FlaskForm   
from wtforms import StringField, PasswordField, SubmitField  # For better form support
from wtforms.validators import InputRequired, EqualTo                       # For form validation
                                           # Import FlaskForm from Flask-WTF package
class SignupForm(FlaskForm):
    # Form for user to create an account
    name = StringField('Name', validators=[InputRequired()], id="signup_name")
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('signup_confirm_password', message="Passwords must match.")], id="signup_password")
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], id="signup_confirm_password")
    submit = SubmitField('Submit')