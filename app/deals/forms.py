from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.fieldtypes import StateSelectField

class AddressForm(FlaskForm):
    line_1 = StringField('Street Address', validators=[])
    line_2 = StringField('Street Address', validators=[])
    city = StringField('City', validators=[])
    state_province = SelectField('State', choices=[
        ('AK','Alaska'),
        ('AL','Alabama'),
        ('AR','Arkansas'),
        ('AZ','Arizona'),
        ('CA','California'),
        ('CT','Connecticut'),
        ('DC','Washington DC'),
        ('DE','Delaware'),
        ('FL','Florida'),
        ('GA','Georgia'),
        ('HI','Hawaii'),
        ('IA','Iowa'),
        ('ID','Idaho'),
        ('IL','Illinois'),
        ('IN','Indiana'),
        ('KS','Kansas'),
        ('KY','Kentucky'),
        ('LA','Louisiana'),
        ('MA','Massachusetts'),
        ('MA','Massachusetts'),
        ('MD','Maryland'),
        ('ME','Maine'),
        ('MI','Michigan'),
        ('MN','Minnesota'),
        ('MO','Missouri'),
        ('MS','Mississippi'),
        ('MT','Montana'),
        ('NC','North Carolina'),
        ('ND','North Dakota'),
        ('NE','Nebraska'),
        ('NH','New Hampshire'),
        ('NJ','New Jersey'),
        ('NM','New Mexico'),
        ('NV','Nevada'),
        ('NY','New York'),
        ('OH','Ohio'),
        ('OK','Oklahoma'),
        ('OR','Oregon'),
        ('PA','Pennsylvania'),
        ('RI','Rhode Island'),
        ('SC','South Carolina'),
        ('SD','South Dakota'),
        ('TN','Tennessee'),
        ('TX','Texas'),
        ('UT','Utah'),
        ('VA','Virginia'),
        ('VT','Vermont'),
        ('WA','Washington'),
        ('WI','Wisconsin'),
        ('WV','West Virginia'),
        ('WY','Wyoming')
    ], validators=[])
    postal_code = StringField('ZIP Code', validators=[])

class SearchForm(FlaskForm):
    line_1 = StringField('Street Address', validators=[])
    city = StringField('City', validators=[])
    state_province = SelectField('State', choices=[
        ('AK','Alaska'),
        ('AL','Alabama'),
        ('AR','Arkansas'),
        ('AZ','Arizona'),
        ('CA','California'),
        ('CT','Connecticut'),
        ('DC','Washington DC'),
        ('DE','Delaware'),
        ('FL','Florida'),
        ('GA','Georgia'),
        ('HI','Hawaii'),
        ('IA','Iowa'),
        ('ID','Idaho'),
        ('IL','Illinois'),
        ('IN','Indiana'),
        ('KS','Kansas'),
        ('KY','Kentucky'),
        ('LA','Louisiana'),
        ('MA','Massachusetts'),
        ('MA','Massachusetts'),
        ('MD','Maryland'),
        ('ME','Maine'),
        ('MI','Michigan'),
        ('MN','Minnesota'),
        ('MO','Missouri'),
        ('MS','Mississippi'),
        ('MT','Montana'),
        ('NC','North Carolina'),
        ('ND','North Dakota'),
        ('NE','Nebraska'),
        ('NH','New Hampshire'),
        ('NJ','New Jersey'),
        ('NM','New Mexico'),
        ('NV','Nevada'),
        ('NY','New York'),
        ('OH','Ohio'),
        ('OK','Oklahoma'),
        ('OR','Oregon'),
        ('PA','Pennsylvania'),
        ('RI','Rhode Island'),
        ('SC','South Carolina'),
        ('SD','South Dakota'),
        ('TN','Tennessee'),
        ('TX','Texas'),
        ('UT','Utah'),
        ('VA','Virginia'),
        ('VT','Vermont'),
        ('WA','Washington'),
        ('WI','Wisconsin'),
        ('WV','West Virginia'),
        ('WY','Wyoming')
    ], validators=[])
    postal_code = StringField('ZIP Code', validators=[])
    name = StringField('Name', validators=[])

class PropertyForm(FlaskForm):
    address = FormField(AddressForm)
    owner_occupied = BooleanField()
    property_type = SelectField('Property Type', choices=[
                                        ('', ''),
                                        ('0', 'Single Family'),
                                        ('1', 'Residential Multi Family'),
                                        ('2', 'Commercial Multi Fmaily'),
                                        ('3', 'Self Storage'),
                                        ('4', 'Retail')],
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
