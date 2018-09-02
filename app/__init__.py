from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_mail import Mail
from config import Config
from sqlalchemy import event
from elasticsearch import Elasticsearch
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
security = Security()
admin = Admin()
mail = Mail()

def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)

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

        #if not app.debug:
        #    if app.config['MAIL_SERVER']:
        #        auth = None
        #        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        #            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        #        secure = None
        #        if app.config['MAIL_USE_TLS']:
        #            secure = ()
        #        mail_handler = SMTPHandler(
        #            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        #            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        #            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
        #            credentials=auth, secure=secure)
        #        mail_handler.setLevel(logging.ERROR)
        #        app.logger.addHandler(mail_handler)

        return app

#from app.deals.models import Deal
#event.listen(Deal, 'init', Deal.init_state_machine)
#event.listen(Deal, 'load', Deal.init_state_machine)
