from flask_wtf import FlaskForm   
from wtforms import StringField, PasswordField, SubmitField  # For better form support
from wtforms.validators import InputRequired, EqualTo                       # For form validation

class LoginForm(FlaskForm):
    # Form for user to login
    name = StringField('Name', validators=[InputRequired()], id="login_name")
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('login_confirm_password', message="Passwords must match.")], id="login_password")
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], id="login_confirm_password")
    submit = SubmitField('Submit')
