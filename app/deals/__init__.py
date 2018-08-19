from flask import Blueprint

bp = Blueprint('deals', __name__)

from app.deals import routes
