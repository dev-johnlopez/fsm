from app import db
from app import constants as CONSTANTS
import app.crm.models as crm_models
from app.common import BaseModel
from app.mixins import StateMixin
#from app.deals import constants as CONSTANTS
#from app.deals import constants as CONSTANTS

#from app.src.util.string_util import StringUtil

class Deal(StateMixin, BaseModel):
    __tablename__ = 'deal'
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
    #contacts = db.relationship('DealContact', backref='deal', lazy=True)

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

    def getApplicableBuyers(self):
        pass

    def getInterestedContacts(self):
        query = crm_models.Contact.query.join(crm_models.InvestmentCriteria).join(crm_models.LocationCriteria)
        deal_zip_code = self.property.address.postal_code
        query = query.filter(crm_models.LocationCriteria.location_code.like('%' + deal_zip_code + '%'))
        return query.all()

class Property(BaseModel):
    __tablename__ = 'property'
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    property_type = db.Column(db.Integer)
    address = db.relationship('Address', uselist=False)
    sq_feet = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    basement_type = db.Column(db.String(255))
    garage_type = db.Column(db.String(255))
    last_sale_date = db.Column(db.Date)
    owner_occupied = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.OTHER,
        'polymorphic_on':property_type
    }

    def __repr__(self):
        return str(self.address)

    def getPropertyType(self):
          return CONSTANTS.PROPERTY_TYPE[self.property_type]

class ResidentialProperty(Property):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.RESIDENTIAL
    }

    def __init__(self, **kwargs):
        super(ResidentialProperty, self).__init__(**kwargs)


class SingleFamilyProperty(ResidentialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.SFR
    }

    def __init__(self, **kwargs):
        super(SingleFamilyProperty, self).__init__(**kwargs)

class ResidentialMultiFamilyProperty(ResidentialProperty):
    units = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.RESIDENTIAL_MULTI_FAMILY
    }

    def __init__(self, **kwargs):
        super(ResidentialMultiFamilyProperty, self).__init__(**kwargs)

class CommercialProperty(Property):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.COMMERCIAL
    }

    def __init__(self, **kwargs):
        super(CommercialProperty, self).__init__(**kwargs)

class CommercialMultiFamilyProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.COMMERCIAL_MULTI_FAMILY
    }

    def __init__(self, **kwargs):
        super(CommercialMultiFamilyProperty, self).__init__(**kwargs)

class SelfStorageProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.SELF_STORAGE
    }

    def __init__(self, **kwargs):
        super(SelfStorageProperty, self).__init__(**kwargs)

class RetailProperty(CommercialProperty):

    __mapper_args__ = {
        'polymorphic_identity':CONSTANTS.RETAIL
    }

    def __init__(self, **kwargs):
        super(RetailProperty, self).__init__(**kwargs)

class Address(BaseModel):
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




#class DealContact(db.Model):
#    __tablename__ = 'dealcontact'
#    id = db.Column(db.Integer, primary_key=True)
#    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))
#    address_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
#    contact = db.relationship('Contact', uselist=False)
#    roles = db.relationship('DealContactRole', backref='contact', lazy=True)

#class DealContactRole(db.Model):
#    __tablename__ = 'dealcontactrole'
#    id = db.Column(db.Integer, primary_key=True)
#    deal_contact_id = db.Column(db.Integer, db.ForeignKey('dealcontact.id'))
#    name = db.Column(db.String(255), nullable=False)
