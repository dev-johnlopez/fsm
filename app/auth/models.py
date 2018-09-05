from app import db
from flask_security import UserMixin, RoleMixin
from app.deals.models import Deal
from app.crm.models import Contact

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '%s' % (self.name)

# Define a User model
class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(40))
    current_login_ip = db.Column(db.String(40))
    login_count = db.Column(db.Integer)
    user_contact_id = db.Column(db.Integer, db.ForeignKey('usercontact.id'))
    user_contact = db.relationship('UserContact', uselist=False, backref='user')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    deals = db.relationship('Deal', backref='created_by', lazy=True)
    contacts = db.relationship('Contact', backref='created_by', lazy=True)

    def __init__(self, **kwargs):
        self.user_contact = UserContact()
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '%s' % (self.email)

    def getUserContacts(self):
        return [contact for contact in self.contacts if contact.active]

    def searchContactsByEmail(self, email):
        for contact in self.contacts:
            if contact.email == email and contact.active:
                return contact
        return None

    def getDeals(self):
        return self.deals

class UserContact(db.Model):

    __tablename__ = 'usercontact'

    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact', uselist=False)

    def __init__(self, **kwargs):
        self.contact = Contact()
        super(UserContact, self).__init__(**kwargs)
