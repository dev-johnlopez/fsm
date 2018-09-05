from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.crm.models import Contact
from app.deals.models import Deal, Property, Address
from app.auth.models import User

def create_admin(app, db):
    admin = Admin(app, name='FSM', template_mode='bootstrap3')
    admin.add_view(ModelView(Contact, db.session))
    admin.add_view(ModelView(Deal, db.session))
    admin.add_view(ModelView(Property, db.session))
    admin.add_view(ModelView(Address, db.session))
    admin.add_view(ModelView(User, db.session))
    return admin
