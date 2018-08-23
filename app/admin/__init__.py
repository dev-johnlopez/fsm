from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.crm.models import Contact
from app.deals.models import Deal

def create_admin(app, db):
    admin = Admin(app, name='FSM', template_mode='bootstrap3')
    admin.add_view(ModelView(Contact, db.session))
    admin.add_view(ModelView(Deal, db.session))
    return admin
