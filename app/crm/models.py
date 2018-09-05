from app import db
from app.common import BaseModel
from app.mixins import SearchableMixin, AuditMixin
from app.src.util.string_util import StringUtil
from app import constants as CONSTANTS

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
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

    def hasMatchingCriteriaForDeal(self, deal):
        for criteria in self.investment_criteria:
            if criteria.doesDealMatchCriteria(deal):
                return True
        return False

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

class LocationCriteria(db.Model):
    __tablename__ = 'locationcriteria'
    id = db.Column(db.Integer, primary_key=True)
    location_type = db.Column(db.String(255))
    location_code = db.Column(db.String(255))
    criteria_id = db.Column(db.Integer, db.ForeignKey('investmentcriteria.id'))

    def doesDealMatchLocation(self, deal):
        if location_type == "State":
            return deal.property.address.state_province == location_code
        if location_type == "Zip Code":
            return deal.property.address.postal_code == location_code
        return False

class InvestmentCriteria(db.Model):
    __tablename__ = 'investmentcriteria'
    id = db.Column(db.Integer, primary_key=True)
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

    def doesDealMatchCriteria(self, deal):
        num_units = deal.property.units
        if self.minimum_units > self.num_units:
            return False
        if self.maximum_units < num_units and self.maximum_units > 0:
            return False
        for location in self.locations:
            if location.doesDealMatchLocation(self, deal):
                return True
        return False
