from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, RadioField, SelectField, FieldList
from wtforms.validators import DataRequired
from app.crm.models import InvestmentCriteria

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

class InvestmentCriteriaForm(FlaskForm):
    property_type = SelectField('Property Type', choices=[
                                        ('', ''),
                                        ('0', 'Single Family'),
                                        ('1', 'Residential Multi Family'),
                                        ('2', 'Commercial Multi Fmaily'),
                                        ('3', 'Self Storage'),
                                        ('4', 'Retail')],
                            validators=[DataRequired()])
    flip = RadioField("Do you flip this properties?", choices=[('0','No'),('1','Yes')], validators=[DataRequired()])
    rental = RadioField("Do you buy & hold this properties?", choices=[('0','No'),('1','Yes')], validators=[DataRequired()])
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
