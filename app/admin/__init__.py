from flask_admin import Admin

def create_admin(app, db):
    admin = Admin(app, name='FSM', template_mode='bootstrap3')
    return admin
