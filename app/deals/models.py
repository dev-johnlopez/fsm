from app import db
from app.mixins import StateMixin
#from app.src.util.string_util import StringUtil

class Deal(StateMixin, db.Model):
    __tablename__ = 'deal'
    id = db.Column(db.Integer, primary_key=True)
    list_price = db.Column(db.Integer)
    rehab_amount = db.Column(db.Integer)
    after_repair_value = db.Column(db.Integer)
    equity = db.Column(db.Integer)
    return_on_investment = db.Column(db.String(255))
    monthly_rent = db.Column(db.Integer)
    taxes = db.Column(db.Integer)
    insurance = db.Column(db.Integer)
    maintenance_percent = db.Column(db.Integer)
    management_percent = db.Column(db.Integer)
    utility_amount = db.Column(db.Integer)
    utility_description = db.Column(db.String(255))
    capex_reserves = db.Column(db.Integer)
    net_operating_income = db.Column(db.Integer)
    cap_rate = db.Column(db.String(255))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    property = db.relationship('Property', uselist=False)
    contacts = db.relationship('DealContact', backref='deal', lazy=True)

    def __repr__(self):
        return str(self.property)

    def addOwnerToDeal(self, contact):
        role = DealContactRole(name="Owner")
        for dContact in self.contacts:
            if dContact.contact == contact:
                dContact.roles.append(role)
                return
        dealContact = DealContact(contact=contact, roles=[role])
        self.contacts.append(dealContact)


class DealContact(db.Model):
    __tablename__ = 'dealcontact'
    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact', uselist=False)
    roles = db.relationship('DealContactRole', backref='contact', lazy=True)

class DealContactRole(db.Model):
    __tablename__ = 'dealcontactrole'
    id = db.Column(db.Integer, primary_key=True)
    deal_contact_id = db.Column(db.Integer, db.ForeignKey('dealcontact.id'))
    name = db.Column(db.String(255), nullable=False)


class Property(db.Model):
    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    type = db.Column(db.String(255))
    address = db.relationship('Address', uselist=False)
    sq_feet = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    basement_type = db.Column(db.String(255))
    garage_type = db.Column(db.String(255))
    last_sale_date = db.Column(db.Date)
    owner_occupied = db.Column(db.Boolean)

    def __repr__(self):
        return str(self.address)


#import enum
#class AddressTypeEnum(enum.Enum):
#    mailing = 1
#    physical = 2

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    line_1 = db.Column(db.String(255))
    line_2 = db.Column(db.String(255))
    line_3 = db.Column(db.String(255))
    line_4 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state_province = db.Column(db.String(255))
    postal_code = db.Column(db.String(20))
    county = db.Column(db.String(255))
    country = db.Column(db.String(255))

    def __repr__(self):
        return self.line_1
        #return StringUtil.joinStringsWithBuffer(", ", [self.ine_1, self.city, self.state_province])
#
