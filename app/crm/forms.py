from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FormField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired

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
