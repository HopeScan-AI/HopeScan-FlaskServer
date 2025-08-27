import os
from flask import Flask
from dotenv import load_dotenv
import logging

from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()  # Also print logs to console
    ])
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name=os.getenv('FLASK_ENV')):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False



    CORS(app, resources={r"/*": {"origins": "http://localhost:3005"}}, supports_credentials=True)
    # CORS(app, supports_credentials=True)
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3005"}})
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.models import Case, Image, User, DriveImage

    from app.modules.myDBA import myDBA
    from app.modules.user import users
    from app.modules.case import cases
    from app.modules.image import images
    from app.modules.drive_images import drive_images
    from app.modules.auth import auth, google_auth
    from app.modules.providers import providers
    from app.modules.notifications import notification
    from app.modules.ai import ai
    from app.modules.subscriptions import payments
    from app.modules.subscriptions import subscriptions
    from app.modules.plans import plans
    from app.modules import landing_page

    app.register_blueprint(myDBA.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(cases.bp)
    app.register_blueprint(images.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(landing_page.bp)
    app.register_blueprint(google_auth.bp)
    app.register_blueprint(drive_images.bp)
    app.register_blueprint(notification.bp)
    app.register_blueprint(providers.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(subscriptions.bp)
    app.register_blueprint(plans.bp)

    return app
