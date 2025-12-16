import logging
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name=os.getenv('FLASK_ENV', '')):
    """
    Flask application factory
    """
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    CORS(app, resources={r"/*": {"origins": "http://localhost:3005"}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.models import Case, DriveImage, Image, User

    from app.modules import landing_page
    from app.modules.ai import ai
    from app.modules.auth import auth, google_auth
    from app.modules.case import cases
    from app.modules.drive_images import drive_images
    from app.modules.image import images
    from app.modules.myDBA import myDBA
    from app.modules.notifications import notification
    from app.modules.plans import plans
    from app.modules.providers import providers
    from app.modules.subscriptions import payments, subscriptions
    from app.modules.user import users

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
