from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
# This imports only specific validators, but WTForms docs also show
# examples importing all the validators and accessing them within the
# validators.validator namespace.
# E.g. from wtforms import validators
from wtforms.validators import DataRequired, Length


class EditNoteForm(FlaskForm):
    note_title = StringField('Title:',
                             validators=[DataRequired(),
                                         Length(max=80)])
    note_body = TextAreaField('Note:',
                              validators=[DataRequired(),
                                          Length(max=4000)])
    submit = SubmitField('Submit')
    
class ConfirmDeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')