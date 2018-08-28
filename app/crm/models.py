from app import db
from app.mixins import SearchableMixin
from app.src.util.string_util import StringUtil
from app.deals.models import Address
from app import constants as CONSTANTS

class Contact(SearchableMixin, db.Model):
    __searchable__ = ['first_name', 'last_name']
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    contact_type = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    referral_source = db.Column(db.String(255))
    investment_strategy = db.Column(db.String(255))
    investment_criteria = db.relationship("InvestmentCriteria")


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

    def __init__(self, **kwargs):
        super(Investor, self).__init__(**kwargs)

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

class InvestmentCriteria(db.Model):
    __tablename__ = 'investmentcriteria'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    property_type = db.Column(db.Integer)
    flip = db.Column(db.Boolean)
    rental = db.Column(db.Boolean)
    minimum_units = db.Column(db.Integer)
    maximum_units = db.Column(db.Integer)

    def getPropertyType(self):
          return CONSTANTS.PROPERTY_TYPE[self.property_type]

    def getRole(self):
      return USER.ROLE[self.role]

class LocationCriteria(db.Model):
    __tablename__ = 'locationcriteria'
    id = db.Column(db.Integer, primary_key=True)
    illinois = db.Column(db.Boolean)
    indiana = db.Column(db.Boolean)
    iowa = db.Column(db.Boolean)
    florida = db.Column(db.Boolean)
    texas = db.Column(db.Boolean)
