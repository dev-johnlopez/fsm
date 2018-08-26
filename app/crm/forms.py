from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])
    type = StringField('Type', validators=[])
    phone = StringField('Phone', validators=[])
    email = StringField('Email', validators=[])
