from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired

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
    property_type = SelectField('Property Type', choices=[
                                        ('', ''),
                                        ('sfr', 'Single Family'),
                                        ('residential_multi_family', 'Residential Multi Family'),
                                        ('commercial_multi_family', 'Commercial Multi Fmaily'),
                                        ('self_storage', 'Self Storage'),
                                        ('retail', 'Retail')],
                            validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[])
    bathrooms = IntegerField('Bathrooms', validators=[])
    sq_feet = IntegerField('Sq. Feet', validators=[])

class DealForm(FlaskForm):
    property = FormField(PropertyForm)
    list_price = IntegerField('List Price', validators=[])
    rehab_amount = IntegerField('Rehab Est.', validators=[])
    after_repair_value = IntegerField('ARV', validators=[])
    equity = IntegerField('Equity', validators=[])
    return_on_investment = StringField('ROI', validators=[])
    monthly_rent = IntegerField('Monthly Rent', validators=[])
    taxes = IntegerField('Taxes', validators=[])
    insurance = IntegerField('Insurance', validators=[])
    maintenance_percent = IntegerField('Maintenance', validators=[])
    management_percent = IntegerField('Management', validators=[])
    utility_amount = IntegerField('Utilities', validators=[])
    utility_description = StringField('Desc. of Utilities', validators=[])
    capex_reserves = IntegerField('Capex', validators=[])
    net_operating_income = IntegerField('NOI', validators=[])
    cap_rate = StringField('Cap Rate', validators=[])

class MarketDealForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
