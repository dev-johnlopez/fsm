from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, RadioField, SelectField, FieldList
from wtforms.validators import DataRequired
from app.crm.models import InvestmentCriteria, LocationCriteria
from app.fieldtypes import StateSelectField
from app import constants as CONSTANTS

class SearchForm(FlaskForm):
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])
    #contact_type = RadioField('Type', choices=[
    #                                    ('investor', 'Investor'),
    #                                    ('builder', 'Builder'),
    #                                    ('wholesaler', 'Wholesaler'),
    #                                    ('realtor', 'Realtor'),
    #                                    ('property_manager', 'Property Manager'),
    #                                    ('lender', 'Lender'),
    #                                    ('contact', 'Other Professional')],
    #                        validators=[])
    phone = StringField('Phone', validators=[])
    email = StringField('Email', validators=[])

class InvestmentLocationForm(FlaskForm):
    location_type = SelectField('Location Type', choices=[
                                        ('1', 'Zip Code')],
                            validators=[DataRequired()])
    location_code = StringField('Location Code', validators=[DataRequired()])

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(InvestmentLocationForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

class InvestmentCriteriaForm(FlaskForm):
    property_type = SelectField('Property Type', choices=[
                                        ('', ''),
                                        (str(CONSTANTS.SFR), 'Single Family'),
                                        (str(CONSTANTS.RESIDENTIAL_MULTI_FAMILY), 'Residential Multi Family'),
                                        (str(CONSTANTS.COMMERCIAL_MULTI_FAMILY), 'Commercial Multi Fmaily'),
                                        (str(CONSTANTS.SELF_STORAGE), 'Self Storage'),
                                        (str(CONSTANTS.RETAIL), 'Retail')],
                            validators=[DataRequired()])
    flip = RadioField("Do you flip this properties?", choices=[('0','No'),('1','Yes')], validators=[DataRequired()])
    rental = RadioField("Do you buy & hold this properties?", choices=[('0','No'),('1','Yes')], validators=[DataRequired()])
    locations = FieldList(FormField(InvestmentLocationForm, default=lambda: LocationCriteria()))
    minimum_units = IntegerField()
    maximum_units = IntegerField()



class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[])
    last_name = StringField('Last Name', validators=[])
    contact_type = RadioField('Type', choices=[
                                        ('investor', 'Investor'),
                                        ('builder', 'Builder'),
                                        ('wholesaler', 'Wholesaler'),
                                        ('realtor', 'Realtor'),
                                        ('property_manager', 'Property Manager'),
                                        ('lender', 'Lender'),
                                        ('contact', 'Other Professional')],
                            validators=[DataRequired()])
    phone = StringField('Phone', validators=[])
    email = StringField('Email', validators=[])
    investment_criteria = FieldList(FormField(InvestmentCriteriaForm, default=lambda: InvestmentCriteria()))
