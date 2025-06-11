from flask_wtf import FlaskForm   
from wtforms import TextAreaField, SubmitField # For better form support
from wtforms.validators import InputRequired       # For form validation

class NoteForm(FlaskForm):
    # Form for user to create a note
    note = TextAreaField('Note', validators=[InputRequired()], id='notes_textarea', render_kw={"rows": 10, "cols": 50})
    submit = SubmitField()