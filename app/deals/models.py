from app import db
from app.mixins import StateMixin

class Deal(StateMixin, db.Model):
    __tablename__ = 'deal'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    ad
    equity = db.Column(db.Integer)
    sq_feet = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    last_sale_date = db.Column(db.Date)
    owner_occupied = db.Column(db.Boolean)

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
