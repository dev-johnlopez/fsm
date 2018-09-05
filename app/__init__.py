from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_mail import Mail
import flask_excel as excel
from config import Config
from sqlalchemy import event
from elasticsearch import Elasticsearch
import logging
from logging.handlers import SMTPHandler
from geopy.geocoders import Nominatim

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
security = Security()
admin = Admin()
mail = Mail()
geolocator = Nominatim(user_agent='Assignably')
#excel = Excel()

def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)
        excel.init_excel(app)

        app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

        from app.auth.models import Role, User

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app=app, datastore=user_datastore)

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

        if not app.debug and not app.testing:
            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
            else:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/microblog.log',
                                                   maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Assignably startup')

        return app

#from app.deals.models import Address
#event.listen(Address, 'before_flush', Address.geocode)
#event.listen(Deal, 'load', Deal.init_state_machine)
