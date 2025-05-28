from flask_wtf import FlaskForm   
from wtforms import StringField, TextAreaField, SubmitField # For better form support
from wtforms.validators import InputRequired, EqualTo       # For form validation

class MessageForm(FlaskForm):
    # Form for user to enter their name and message
    title = StringField('Title', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit')