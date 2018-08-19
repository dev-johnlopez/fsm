from app import db
from app.mixins import StateMixin

class Deal(StateMixin, db.Model):
    __tablename__ = 'deal'
    id = db.Column(db.Integer, primary_key=True)
