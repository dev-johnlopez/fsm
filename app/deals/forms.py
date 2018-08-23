from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField

class AddressForm(FlaskForm):
    line_1 = StringField('Street Address', validators=[])
    line_2 = StringField('Street Address', validators=[])
    city = StringField('City', validators=[])
    state_province = StringField('State', validators=[])
    postal_code = StringField('ZIP Code', validators=[])

class SearchForm(FlaskForm):
    line_1 = StringField('Street Address', validators=[])
    city = StringField('City', validators=[])
    state_province = StringField('State', validators=[])
    postal_code = StringField('ZIP Code', validators=[])
    name = StringField('Name', validators=[])

class PropertyForm(FlaskForm):
    address = FormField(AddressForm)
    owner_occupied = BooleanField()

class DealForm(FlaskForm):
    equity = IntegerField('Equity %', validators=[])
    property = FormField(PropertyForm)
