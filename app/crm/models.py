from app import db
from app.mixins import SearchableMixin
from app.src.util.string_util import StringUtil

class Contact(SearchableMixin, db.Model):
    __searchable__ = ['first_name', 'last_name']
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    contact_type = db.Column(db.String(50))
    addresses = db.relationship("ContactAddress", back_populates="contact")
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    referral_source = db.Column(db.String(255))
    investment_strategy = db.Column(db.String(255))
    propertytypecriteria_id = db.Column(db.Integer, db.ForeignKey('propertytypecriteria.id'))
    property_type_criteria = db.relationship("PropertyTypeCriteria")
    locationcriteria_id = db.Column(db.Integer, db.ForeignKey('locationcriteria.id'))
    location_criteria = db.relationship("LocationCriteria")


    __mapper_args__ = {
        'polymorphic_identity':'contact',
        'polymorphic_on':contact_type
    }

    def __init__(self, **kwargs):
        self.addresses = []
        super(Contact, self).__init__(**kwargs)

    def __repr__(self):
        return self.name

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

class ContactAddress(db.Model):
    __tablename__ = 'contactaddress'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact", back_populates="addresses")
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship("Address")
    type = db.Column(db.String(255))

class PropertyTypeCriteria(db.Model):
    __tablename__ = 'propertytypecriteria'
    id = db.Column(db.Integer, primary_key=True)
    unknown = db.Column(db.Boolean)
    single_family = db.Column(db.Boolean)
    residential_multi_family = db.Column(db.Boolean)
    small_multi_family = db.Column(db.Boolean)
    medium_multi_family = db.Column(db.Boolean)
    large_multi_family = db.Column(db.Boolean)
    multi_family_complexes = db.Column(db.Boolean)
    self_storage = db.Column(db.Boolean)
    retail = db.Column(db.Boolean)

class LocationCriteria(db.Model):
    __tablename__ = 'locationcriteria'
    id = db.Column(db.Integer, primary_key=True)
    illinois = db.Column(db.Boolean)
    indiana = db.Column(db.Boolean)
    iowa = db.Column(db.Boolean)
    florida = db.Column(db.Boolean)
    texas = db.Column(db.Boolean)
