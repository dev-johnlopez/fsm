from app import db
from app.common import BaseModel
from app.mixins import SearchableMixin
from app.src.util.string_util import StringUtil
from app import constants as CONSTANTS

class Contact(SearchableMixin, BaseModel):
    __searchable__ = ['first_name', 'last_name']
    __tablename__ = 'contact'
    active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    contact_type = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    referral_source = db.Column(db.String(255))
    investment_strategy = db.Column(db.String(255))
    investment_criteria = db.relationship('InvestmentCriteria')


    __mapper_args__ = {
        'polymorphic_identity':'contact',
        'polymorphic_on':contact_type
    }

    def __init__(self, **kwargs):
        self.addresses = []
        super(Contact, self).__init__(**kwargs)

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def mailing_address(self):
        return self.addresses[0].address

    def addMailingAddress(self, address):
        self.addresses.append(ContactAddress(type="mailing", address=address))


class Investor(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'investor'
    }

class Builder(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'builder'
    }

    def __init__(self, **kwargs):
        super(Builder, self).__init__(**kwargs)

class Wholesaler(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'wholesaler'
    }

    def __init__(self, **kwargs):
        super(Builder, self).__init__(**kwargs)

class Realtor(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'realtor'
    }

    def __init__(self, **kwargs):
        super(Builder, self).__init__(**kwargs)

class PropertyManager(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'property_manager'
    }

    def __init__(self, **kwargs):
        super(Builder, self).__init__(**kwargs)

class Lender(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'lender'
    }

    def __init__(self, **kwargs):
        super(Builder, self).__init__(**kwargs)

class LocationCriteria(BaseModel):
    __tablename__ = 'locationcriteria'
    location_type = db.Column(db.String(255))
    location_code = db.Column(db.String(255))
    criteria_id = db.Column(db.Integer, db.ForeignKey('investmentcriteria.id'))

class InvestmentCriteria(BaseModel):
    __tablename__ = 'investmentcriteria'
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    property_type = db.Column(db.Integer)
    flip = db.Column(db.Integer)
    rental = db.Column(db.Integer)
    minimum_units = db.Column(db.Integer)
    maximum_units = db.Column(db.Integer)
    locations = db.relationship('LocationCriteria')

    def getPropertyType(self):
          return CONSTANTS.PROPERTY_TYPE[self.property_type]

    def getDetailedPropertyType(self):
        if self.property_type == CONSTANTS.SFR:
            return self.getPropertyType()
        if self.maximum_units == -1:
            return '{} ({}+ Units)'.format(self.getPropertyType(), self.minimum_units)
        else:
            return '{} ({}-{} Units)'.format(self.getPropertyType(), self.minimum_units, self.maximum_units)

    def getLocations(self):
        return ', '.join(location.location_code for location in self.locations)
