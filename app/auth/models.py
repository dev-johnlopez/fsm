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
    user_contact = db.relationship('UserContact', uselist=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.user_contact = UserContact()
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '%s' % (self.email)

    def getUserContacts(self):
        return Contact.query.filter_by(create_user_id=self.id).filter_by(active=True).all()

    def searchContactsByEmail(self, email):
        return Contact.query.filter_by(create_user_id=self.id).filter_by(email=email).first()

    def getDeals(self):
        return Deal.query.filter_by(create_user_id=self.id).all()

class UserContact(db.Model):

    __tablename__ = 'usercontact'

    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact', uselist=False)

    def __init__(self, **kwargs):
        self.contact = Contact()
        super(UserContact, self).__init__(**kwargs)
