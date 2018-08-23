from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security
from flask_admin import Admin
from config import Config
from sqlalchemy import event
from elasticsearch import Elasticsearch

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
security = Security()
admin = Admin()

def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)
        security.init_app(app)
        app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.deals import bp as deals_bp
        app.register_blueprint(deals_bp, url_prefix="/deals")

        from app.crm import bp as crm_bp
        app.register_blueprint(crm_bp, url_prefix="/crm")

        from app.upload import bp as upload_bp
        app.register_blueprint(upload_bp, url_prefix="/import")

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.admin import create_admin
        admin = create_admin(app, db)

        return app

from app.deals.models import *
event.listen(Deal, 'init', Deal.init_state_machine)
event.listen(Deal, 'load', Deal.init_state_machine)
