from app import db
from app.mixins import SearchableMixin
from app.src.util.string_util import StringUtil

class Contact(SearchableMixin, db.Model):
    __searchable__ = ['name']
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(50))
    addresses = db.relationship("ContactAddress", back_populates="contact")
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity':'contact',
        'polymorphic_on':type
    }

    def __init__(self, **kwargs):
        print("******** constructing!")
        self.addresses = []
        super(Contact, self).__init__(**kwargs)

    def __repr__(self):
        return self.name

    @property
    def mailing_address(self):
        return self.addresses[0].address

    def addMailingAddress(self, address):
        self.addresses.append(ContactAddress(type="mailing", address=address))


class Person(Contact):
    __searchable__ = ['first_name', 'last_name']
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    suffix = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity':'person'
    }

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)

    def __repr__(self):
        return StringUtil.joinStringsWithBuffer(" ", [self.first_name, self.last_name, self.suffix])

class Company(Contact):

    __mapper_args__ = {
        'polymorphic_identity':'company'
    }

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)

    def __repr__(self):
        return self.name

class ContactAddress(db.Model):
    __tablename__ = 'contactaddress'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact", back_populates="addresses")
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship("Address", back_populates="contact_address")
    type = db.Column(db.String(255))
