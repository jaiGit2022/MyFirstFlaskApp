from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, BooleanField, FileField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    due_date = DateField('Due Date')
    completion = BooleanField('Completion Status')
    completion_date = DateField('Completion Date')

    file = FileField('Upload file')

    submit = SubmitField('Post')